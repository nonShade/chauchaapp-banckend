"""
Transactions service — business logic layer.
"""

import math
from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from app.modules.transactions.dto import (
    CategoryDistributionDTO,
    FinancialSummaryDTO,
    IncomeTypeResponseDTO,
    IncomeVsExpensesDTO,
    PaginationMetaDTO,
    TransactionCategoryResponseDTO,
    TransactionCreateDTO,
    TransactionFrequencyResponseDTO,
    TransactionPaginationResponseDTO,
    TransactionResponseDTO,
    TransactionTypeResponseDTO,
    TransactionUpdateDTO,
)
from app.modules.transactions.entities import Transaction
from app.modules.transactions.repository import TransactionsRepository
from app.shared.exceptions import ForbiddenException, NotFoundException


class TransactionsService:
    """Business logic for transaction entities."""

    def __init__(self, repository: TransactionsRepository):
        self._repository = repository

    def get_income_types(self) -> list[IncomeTypeResponseDTO]:
        """Get all available income types.
        
        Returns:
            List of income types.
        """
        income_types = self._repository.get_all_income_types()
        return [
            IncomeTypeResponseDTO(id=it.income_type_id, name=it.name)
            for it in income_types
        ]

    def get_transaction_types(self) -> list[TransactionTypeResponseDTO]:
        """Get all transaction types."""
        types = self._repository.get_all_transaction_types()
        return [
            TransactionTypeResponseDTO(
                id=t.transaction_type_id, name=t.name, description=t.description
            )
            for t in types
        ]

    def get_transaction_frequencies(self) -> list[TransactionFrequencyResponseDTO]:
        """Get all transaction frequencies."""
        frequencies = self._repository.get_all_transaction_frequencies()
        return [
            TransactionFrequencyResponseDTO(
                id=f.transaction_frequency_id, name=f.name, description=f.description
            )
            for f in frequencies
        ]

    def get_transaction_categories(self) -> list[TransactionCategoryResponseDTO]:
        """Get all transaction categories."""
        categories = self._repository.get_all_transaction_categories()
        return [
            TransactionCategoryResponseDTO(
                id=c.transaction_category_id,
                name=c.name,
                description=c.description,
                transaction_type_id=c.transaction_type_id,
            )
            for c in categories
        ]

    def create_transaction(
        self, user_id: UUID, data: TransactionCreateDTO
    ) -> TransactionResponseDTO:
        """Create a new transaction for the user."""
        transaction = Transaction(
            user_id=user_id,
            amount=data.amount,
            transaction_type_id=data.transaction_type_id,
            transaction_category_id=data.transaction_category_id,
            transaction_frequency_id=data.transaction_frequency_id,
            description=data.description,
            transaction_date=data.transaction_date,
        )
        created = self._repository.create_transaction(transaction)
        return self._map_to_response_dto(created)

    def update_transaction(
        self, user_id: UUID, transaction_id: UUID, data: TransactionUpdateDTO
    ) -> TransactionResponseDTO:
        """Update an existing transaction if it belongs to the user."""
        transaction = self._repository.get_transaction_by_id(transaction_id)
        if not transaction:
            raise NotFoundException("La transacción no existe")

        if transaction.user_id != user_id:
            raise ForbiddenException("No puedes editar una transacción que no te pertenece")

        updated = self._repository.update_transaction(
            transaction_id, **data.model_dump(exclude_unset=True)
        )
        return self._map_to_response_dto(updated)

    def delete_transaction(self, user_id: UUID, transaction_id: UUID) -> bool:
        """Delete a transaction if it belongs to the user."""
        transaction = self._repository.get_transaction_by_id(transaction_id)
        if not transaction:
            raise NotFoundException("La transacción no existe")

        if transaction.user_id != user_id:
            raise ForbiddenException("No tienes permiso para eliminar este registro")

        return self._repository.delete_transaction(transaction_id)

    def get_user_transactions(
        self,
        user_id: UUID,
        page: int = 1,
        limit: int = 10,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> TransactionPaginationResponseDTO:
        """Get paginated transactions for the user."""
        transactions, total_count = self._repository.get_transactions_by_user(
            user_id, page, limit, start_date, end_date
        )

        total_pages = math.ceil(total_count / limit) if total_count > 0 else 0

        meta = PaginationMetaDTO(
            currentPage=page,
            totalPages=total_pages,
            totalItems=total_count,
            itemsPerPage=limit,
        )

        data = [self._map_to_response_dto(t) for t in transactions]

        return TransactionPaginationResponseDTO(meta=meta, data=data)

    def _map_to_response_dto(self, t: Transaction) -> TransactionResponseDTO:
        """Helper to map Transaction entity to TransactionResponseDTO."""
        return TransactionResponseDTO(
            transaction_id=t.transaction_id,
            amount=t.amount,
            description=t.description,
            transaction_date=t.transaction_date,
            transaction_type_id=t.transaction_type_id,
            transaction_category_id=t.transaction_category_id,
            transaction_frequency_id=t.transaction_frequency_id,
        )

    def get_financial_summary(
        self, user_id: UUID, start_date: date | None = None, end_date: date | None = None
    ) -> FinancialSummaryDTO:
        """Calculate financial totals for a given period."""
        if not start_date:
            start_date = date.today().replace(day=1)
        if not end_date:
            end_date = date.today()

        totals = self._repository.get_totals_by_type(user_id, start_date, end_date)
        
        income = Decimal("0")
        expenses = Decimal("0")
        
        for name, amount in totals:
            name_norm = name.lower().strip() if name else ""
            if name_norm == "ingreso":
                income += amount
            elif name_norm == "gasto":
                expenses += amount
        
        return FinancialSummaryDTO(
            total_income=income,
            total_expenses=expenses,
            total_balance=income - expenses
        )

    def get_expense_distribution(
        self, user_id: UUID, start_date: date | None = None, end_date: date | None = None
    ) -> list[CategoryDistributionDTO]:
        """Get total expenses by category and their percentage."""
        if not start_date:
            start_date = date.today().replace(day=1)
        if not end_date:
            end_date = date.today()

        results = self._repository.get_distribution_by_category(user_id, start_date, end_date)
        
        total_expense = sum(amount for _, _, amount in results)
        
        distribution = []
        for cat_id, cat_name, amount in results:
            percentage = (float(amount) / float(total_expense) * 100) if total_expense > 0 else 0
            distribution.append(
                CategoryDistributionDTO(
                    category_id=cat_id,
                    category_name=cat_name,
                    total_amount=amount,
                    percentage=round(percentage, 2)
                )
            )
        
        return distribution

    def get_income_vs_expenses(self, user_id: UUID) -> list[IncomeVsExpensesDTO]:
        """Compare income vs expenses over the last 6 months."""
        results = self._repository.get_monthly_comparison(user_id)
        
        # Group by month
        monthly_data = {}
        for month, type_name, amount in results:
            if month not in monthly_data:
                monthly_data[month] = {"income": Decimal("0"), "expenses": Decimal("0")}
            
            type_name_norm = type_name.lower().strip() if type_name else ""
            if type_name_norm == "ingreso":
                monthly_data[month]["income"] += amount
            elif type_name_norm == "gasto":
                monthly_data[month]["expenses"] += amount
        
        comparison = []
        for month, data in sorted(monthly_data.items()):
            comparison.append(
                IncomeVsExpensesDTO(
                    month=month,
                    income=data["income"],
                    expenses=data["expenses"]
                )
            )
        
        return comparison

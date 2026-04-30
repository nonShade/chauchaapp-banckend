"""
Transactions repository — data access layer.
"""

from datetime import date
from decimal import Decimal
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.modules.users.entities import IncomeType
from app.modules.transactions.entities import (
    TransactionCategory,
    TransactionFrequency,
    Transaction,
    TransactionType,
)


class TransactionsRepository:
    """Data access for transaction-related entries (including income types)."""

    def __init__(self, session: Session):
        self._session = session

    def get_all_income_types(self) -> list[IncomeType]:
        """Get all available income types.

        Returns:
            A list of IncomeType entities.
        """
        return self._session.query(IncomeType).all()

    def get_all_transaction_types(self) -> list[TransactionType]:
        """Get all available transaction types."""
        return self._session.query(TransactionType).all()

    def get_all_transaction_frequencies(self) -> list[TransactionFrequency]:
        """Get all available transaction frequencies."""
        return self._session.query(TransactionFrequency).all()

    def get_all_transaction_categories(self) -> list[TransactionCategory]:
        """Get all available transaction categories."""
        return self._session.query(TransactionCategory).all()

    def create_transaction(self, transaction: Transaction) -> Transaction:
        """Create a new financial transaction."""
        self._session.add(transaction)
        self._session.commit()
        self._session.refresh(transaction)
        return transaction

    def update_transaction(self, transaction_id: UUID, **kwargs) -> Transaction | None:
        """Update an existing transaction."""
        transaction = self.get_transaction_by_id(transaction_id)
        if not transaction:
            return None

        for key, value in kwargs.items():
            if value is not None:
                setattr(transaction, key, value)

        self._session.commit()
        self._session.refresh(transaction)
        return transaction

    def delete_transaction(self, transaction_id: UUID) -> bool:
        """Delete a transaction."""
        transaction = self.get_transaction_by_id(transaction_id)
        if not transaction:
            return False

        self._session.delete(transaction)
        self._session.commit()
        return True

    def get_transaction_by_id(self, transaction_id: UUID) -> Transaction | None:
        """Retrieve a transaction by its ID."""
        return (
            self._session.query(Transaction)
            .filter(Transaction.transaction_id == transaction_id)
            .first()
        )

    def get_transactions_by_user(
        self,
        user_id: UUID,
        page: int = 1,
        limit: int = 10,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> tuple[list[Transaction], int]:
        """Get paginated transactions for a user with optional date filtering."""
        query = self._session.query(Transaction).filter(Transaction.user_id == user_id)

        if start_date:
            query = query.filter(Transaction.transaction_date >= start_date)
        if end_date:
            query = query.filter(Transaction.transaction_date <= end_date)

        total_count = query.count()

        offset = (page - 1) * limit
        transactions = (
            query.order_by(Transaction.transaction_date.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        return transactions, total_count

    def get_totals_by_type(
        self, user_id: UUID, start_date: date, end_date: date
    ) -> list[tuple[str, Decimal]]:
        """Get total amounts grouped by transaction type (ingreso/gasto)."""
        return (
            self._session.query(TransactionType.name, func.sum(Transaction.amount))
            .join(TransactionType, Transaction.transaction_type_id == TransactionType.transaction_type_id)
            .filter(Transaction.user_id == user_id)
            .filter(Transaction.transaction_date >= start_date)
            .filter(Transaction.transaction_date <= end_date)
            .group_by(TransactionType.name)
            .all()
        )

    def get_distribution_by_category(
        self, user_id: UUID, start_date: date, end_date: date
    ) -> list[tuple[UUID | None, str, Decimal]]:
        """Get total amounts grouped by category for expenses."""
        return (
            self._session.query(
                TransactionCategory.transaction_category_id,
                TransactionCategory.name,
                func.sum(Transaction.amount),
            )
            .join(
                TransactionCategory,
                Transaction.transaction_category_id == TransactionCategory.transaction_category_id,
            )
            .join(
                TransactionType,
                Transaction.transaction_type_id == TransactionType.transaction_type_id,
            )
            .filter(Transaction.user_id == user_id)
            .filter(func.lower(TransactionType.name) == "gasto")
            .filter(Transaction.transaction_date >= start_date)
            .filter(Transaction.transaction_date <= end_date)
            .group_by(TransactionCategory.transaction_category_id, TransactionCategory.name)
            .all()
        )

    def get_monthly_comparison(
        self, user_id: UUID, limit_months: int = 6
    ) -> list[tuple[str, str, Decimal]]:
        """Get monthly totals for income and expenses."""
        # Handle different dialects (PostgreSQL for QA/Prod, SQLite for tests/dev)
        if self._session.bind.dialect.name == "postgresql":
            month_format = func.to_char(Transaction.transaction_date, "YYYY-MM")
        else:
            month_format = func.strftime("%Y-%m", Transaction.transaction_date)
        
        return (
            self._session.query(
                month_format.label("month"),
                TransactionType.name,
                func.sum(Transaction.amount),
            )
            .join(TransactionType, Transaction.transaction_type_id == TransactionType.transaction_type_id)
            .filter(Transaction.user_id == user_id)
            .group_by("month", TransactionType.name)
            .order_by("month")
            .limit(limit_months * 2) 
            .all()
        )

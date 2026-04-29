"""
Transactions service — business logic layer.
"""

from app.modules.transactions.dto import IncomeTypeResponseDTO
from app.modules.transactions.repository import TransactionsRepository


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

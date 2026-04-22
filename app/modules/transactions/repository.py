"""
Transactions repository — data access layer.
"""

from sqlalchemy.orm import Session

from app.modules.users.entities import IncomeType


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

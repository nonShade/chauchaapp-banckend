"""
Transactions controller — HTTP endpoint layer.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.modules.transactions.dto import IncomeTypeResponseDTO
from app.modules.transactions.repository import TransactionsRepository
from app.modules.transactions.service import TransactionsService
from app.shared.database import get_db

router = APIRouter(prefix="/v1/transactions", tags=["Transactions"])


def _get_transactions_service(db: Session = Depends(get_db)) -> TransactionsService:
    """Dependency to build transactions service with its database repository."""
    repository = TransactionsRepository(db)
    return TransactionsService(repository)


@router.get(
    "/income-types",
    response_model=list[IncomeTypeResponseDTO],
    summary="Obtener tipos de ingresos",
    description="Devuelve el catálogo de tipos de ingresos disponibles para registro.",
)
def get_income_types(service: TransactionsService = Depends(_get_transactions_service)):
    """Retrieve all available income types."""
    return service.get_income_types()

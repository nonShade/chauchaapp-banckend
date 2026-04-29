"""
Transactions module DTOs.

Handles data transfer formatting for endpoints in the Transactions module.
"""

from uuid import UUID

from pydantic import BaseModel


class IncomeTypeResponseDTO(BaseModel):
    """Details of an income type available for selection."""

    id: UUID
    name: str

    model_config = {"from_attributes": True}

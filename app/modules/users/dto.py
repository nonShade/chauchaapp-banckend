"""
Users module DTOs — Pydantic models for request/response validation.

All API input/output is validated through these DTOs as required
by the backend development rules.
"""

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator


# ---------------------------------------------------------------------------
# Response DTOs
# ---------------------------------------------------------------------------


class UserProfileResponseDTO(BaseModel):
    """Full user profile response."""

    id: UUID
    first_name: str
    last_name: str
    email: str
    birth_date: date
    income_type_id: UUID | None
    monthly_income: Decimal
    monthly_expenses: Decimal
    topics: list[UUID]


# ---------------------------------------------------------------------------
# Request DTOs
# ---------------------------------------------------------------------------


class UpdateProfileRequestDTO(BaseModel):
    """Update profile request payload with full business-rule validation."""

    first_name: str
    last_name: str
    email: EmailStr
    birth_date: date
    income_type_id: UUID
    monthly_income: Decimal
    monthly_expenses: Decimal
    topics: list[UUID]

    @field_validator("first_name", "last_name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El nombre es requerido")
        return v.strip()

    @field_validator("birth_date")
    @classmethod
    def validate_age(cls, v: date) -> date:
        today = date.today()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 18 or age > 50:
            raise ValueError("La edad debe estar entre 18 y 50 años")
        return v

    @field_validator("monthly_income")
    @classmethod
    def validate_income(cls, v: Decimal) -> Decimal:
        if v < 0:
            raise ValueError("El ingreso mensual no puede ser negativo")
        return v

    @field_validator("monthly_expenses")
    @classmethod
    def validate_expenses(cls, v: Decimal) -> Decimal:
        if v < 0:
            raise ValueError("Los gastos mensuales no pueden ser negativos")
        return v


# ---------------------------------------------------------------------------
# Error DTOs
# ---------------------------------------------------------------------------


class ErrorResponseDTO(BaseModel):
    """Standard error response format."""

    error: str

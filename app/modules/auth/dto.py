"""
Auth module DTOs — Pydantic models for request/response validation.

All API input/output is validated through these DTOs as required
by the backend development rules.
"""

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, EmailStr, field_validator


# ---------------------------------------------------------------------------
# Request DTOs
# ---------------------------------------------------------------------------


class LoginRequestDTO(BaseModel):
    """Login request payload."""

    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("La contraseña es requerida")
        return v


class RegisterRequestDTO(BaseModel):
    """Registration request payload with full business-rule validation."""

    first_name: str
    last_name: str
    email: EmailStr
    password: str
    birth_date: date
    income_type: UUID
    monthly_income: Decimal
    monthly_expenses: Decimal
    topics: list[UUID]

    @field_validator("first_name", "last_name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El nombre es requerido")
        return v.strip()

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("La contraseña debe tener al menos 6 caracteres")
        return v

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
        if v <= 5000:
            raise ValueError("El ingreso mensual debe ser mayor a 5000")
        return v

    @field_validator("topics")
    @classmethod
    def validate_topics(cls, v: list[UUID]) -> list[UUID]:
        if not v or len(v) == 0:
            raise ValueError("Debe seleccionar al menos un tópico")
        return v


# ---------------------------------------------------------------------------
# Response DTOs
# ---------------------------------------------------------------------------


class UserResponseDTO(BaseModel):
    """User data included in authentication responses."""

    id: UUID
    email: str
    first_name: str
    last_name: str
    created_at: datetime | None = None

    model_config = {"from_attributes": True}


class LoginResponseDTO(BaseModel):
    """Successful login response with JWT tokens."""

    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int
    message: str
    user: UserResponseDTO


class RegisterResponseDTO(BaseModel):
    """Successful registration response."""

    message: str
    user: UserResponseDTO


class LogoutResponseDTO(BaseModel):
    """Successful logout response."""

    message: str


class ErrorResponseDTO(BaseModel):
    """Standard error response format."""

    error: str

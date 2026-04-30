"""
Transactions module DTOs.

Handles data transfer formatting for endpoints in the Transactions module.
"""

from datetime import date
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class IncomeTypeResponseDTO(BaseModel):
    """Details of an income type available for selection."""

    id: UUID
    name: str

    model_config = {"from_attributes": True}


class TransactionTypeResponseDTO(BaseModel):
    """Details of a transaction type (e.g. income, expense)."""

    id: UUID
    name: str
    description: str | None = None

    model_config = {"from_attributes": True}


class TransactionFrequencyResponseDTO(BaseModel):
    """Details of a transaction frequency (e.g. one_time, monthly)."""

    id: UUID
    name: str
    description: str | None = None

    model_config = {"from_attributes": True}


class TransactionCategoryResponseDTO(BaseModel):
    """Details of a transaction category."""

    id: UUID
    name: str
    description: str | None = None
    transaction_type_id: UUID | None = None

    model_config = {"from_attributes": True}


class TransactionCreateDTO(BaseModel):
    """Schema for creating a new transaction."""

    amount: Decimal = Field(gt=0)
    transaction_type_id: UUID
    transaction_category_id: UUID | None = None
    transaction_frequency_id: UUID | None = None
    description: str | None = None
    transaction_date: date


class TransactionUpdateDTO(BaseModel):
    """Schema for updating an existing transaction."""

    amount: Decimal | None = Field(None, gt=0)
    transaction_type_id: UUID | None = None
    transaction_category_id: UUID | None = None
    transaction_frequency_id: UUID | None = None
    description: str | None = None
    transaction_date: date | None = None


class TransactionResponseDTO(BaseModel):
    """Schema for transaction record response."""

    transaction_id: UUID
    amount: Decimal
    description: str | None = None
    transaction_date: date
    transaction_type_id: UUID
    transaction_category_id: UUID | None = None
    transaction_frequency_id: UUID | None = None

    model_config = {"from_attributes": True}


class PaginationMetaDTO(BaseModel):
    """Schema for pagination metadata."""

    currentPage: int
    totalPages: int
    totalItems: int
    itemsPerPage: int


class TransactionPaginationResponseDTO(BaseModel):
    """Schema for paginated transaction list response."""

    meta: PaginationMetaDTO
    data: list[TransactionResponseDTO]


class FinancialSummaryDTO(BaseModel):
    """Schema for general financial summary (income, expenses, balance)."""

    total_balance: Decimal
    total_income: Decimal
    total_expenses: Decimal


class CategoryDistributionDTO(BaseModel):
    """Schema for expense distribution by category."""

    category_id: UUID | None
    category_name: str
    total_amount: Decimal
    percentage: float


class IncomeVsExpensesDTO(BaseModel):
    """Schema for monthly income vs expenses comparison."""

    month: str
    income: Decimal
    expenses: Decimal

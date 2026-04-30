from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field


class DailyTipCreate(BaseModel):
    """DTO para crear un consejo diario."""

    title: str = Field(..., min_length=1, max_length=255)
    text: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1, max_length=100)
    day_of_week: int = Field(..., ge=0, le=6, description="0=Lunes, ..., 6=Domingo")


class DailyTipUpdate(BaseModel):
    """DTO para actualizar un consejo diario."""

    title: str | None = Field(None, min_length=1, max_length=255)
    text: str | None = Field(None, min_length=1)
    category: str | None = Field(None, min_length=1, max_length=100)
    is_active: bool | None = None


class DailyTipResponse(BaseModel):
    """DTO para devolver un consejo diario."""

    daily_tip_id: UUID
    title: str
    text: str
    category: str
    day_of_week: int
    generated_at: datetime
    is_active: bool

    class Config:
        from_attributes = True


class DailyTipBatchResponse(BaseModel):
    """DTO para devolver un lote de consejos diarios."""

    tips: list[DailyTipResponse]
    total_count: int
    generated_at: datetime

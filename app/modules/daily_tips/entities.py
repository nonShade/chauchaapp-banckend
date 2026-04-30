"""
Entidades del módulo de consejos diarios.

Tablas:
    - daily_tip: Consejos financieros generados por IA y servidos diariamente (rotativos).
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.base_entity import AuditMixin
from app.shared.database import Base


class DailyTip(Base, AuditMixin):
    """Consejo financiero generado por IA y servido a los usuarios"""

    __tablename__ = "daily_tip"

    daily_tip_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    day_of_week: Mapped[int] = mapped_column(
        Integer, nullable=False, comment="0=Lunes, 1=Martes, ..., 6=Domingo"
    )
    generated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    is_active: Mapped[bool] = mapped_column(
        default=True, nullable=False, comment="Set to False when a new batch is generated"
    )

    def __repr__(self) -> str:
        return f"<DailyTip(day={self.day_of_week}, category={self.category}, title={self.title[:30]})>"

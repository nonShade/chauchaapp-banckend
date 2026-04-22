"""
User module entities.

Tables:
    - income_type: Lookup table for user income types.
    - user: Core user entity with personal and financial information.
"""

import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.base_entity import AuditMixin
from app.shared.database import Base


class IncomeType(Base, AuditMixin):
    """Lookup table for user income classification."""

    __tablename__ = "income_type"

    income_type_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relationships
    users: Mapped[list["User"]] = relationship(back_populates="income_type_rel")


class User(Base, AuditMixin):
    """Core user entity with personal and financial data."""

    __tablename__ = "user"

    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(180), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    income_type_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("income_type.income_type_id"),
        nullable=True,
    )
    monthly_income: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False
    )
    monthly_expenses: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False
    )

    # Relationships
    income_type_rel: Mapped["IncomeType | None"] = relationship(
        back_populates="users"
    )
    family_groups_admin: Mapped[list["FamilyGroup"]] = relationship(
        back_populates="admin",
        foreign_keys="[FamilyGroup.admin_id]",
    )
    group_memberships: Mapped[list["GroupMember"]] = relationship(
        back_populates="user"
    )
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="user"
    )
    user_progress: Mapped[list["UserProgress"]] = relationship(
        back_populates="user"
    )
    quiz_results: Mapped[list["QuizResult"]] = relationship(
        back_populates="user"
    )
    notifications: Mapped[list["Notification"]] = relationship(
        back_populates="user"
    )
    personalized_analyses: Mapped[list["PersonalizedAnalysisNews"]] = relationship(
        back_populates="user"
    )
    user_interests: Mapped[list["UserInterest"]] = relationship(
        back_populates="user"
    )

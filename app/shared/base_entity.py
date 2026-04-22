"""
Base entity mixin providing audit fields for all ORM models.

Every table in ChauchaApp must include created_at, updated_at,
created_by, and updated_by columns as per the project requirements.
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column


class AuditMixin:
    """
    Mixin that adds audit columns to any ORM model.

    Columns:
        created_at: Timestamp of record creation (auto-set).
        updated_at: Timestamp of last update (auto-updated).
        created_by: UUID of the user who created the record (optional).
        updated_by: UUID of the user who last updated the record (optional).
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    created_by: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True,
    )
    updated_by: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        nullable=True,
    )

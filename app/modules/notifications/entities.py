"""
Notifications module entities.

Tables:
    - notification_type: Lookup table for notification types
      (group_join_request, transaction_reminder, etc.).
    - notification_status: Lookup table for notification statuses
      (pending, sent, read, dismissed).
    - notification: User notifications with polymorphic reference support.

Design Notes:
    Notifications support polymorphic references via reference_id + reference_type
    columns, allowing them to link to different source entities:
    - 'group_join_request' → links to group_join_request table
    - 'transaction' → links to transaction table (for reminders)
    - etc.
"""

import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.base_entity import AuditMixin
from app.shared.database import Base


class NotificationType(Base, AuditMixin):
    """
    Lookup table for notification types.

    Values: group_join_request, group_join_accepted, group_join_rejected,
    transaction_reminder, system_info, educational_reminder.
    """

    __tablename__ = "notification_type"

    notification_type_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relationships
    notifications: Mapped[list["Notification"]] = relationship(
        back_populates="notification_type"
    )


class NotificationStatus(Base, AuditMixin):
    """
    Lookup table for notification statuses.

    Values: pending, sent, read, dismissed.
    """

    __tablename__ = "notification_status"

    notification_status_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Relationships
    notifications: Mapped[list["Notification"]] = relationship(
        back_populates="notification_status"
    )


class Notification(Base, AuditMixin):
    """
    User notification.

    Supports polymorphic references to source entities via
    reference_id (UUID of the related record) and
    reference_type (name of the related table/entity).

    Examples:
        - Group join request notification:
          reference_type='group_join_request', reference_id=<group_join_request_id>
        - Transaction reminder:
          reference_type='transaction', reference_id=<transaction_id>
    """

    __tablename__ = "notification"

    notification_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("user.user_id"),
        nullable=False,
    )
    notification_type_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("notification_type.notification_type_id"),
        nullable=False,
    )
    notification_status_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("notification_status.notification_status_id"),
        nullable=False,
    )
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    scheduled_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    reference_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), nullable=True
    )
    reference_type: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="notifications")
    notification_type: Mapped["NotificationType"] = relationship(
        back_populates="notifications"
    )
    notification_status: Mapped["NotificationStatus"] = relationship(
        back_populates="notifications"
    )

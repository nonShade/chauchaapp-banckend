"""
Groups module entities.

Tables:
    - family_group: Family groups with an admin user.
    - group_member: M2M relationship between users and family groups.
    - group_join_request: Tracks requests to join a family group.
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.shared.base_entity import AuditMixin
from app.shared.database import Base


class FamilyGroup(Base, AuditMixin):
    """Family group entity — users can form groups for shared finances."""

    __tablename__ = "family_group"

    family_group_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    admin_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("user.user_id"),
        nullable=False,
    )

    # Relationships
    admin: Mapped["User"] = relationship(
        back_populates="family_groups_admin",
        foreign_keys=[admin_id],
    )
    members: Mapped[list["GroupMember"]] = relationship(
        back_populates="family_group"
    )
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="family_group"
    )
    join_requests: Mapped[list["GroupJoinRequest"]] = relationship(
        back_populates="family_group"
    )


class GroupMember(Base, AuditMixin):
    """Membership record linking a user to a family group."""

    __tablename__ = "group_member"

    group_member_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("user.user_id"),
        nullable=False,
    )
    family_group_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("family_group.family_group_id"),
        nullable=False,
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="group_memberships")
    family_group: Mapped["FamilyGroup"] = relationship(back_populates="members")


class GroupJoinRequest(Base, AuditMixin):
    """
    Tracks requests from users wanting to join a family group.

    Generates a notification of type 'group_join_request' for the group admin.
    """

    __tablename__ = "group_join_request"

    group_join_request_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    family_group_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("family_group.family_group_id"),
        nullable=False,
    )
    requester_user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("user.user_id"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(45), nullable=False, default="pending"
    )
    responded_by: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("user.user_id"),
        nullable=True,
    )
    responded_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )

    # Relationships
    family_group: Mapped["FamilyGroup"] = relationship(
        back_populates="join_requests"
    )
    requester: Mapped["User"] = relationship(
        foreign_keys=[requester_user_id]
    )
    responder: Mapped["User | None"] = relationship(
        foreign_keys=[responded_by]
    )

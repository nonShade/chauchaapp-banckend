"""
Users repository — data access layer.

Abstracts database operations for user profile management.
Must not contain business logic (per backend development rules).
"""

import uuid

from sqlalchemy.orm import Session

from app.modules.news.entities import NewsTag, UserInterest
from app.modules.users.entities import IncomeType, User


class UserRepository:
    """Data access for user profile operations."""

    def __init__(self, session: Session):
        self._session = session

    def get_user_by_id(self, user_id: uuid.UUID) -> User | None:
        """Find a user by their primary key.

        Args:
            user_id: The user's UUID.

        Returns:
            The User entity or None if not found.
        """
        return (
            self._session.query(User)
            .filter(User.user_id == user_id)
            .first()
        )

    def get_user_by_email(self, email: str) -> User | None:
        """Find a user by email address.

        Args:
            email: The email to search for.

        Returns:
            The User entity or None if not found.
        """
        return (
            self._session.query(User)
            .filter(User.email == email)
            .first()
        )

    def get_income_type_by_id(self, income_type_id: uuid.UUID) -> IncomeType | None:
        """Find an income type by its ID.

        Args:
            income_type_id: The income type UUID.

        Returns:
            The IncomeType entity or None if not found.
        """
        return (
            self._session.query(IncomeType)
            .filter(IncomeType.income_type_id == income_type_id)
            .first()
        )

    def get_tags_by_ids(self, tag_ids: list[uuid.UUID]) -> list[NewsTag]:
        """Find news tags matching a list of IDs.

        Args:
            tag_ids: List of tag UUIDs to search for.

        Returns:
            List of matching NewsTag entities.
        """
        return (
            self._session.query(NewsTag)
            .filter(NewsTag.tag_id.in_(tag_ids))
            .all()
        )

    def get_interests_by_user_id(self, user_id: uuid.UUID) -> list[UserInterest]:
        """Retrieve all interest records for a given user.

        Args:
            user_id: The user's UUID.

        Returns:
            List of UserInterest entities.
        """
        return (
            self._session.query(UserInterest)
            .filter(UserInterest.user_id == user_id)
            .all()
        )

    def delete_user_interests(self, user_id: uuid.UUID) -> None:
        """Delete all interest records for a given user.

        Args:
            user_id: The user's UUID.
        """
        self._session.query(UserInterest).filter(
            UserInterest.user_id == user_id
        ).delete(synchronize_session=False)

    def create_user_interests(
        self, user_id: uuid.UUID, tag_ids: list[uuid.UUID]
    ) -> None:
        """Create user interest records linking a user to news tags.

        Args:
            user_id: The user's UUID.
            tag_ids: List of news tag UUIDs.
        """
        for tag_id in tag_ids:
            interest = UserInterest(user_id=user_id, tag_id=tag_id)
            self._session.add(interest)
        self._session.flush()

    def update_user(self, user: User) -> User:
        """Persist changes to an existing user entity.

        Args:
            user: The modified User entity already tracked by the session.

        Returns:
            The updated User entity.
        """
        self._session.flush()
        return user

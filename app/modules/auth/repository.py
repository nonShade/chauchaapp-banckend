"""
Auth repository — data access layer.

Abstracts database operations for authentication workflows.
Must not contain business logic (per backend development rules).
"""

import uuid

from sqlalchemy.orm import Session

from app.modules.news.entities import NewsTag, UserInterest
from app.modules.users.entities import IncomeType, User


class AuthRepository:
    """Data access for authentication operations."""

    def __init__(self, session: Session):
        self._session = session

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

    def create_user(self, user: User) -> User:
        """Persist a new user to the database.

        Args:
            user: The User entity to create.

        Returns:
            The persisted User entity with generated ID.
        """
        self._session.add(user)
        self._session.flush()
        return user

    def get_income_type_by_id(self, income_type_id: uuid.UUID) -> IncomeType | None:
        """Find an income type by its ID.

        Returns:
            The IncomeType entity or None if not found.
        """
        return (
            self._session.query(IncomeType)
            .filter(IncomeType.income_type_id == income_type_id)
            .first()
        )

    def get_news_tags_by_ids(self, tag_ids: list[uuid.UUID]) -> list[NewsTag]:
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

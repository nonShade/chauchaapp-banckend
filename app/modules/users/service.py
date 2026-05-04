"""
Users service — business logic layer.

Contains business logic for user profile retrieval and updates.
Delegates data access to the repository layer.
Must be independent of web framework (per backend development rules).
"""

import uuid

from app.modules.users.dto import UpdateProfileRequestDTO, UserProfileResponseDTO
from app.modules.users.exceptions import (
    EmailAlreadyInUseException,
    InvalidIncomeTypeException,
    InvalidTopicException,
    UserNotFoundException,
)
from app.modules.users.repository import UserRepository


class UserProfileService:
    """Business logic for user profile operations."""

    def __init__(self, repository: UserRepository):
        self._repository = repository

    def get_profile(self, user_id: uuid.UUID) -> UserProfileResponseDTO:
        """Retrieve the full profile of a user by their ID.

        Args:
            user_id: The authenticated user's UUID (extracted from JWT).

        Returns:
            Full user profile including interest topic IDs.

        Raises:
            UserNotFoundException: If no user matches the given ID.
        """
        user = self._repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException()

        interests = self._repository.get_interests_by_user_id(user_id)
        topic_ids = [interest.tag_id for interest in interests]

        return UserProfileResponseDTO(
            id=user.user_id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            birth_date=user.birth_date,
            income_type_id=user.income_type_id,
            monthly_income=user.monthly_income,
            monthly_expenses=user.monthly_expenses,
            topics=topic_ids,
        )

    def update_profile(
        self, user_id: uuid.UUID, dto: UpdateProfileRequestDTO
    ) -> UserProfileResponseDTO:
        """Update the profile of a user.

        Validates business rules before applying changes:
        - Email must not belong to another user.
        - income_type_id must exist in the database.
        - Every topic UUID must exist in the database.
        Replaces all interests with the new list (full replace strategy).

        Args:
            user_id: The authenticated user's UUID (extracted from JWT).
            dto: Update request with the new profile data.

        Returns:
            The updated user profile.

        Raises:
            UserNotFoundException: If no user matches the given ID.
            EmailAlreadyInUseException: If the new email belongs to another user.
            InvalidIncomeTypeException: If income_type_id does not exist.
            InvalidTopicException: If any topic UUID does not exist.
        """
        user = self._repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException()

        # Validate email uniqueness (skip check when email is unchanged)
        if dto.email != user.email:
            existing = self._repository.get_user_by_email(dto.email)
            if existing:
                raise EmailAlreadyInUseException()

        # Validate income type exists
        income_type = self._repository.get_income_type_by_id(dto.income_type_id)
        if not income_type:
            raise InvalidIncomeTypeException()

        # Validate all topic UUIDs exist
        if dto.topics:
            found_tags = self._repository.get_tags_by_ids(dto.topics)
            if len(found_tags) != len(dto.topics):
                raise InvalidTopicException()

        # Apply field updates to the tracked ORM entity
        user.first_name = dto.first_name
        user.last_name = dto.last_name
        user.email = dto.email
        user.birth_date = dto.birth_date
        user.income_type_id = dto.income_type_id
        user.monthly_income = dto.monthly_income
        user.monthly_expenses = dto.monthly_expenses

        self._repository.update_user(user)

        # Replace interests (full replace: delete all then re-insert)
        self._repository.delete_user_interests(user_id)
        if dto.topics:
            self._repository.create_user_interests(user_id, dto.topics)

        return self.get_profile(user_id)

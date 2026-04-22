"""
Unit tests for AuthRepository — tests data access in isolation
with mocked SQLAlchemy session.
"""

from unittest.mock import MagicMock

import pytest

from app.modules.auth.repository import AuthRepository
from app.modules.users.entities import User


@pytest.fixture
def mock_session():
    """Provide a mock SQLAlchemy session."""
    return MagicMock()


@pytest.fixture
def repository(mock_session):
    """Provide an AuthRepository with mocked session."""
    return AuthRepository(mock_session)


class TestGetUserByEmail:
    """Tests for user lookup by email."""

    def test_user_found(self, repository, mock_session):
        """When user exists, return the User entity."""
        mock_user = MagicMock(spec=User)
        mock_user.email = "test@example.com"
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_user
        )

        result = repository.get_user_by_email("test@example.com")

        assert result == mock_user
        mock_session.query.assert_called_once()

    def test_user_not_found(self, repository, mock_session):
        """When user doesn't exist, return None."""
        mock_session.query.return_value.filter.return_value.first.return_value = (
            None
        )

        result = repository.get_user_by_email("noexist@example.com")

        assert result is None


class TestCreateUser:
    """Tests for user creation."""

    def test_create_user_adds_and_flushes(self, repository, mock_session):
        """create_user must add to session and flush."""
        user = MagicMock(spec=User)

        result = repository.create_user(user)

        mock_session.add.assert_called_once_with(user)
        mock_session.flush.assert_called_once()
        assert result == user


class TestGetIncomeTypeByName:
    """Tests for income type lookup."""

    def test_income_type_found(self, repository, mock_session):
        """When income type exists, return it."""
        mock_it = MagicMock()
        mock_it.name = "salaried"
        mock_session.query.return_value.filter.return_value.first.return_value = (
            mock_it
        )

        result = repository.get_income_type_by_name("salaried")

        assert result == mock_it

    def test_income_type_not_found(self, repository, mock_session):
        """When income type doesn't exist, return None."""
        mock_session.query.return_value.filter.return_value.first.return_value = (
            None
        )

        result = repository.get_income_type_by_name("nonexistent")

        assert result is None


class TestCreateUserInterests:
    """Tests for creating user-interest records."""

    def test_creates_interests_for_each_tag(self, repository, mock_session):
        """Must add one interest record per tag ID and flush."""
        import uuid

        tag_ids = [uuid.uuid4(), uuid.uuid4(), uuid.uuid4()]
        user_id = uuid.uuid4()

        repository.create_user_interests(user_id, tag_ids)

        assert mock_session.add.call_count == 3
        mock_session.flush.assert_called_once()

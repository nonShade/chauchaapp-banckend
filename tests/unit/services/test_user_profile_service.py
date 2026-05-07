"""
Unit tests for UserProfileService — tests business logic in isolation
with mocked repository.

Test cases covered:
    CP-P01: Obtención Exitosa del perfil
    CP-P02: Validación de Email duplicado en PUT
    CP-P03: Integridad UUID — income_type_id inválido
    CP-P04: Validación de Tópicos — actualización N:M correcta
    CP-P05: Seguridad — usuario no encontrado (user_id del JWT no existe)
"""

import uuid
from datetime import date, datetime
from decimal import Decimal
from unittest.mock import MagicMock, call

import pytest

from app.modules.news.entities import NewsTag, UserInterest
from app.modules.users.dto import UpdateProfileRequestDTO
from app.modules.users.entities import IncomeType, User
from app.modules.users.exceptions import (
    EmailAlreadyInUseException,
    InvalidIncomeTypeException,
    InvalidTopicException,
    UserNotFoundException,
)
from app.modules.users.service import UserProfileService


@pytest.fixture
def mock_repository():
    """Provide a fully mocked UserRepository."""
    return MagicMock()


@pytest.fixture
def mock_tx_repository():
    """Provide a fully mocked TransactionsRepository."""
    return MagicMock()


@pytest.fixture
def service(mock_repository, mock_tx_repository):
    """Provide a UserProfileService with mocked repositories."""
    return UserProfileService(mock_repository, mock_tx_repository)


@pytest.fixture
def mock_tx_setup(mock_tx_repository):
    """Set up mock transaction repository responses for profile update flow."""
    mock_type = MagicMock()
    mock_type.transaction_type_id = uuid.uuid4()
    mock_category = MagicMock()
    mock_category.transaction_category_id = uuid.uuid4()
    mock_tx = MagicMock()
    mock_tx.amount = Decimal("500000")

    mock_tx_repository.get_transaction_type_by_name.return_value = mock_type
    mock_tx_repository.get_transaction_category_by_name.return_value = mock_category
    mock_tx_repository.get_transaction_by_user_type_category.return_value = mock_tx
    return mock_tx_repository


@pytest.fixture
def user_id():
    """Return a fixed user UUID for tests."""
    return uuid.uuid4()


@pytest.fixture
def sample_user(user_id):
    """Create a mock User entity."""
    user = MagicMock(spec=User)
    user.user_id = user_id
    user.first_name = "Carlos"
    user.last_name = "Lopez"
    user.email = "carlos@example.com"
    user.birth_date = date(1995, 5, 25)
    user.income_type_id = uuid.uuid4()
    user.monthly_income = Decimal("950750")
    user.monthly_expenses = Decimal("450120")
    user.created_at = datetime.now()
    return user


@pytest.fixture
def sample_interests(user_id):
    """Create two mock UserInterest entities."""
    tag_id_1 = uuid.uuid4()
    tag_id_2 = uuid.uuid4()

    interest_1 = MagicMock(spec=UserInterest)
    interest_1.user_id = user_id
    interest_1.tag_id = tag_id_1

    interest_2 = MagicMock(spec=UserInterest)
    interest_2.user_id = user_id
    interest_2.tag_id = tag_id_2

    return [interest_1, interest_2]


@pytest.fixture
def sample_income_type():
    """Create a mock IncomeType entity."""
    it = MagicMock(spec=IncomeType)
    it.income_type_id = uuid.uuid4()
    it.name = "Renta fija"
    return it


@pytest.fixture
def update_dto(sample_income_type):
    """Provide a valid UpdateProfileRequestDTO."""
    return UpdateProfileRequestDTO(
        first_name="Carlos",
        last_name="Lopez",
        email="carlos@example.com",
        birth_date=date(1995, 5, 25),
        income_type_id=sample_income_type.income_type_id,
        monthly_income=Decimal("1200000"),
        monthly_expenses=Decimal("500000"),
        topics=[uuid.uuid4(), uuid.uuid4()],
    )


# -----------------------------------------------------------------------
# CP-P01: Obtención Exitosa del Perfil
# -----------------------------------------------------------------------


class TestGetProfile:
    """Tests for UserProfileService.get_profile()."""

    def test_get_profile_returns_all_fields(
        self, service, mock_repository, user_id, sample_user, sample_interests
    ):
        """CP-P01: Successful profile retrieval returns all fields."""
        mock_repository.get_user_by_id.return_value = sample_user
        mock_repository.get_interests_by_user_id.return_value = sample_interests

        result = service.get_profile(user_id)

        assert result.id == sample_user.user_id
        assert result.first_name == "Carlos"
        assert result.last_name == "Lopez"
        assert result.email == "carlos@example.com"
        assert result.birth_date == date(1995, 5, 25)
        assert result.income_type_id == sample_user.income_type_id
        assert result.monthly_income == Decimal("950750")
        assert result.monthly_expenses == Decimal("450120")

    def test_get_profile_returns_correct_topic_uuids(
        self, service, mock_repository, user_id, sample_user, sample_interests
    ):
        """CP-P01: Profile includes the correct topic UUID list."""
        mock_repository.get_user_by_id.return_value = sample_user
        mock_repository.get_interests_by_user_id.return_value = sample_interests

        result = service.get_profile(user_id)

        expected_topics = [i.tag_id for i in sample_interests]
        assert result.topics == expected_topics
        assert len(result.topics) == 2

    def test_get_profile_user_not_found_raises(
        self, service, mock_repository, user_id
    ):
        """CP-P05: Non-existent user raises UserNotFoundException."""
        mock_repository.get_user_by_id.return_value = None

        with pytest.raises(UserNotFoundException):
            service.get_profile(user_id)

    def test_get_profile_empty_topics(
        self, service, mock_repository, user_id, sample_user
    ):
        """Profile with no interests returns empty topics list."""
        mock_repository.get_user_by_id.return_value = sample_user
        mock_repository.get_interests_by_user_id.return_value = []

        result = service.get_profile(user_id)

        assert result.topics == []


# -----------------------------------------------------------------------
# CP-P02: Validación de Email duplicado
# -----------------------------------------------------------------------


class TestUpdateProfileEmail:
    """Tests for email validation in UserProfileService.update_profile()."""

    def test_update_profile_with_same_email_skips_uniqueness_check(
        self,
        service,
        mock_repository,
        mock_tx_setup,
        user_id,
        sample_user,
        sample_income_type,
        update_dto,
    ):
        """Same email as current user should not trigger uniqueness check."""
        # Update DTO email matches the current user email
        same_email_dto = UpdateProfileRequestDTO(
            first_name=update_dto.first_name,
            last_name=update_dto.last_name,
            email=sample_user.email,  # same email
            birth_date=update_dto.birth_date,
            income_type_id=update_dto.income_type_id,
            monthly_income=update_dto.monthly_income,
            monthly_expenses=update_dto.monthly_expenses,
            topics=update_dto.topics,
        )
        mock_repository.get_user_by_id.return_value = sample_user
        mock_repository.get_income_type_by_id.return_value = sample_income_type
        tags = [MagicMock(spec=NewsTag) for _ in same_email_dto.topics]
        mock_repository.get_tags_by_ids.return_value = tags
        mock_repository.get_interests_by_user_id.return_value = []

        # Should NOT raise
        service.update_profile(user_id, same_email_dto)

        mock_repository.get_user_by_email.assert_not_called()

    def test_update_profile_duplicate_email_raises(
        self,
        service,
        mock_repository,
        user_id,
        sample_user,
        update_dto,
    ):
        """CP-P02: New email already belonging to another user raises EmailAlreadyInUseException."""
        new_email_dto = UpdateProfileRequestDTO(
            first_name=update_dto.first_name,
            last_name=update_dto.last_name,
            email="other@example.com",  # different from current
            birth_date=update_dto.birth_date,
            income_type_id=update_dto.income_type_id,
            monthly_income=update_dto.monthly_income,
            monthly_expenses=update_dto.monthly_expenses,
            topics=update_dto.topics,
        )
        mock_repository.get_user_by_id.return_value = sample_user
        # Another user already has this email
        mock_repository.get_user_by_email.return_value = MagicMock(spec=User)

        with pytest.raises(EmailAlreadyInUseException):
            service.update_profile(user_id, new_email_dto)


# -----------------------------------------------------------------------
# CP-P03: Integridad UUID — income_type_id
# -----------------------------------------------------------------------


class TestUpdateProfileIncomeType:
    """Tests for income type validation in UserProfileService.update_profile()."""

    def test_update_profile_invalid_income_type_raises(
        self, service, mock_repository, user_id, sample_user, update_dto
    ):
        """CP-P03: Non-existent income_type_id raises InvalidIncomeTypeException."""
        mock_repository.get_user_by_id.return_value = sample_user
        mock_repository.get_user_by_email.return_value = None
        mock_repository.get_income_type_by_id.return_value = None  # does not exist

        with pytest.raises(InvalidIncomeTypeException):
            service.update_profile(user_id, update_dto)


# -----------------------------------------------------------------------
# CP-P04: Validación de Tópicos — actualización N:M
# -----------------------------------------------------------------------


class TestUpdateProfileTopics:
    """Tests for topic validation and N:M update in UserProfileService.update_profile()."""

    def test_update_profile_invalid_topic_raises(
        self,
        service,
        mock_repository,
        user_id,
        sample_user,
        sample_income_type,
        update_dto,
    ):
        """CP-P04: Topic UUID that does not exist raises InvalidTopicException."""
        mock_repository.get_user_by_id.return_value = sample_user
        mock_repository.get_user_by_email.return_value = None
        mock_repository.get_income_type_by_id.return_value = sample_income_type
        # Only 1 tag found, but 2 were requested → mismatch
        mock_repository.get_tags_by_ids.return_value = [MagicMock(spec=NewsTag)]

        with pytest.raises(InvalidTopicException):
            service.update_profile(user_id, update_dto)

    def test_update_profile_replaces_interests(
        self,
        service,
        mock_repository,
        mock_tx_setup,
        user_id,
        sample_user,
        sample_income_type,
        update_dto,
    ):
        """CP-P04: Interests are fully replaced (delete then insert) on update."""
        mock_repository.get_user_by_id.return_value = sample_user
        mock_repository.get_user_by_email.return_value = None
        mock_repository.get_income_type_by_id.return_value = sample_income_type
        tags = [MagicMock(spec=NewsTag) for _ in update_dto.topics]
        mock_repository.get_tags_by_ids.return_value = tags
        mock_repository.get_interests_by_user_id.return_value = []

        service.update_profile(user_id, update_dto)

        mock_repository.delete_user_interests.assert_called_once_with(user_id)
        mock_repository.create_user_interests.assert_called_once_with(
            user_id, update_dto.topics
        )

    def test_update_profile_updates_financial_fields(
        self,
        service,
        mock_repository,
        mock_tx_setup,
        user_id,
        sample_user,
        sample_income_type,
        update_dto,
    ):
        """Monthly income and expenses are correctly updated on the user entity."""
        mock_repository.get_user_by_id.return_value = sample_user
        mock_repository.get_user_by_email.return_value = None
        mock_repository.get_income_type_by_id.return_value = sample_income_type
        tags = [MagicMock(spec=NewsTag) for _ in update_dto.topics]
        mock_repository.get_tags_by_ids.return_value = tags
        mock_repository.get_interests_by_user_id.return_value = []

        service.update_profile(user_id, update_dto)

        assert sample_user.monthly_income == update_dto.monthly_income
        assert sample_user.monthly_expenses == update_dto.monthly_expenses


# -----------------------------------------------------------------------
# CP-P05: Seguridad JWT — user_id inválido
# -----------------------------------------------------------------------


class TestUpdateProfileSecurity:
    """Tests for security enforcement in UserProfileService.update_profile()."""

    def test_update_profile_user_not_found_raises(
        self, service, mock_repository, user_id, update_dto
    ):
        """CP-P05: Non-existent user_id raises UserNotFoundException."""
        mock_repository.get_user_by_id.return_value = None

        with pytest.raises(UserNotFoundException):
            service.update_profile(user_id, update_dto)

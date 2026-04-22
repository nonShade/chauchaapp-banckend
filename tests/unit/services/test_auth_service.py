"""
Unit tests for AuthService — tests business logic in isolation
with mocked repository.

Test cases covered:
    CP-001: Login exitoso
    CP-002: Credenciales incorrectas
    CP-005: Registro exitoso
    CP-006: Email duplicado
    + Invalid income type, logout
"""

import uuid
from datetime import date, datetime
from decimal import Decimal
from unittest.mock import MagicMock

import pytest

from app.modules.auth.dto import LoginRequestDTO, RegisterRequestDTO
from app.modules.auth.exceptions import (
    EmailAlreadyExistsException,
    InvalidCredentialsException,
    InvalidIncomeTypeException,
)
from app.modules.auth.service import AuthService
from app.modules.news.entities import NewsTag
from app.modules.users.entities import IncomeType, User
from app.shared.security.password import hash_password


@pytest.fixture
def mock_repository():
    """Provide a fully mocked AuthRepository."""
    return MagicMock()


@pytest.fixture
def service(mock_repository):
    """Provide an AuthService with mocked repository."""
    return AuthService(mock_repository)


@pytest.fixture
def sample_user():
    """Create a mock User with a hashed password."""
    user = MagicMock(spec=User)
    user.user_id = uuid.uuid4()
    user.email = "test@example.com"
    user.password = hash_password("TestPass123!")
    user.first_name = "Test"
    user.last_name = "User"
    user.created_at = datetime.now()
    return user


@pytest.fixture
def register_dto():
    """Provide a valid RegisterRequestDTO."""
    return RegisterRequestDTO(
        first_name="Carlos",
        last_name="Lopez",
        email="carlos@example.com",
        password="Passw0rd",
        birth_date=date(1995, 5, 25),
        income_type=uuid.uuid4(),
        monthly_income=Decimal("950750"),
        monthly_expenses=Decimal("450120"),
        topics=[uuid.uuid4(), uuid.uuid4()],
    )


# -----------------------------------------------------------------------
# Login Tests
# -----------------------------------------------------------------------


class TestLogin:
    """Tests for AuthService.login()."""

    def test_login_success_returns_tokens(self, service, mock_repository, sample_user):
        """CP-001: Successful login returns access & refresh tokens."""
        mock_repository.get_user_by_email.return_value = sample_user

        dto = LoginRequestDTO(email="test@example.com", password="TestPass123!")
        result = service.login(dto)

        assert result.access_token is not None
        assert result.refresh_token is not None
        assert result.token_type == "Bearer"
        assert result.expires_in > 0
        assert result.message == "Inicio de sesión exitoso"

    def test_login_success_returns_user_data(
        self, service, mock_repository, sample_user
    ):
        """CP-001: Response includes correct user data."""
        mock_repository.get_user_by_email.return_value = sample_user

        dto = LoginRequestDTO(email="test@example.com", password="TestPass123!")
        result = service.login(dto)

        assert result.user.email == "test@example.com"
        assert result.user.first_name == "Test"
        assert result.user.last_name == "User"
        assert result.user.id == sample_user.user_id

    def test_login_wrong_password_raises(
        self, service, mock_repository, sample_user
    ):
        """CP-002: Wrong password raises InvalidCredentialsException."""
        mock_repository.get_user_by_email.return_value = sample_user

        dto = LoginRequestDTO(email="test@example.com", password="WrongPassword")
        with pytest.raises(InvalidCredentialsException):
            service.login(dto)

    def test_login_user_not_found_raises(self, service, mock_repository):
        """CP-002: Non-existent user raises InvalidCredentialsException."""
        mock_repository.get_user_by_email.return_value = None

        dto = LoginRequestDTO(email="noexist@example.com", password="TestPass123!")
        with pytest.raises(InvalidCredentialsException):
            service.login(dto)


# -----------------------------------------------------------------------
# Register Tests
# -----------------------------------------------------------------------


class TestRegister:
    """Tests for AuthService.register()."""

    @pytest.fixture
    def mock_income_type(self):
        """Provide a mock IncomeType entity."""
        it = MagicMock(spec=IncomeType)
        it.income_type_id = uuid.uuid4()
        it.name = "salaried"
        return it

    def test_register_success(
        self, service, mock_repository, register_dto, mock_income_type
    ):
        """CP-005: Successful registration returns user confirmation."""
        mock_repository.get_user_by_email.return_value = None
        mock_repository.get_income_type_by_id.return_value = mock_income_type

        created_user = MagicMock(spec=User)
        created_user.user_id = uuid.uuid4()
        created_user.first_name = "Carlos"
        created_user.last_name = "Lopez"
        created_user.email = "carlos@example.com"
        created_user.created_at = datetime.now()
        mock_repository.create_user.return_value = created_user

        tag = MagicMock(spec=NewsTag)
        tag.tag_id = uuid.uuid4()
        mock_repository.get_news_tags_by_ids.return_value = [tag]

        result = service.register(register_dto)

        assert result.message == "Usuario creado correctamente"
        assert result.user.email == "carlos@example.com"
        assert result.user.first_name == "Carlos"
        mock_repository.create_user.assert_called_once()
        mock_repository.create_user_interests.assert_called_once()

    def test_register_hashes_password(
        self, service, mock_repository, register_dto, mock_income_type
    ):
        """Password must be hashed before storing."""
        mock_repository.get_user_by_email.return_value = None
        mock_repository.get_income_type_by_id.return_value = mock_income_type

        created_user = MagicMock(spec=User)
        created_user.user_id = uuid.uuid4()
        created_user.first_name = "Carlos"
        created_user.last_name = "Lopez"
        created_user.email = "carlos@example.com"
        created_user.created_at = datetime.now()
        mock_repository.create_user.return_value = created_user
        mock_repository.get_news_tags_by_ids.return_value = []

        service.register(register_dto)

        # Get the User passed to create_user
        call_args = mock_repository.create_user.call_args
        user_arg = call_args[0][0]
        assert user_arg.password != "Passw0rd"  # Must be hashed
        assert user_arg.password.startswith("$2b$")

    def test_register_duplicate_email_raises(
        self, service, mock_repository, register_dto
    ):
        """CP-006: Duplicate email raises EmailAlreadyExistsException."""
        mock_repository.get_user_by_email.return_value = MagicMock(spec=User)

        with pytest.raises(EmailAlreadyExistsException):
            service.register(register_dto)

    def test_register_invalid_income_type_raises(
        self, service, mock_repository, register_dto
    ):
        """Invalid income type raises InvalidIncomeTypeException."""
        mock_repository.get_user_by_email.return_value = None
        mock_repository.get_income_type_by_id.return_value = None

        with pytest.raises(InvalidIncomeTypeException):
            service.register(register_dto)


# -----------------------------------------------------------------------
# Logout Tests
# -----------------------------------------------------------------------


class TestLogout:
    """Tests for AuthService.logout()."""

    def test_logout_success(self, service):
        """Logout with valid token returns success message."""
        from app.shared.security.jwt_handler import create_access_token

        token, _, _ = create_access_token("test-id", "test@example.com")

        result = service.logout(token)

        assert result.message == "Cierre de sesión exitoso"

    def test_logout_blacklists_token(self, service):
        """After logout, the token JTI must be in the blacklist."""
        from app.shared.security.jwt_handler import create_access_token, decode_token
        from app.shared.security.token_blacklist import token_blacklist

        token, jti, _ = create_access_token("test-id", "test@example.com")

        service.logout(token)

        assert token_blacklist.is_blacklisted(jti) is True

    def test_logout_invalid_token_raises(self, service):
        """Logout with invalid token raises ValueError."""
        with pytest.raises(ValueError):
            service.logout("not-a-valid-jwt")

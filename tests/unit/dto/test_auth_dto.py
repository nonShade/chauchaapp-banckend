"""
Unit tests for Auth DTOs — validates Pydantic models enforce
business rules at the input layer.

Test cases:
    CP-003: Empty fields → validation error
    CP-007: Invalid age → validation error
    CP-008: Empty fields → validation error
    + Password too short, income too low, no topics
"""

from datetime import date
from decimal import Decimal
import uuid

import pytest
from pydantic import ValidationError

from app.modules.auth.dto import LoginRequestDTO, RegisterRequestDTO


# -----------------------------------------------------------------------
# LoginRequestDTO Tests
# -----------------------------------------------------------------------


class TestLoginRequestDTO:
    """Tests for login request validation."""

    def test_valid_login(self):
        """CP-001 precondition: valid email and password are accepted."""
        dto = LoginRequestDTO(email="test@example.com", password="password123")
        assert dto.email == "test@example.com"
        assert dto.password == "password123"

    def test_invalid_email_format(self):
        """Email must be a valid email format."""
        with pytest.raises(ValidationError):
            LoginRequestDTO(email="not-an-email", password="password123")

    def test_empty_password_rejected(self):
        """CP-003: Empty password must be rejected."""
        with pytest.raises(ValidationError, match="requerida"):
            LoginRequestDTO(email="test@example.com", password="")

    def test_whitespace_only_password_rejected(self):
        """Whitespace-only password must be rejected."""
        with pytest.raises(ValidationError, match="requerida"):
            LoginRequestDTO(email="test@example.com", password="   ")

    def test_missing_email_rejected(self):
        """CP-008: Missing email must be rejected."""
        with pytest.raises(ValidationError):
            LoginRequestDTO(password="password123")

    def test_missing_password_rejected(self):
        """CP-008: Missing password must be rejected."""
        with pytest.raises(ValidationError):
            LoginRequestDTO(email="test@example.com")


# -----------------------------------------------------------------------
# RegisterRequestDTO Tests
# -----------------------------------------------------------------------


class TestRegisterRequestDTO:
    """Tests for registration request validation."""

    @pytest.fixture
    def valid_data(self):
        """Provide valid registration data as a baseline."""
        return {
            "first_name": "Carlos",
            "last_name": "Lopez",
            "email": "carlos@example.com",
            "password": "Passw0rd",
            "birth_date": date(1995, 5, 25),
            "income_type": uuid.uuid4(),
            "monthly_income": Decimal("950750"),
            "monthly_expenses": Decimal("450120"),
            "topics": [uuid.uuid4(), uuid.uuid4()],
        }

    def test_valid_registration(self, valid_data):
        """CP-005 precondition: valid data is accepted."""
        dto = RegisterRequestDTO(**valid_data)
        assert dto.first_name == "Carlos"
        assert dto.last_name == "Lopez"
        assert dto.email == "carlos@example.com"
        assert len(dto.topics) == 2

    def test_password_too_short(self, valid_data):
        """Password must be at least 6 characters."""
        valid_data["password"] = "12345"
        with pytest.raises(ValidationError, match="6 caracteres"):
            RegisterRequestDTO(**valid_data)

    def test_password_exactly_6_chars_accepted(self, valid_data):
        """Boundary: exactly 6 characters should be accepted."""
        valid_data["password"] = "123456"
        dto = RegisterRequestDTO(**valid_data)
        assert dto.password == "123456"

    def test_age_under_18_rejected(self, valid_data):
        """CP-007: Age under 18 must be rejected."""
        valid_data["birth_date"] = date(2015, 5, 25)
        with pytest.raises(ValidationError, match="18 y 50"):
            RegisterRequestDTO(**valid_data)

    def test_age_over_50_rejected(self, valid_data):
        """CP-007: Age over 50 must be rejected."""
        valid_data["birth_date"] = date(1970, 1, 1)
        with pytest.raises(ValidationError, match="18 y 50"):
            RegisterRequestDTO(**valid_data)

    def test_age_exactly_18_accepted(self, valid_data):
        """Boundary: exactly 18 years old should be accepted."""
        today = date.today()
        birth_18 = date(today.year - 18, today.month, today.day)
        valid_data["birth_date"] = birth_18
        dto = RegisterRequestDTO(**valid_data)
        assert dto.birth_date == birth_18

    def test_age_exactly_50_accepted(self, valid_data):
        """Boundary: exactly 50 years old should be accepted."""
        today = date.today()
        birth_50 = date(today.year - 50, today.month, today.day)
        valid_data["birth_date"] = birth_50
        dto = RegisterRequestDTO(**valid_data)
        assert dto.birth_date == birth_50

    def test_income_too_low(self, valid_data):
        """Monthly income must be greater than 5000."""
        valid_data["monthly_income"] = Decimal("3000")
        with pytest.raises(ValidationError, match="5000"):
            RegisterRequestDTO(**valid_data)

    def test_income_exactly_5000_rejected(self, valid_data):
        """Boundary: income of exactly 5000 is NOT accepted (must be >5000)."""
        valid_data["monthly_income"] = Decimal("5000")
        with pytest.raises(ValidationError, match="5000"):
            RegisterRequestDTO(**valid_data)

    def test_income_5001_accepted(self, valid_data):
        """Boundary: income of 5001 should be accepted."""
        valid_data["monthly_income"] = Decimal("5001")
        dto = RegisterRequestDTO(**valid_data)
        assert dto.monthly_income == Decimal("5001")

    def test_no_topics_rejected(self, valid_data):
        """At least one topic must be selected."""
        valid_data["topics"] = []
        with pytest.raises(ValidationError, match="tópico"):
            RegisterRequestDTO(**valid_data)

    def test_single_topic_accepted(self, valid_data):
        """One topic should be sufficient."""
        valid_data["topics"] = [uuid.uuid4()]
        dto = RegisterRequestDTO(**valid_data)
        assert len(dto.topics) == 1

    def test_invalid_email_rejected(self, valid_data):
        """Invalid email format must be rejected."""
        valid_data["email"] = "not-an-email"
        with pytest.raises(ValidationError):
            RegisterRequestDTO(**valid_data)

    def test_empty_first_name_rejected(self, valid_data):
        """First name cannot be empty."""
        valid_data["first_name"] = ""
        with pytest.raises(ValidationError, match="nombre"):
            RegisterRequestDTO(**valid_data)

    def test_empty_last_name_rejected(self, valid_data):
        """Last name cannot be empty."""
        valid_data["last_name"] = ""
        with pytest.raises(ValidationError, match="nombre"):
            RegisterRequestDTO(**valid_data)

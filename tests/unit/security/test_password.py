"""
Unit tests for password hashing utilities.
"""

from app.shared.security.password import hash_password, verify_password


class TestHashPassword:
    """Tests for password hashing."""

    def test_hash_returns_bcrypt_string(self):
        """Hashed password must be a bcrypt hash string."""
        hashed = hash_password("TestPass123!")
        assert isinstance(hashed, str)
        assert hashed.startswith("$2b$")

    def test_hash_is_not_plaintext(self):
        """Hashed password must not equal the plain text."""
        plain = "TestPass123!"
        hashed = hash_password(plain)
        assert hashed != plain

    def test_different_hashes_for_same_password(self):
        """Each hash should be unique due to random salt."""
        hash1 = hash_password("TestPass123!")
        hash2 = hash_password("TestPass123!")
        assert hash1 != hash2


class TestVerifyPassword:
    """Tests for password verification."""

    def test_correct_password_verifies(self):
        """Correct password must verify successfully."""
        hashed = hash_password("TestPass123!")
        assert verify_password("TestPass123!", hashed) is True

    def test_wrong_password_fails(self):
        """Wrong password must fail verification."""
        hashed = hash_password("TestPass123!")
        assert verify_password("WrongPassword", hashed) is False

    def test_empty_password_fails(self):
        """Empty password must fail against a real hash."""
        hashed = hash_password("TestPass123!")
        assert verify_password("", hashed) is False

"""
Unit tests for JWT token handler.
"""

import os

import pytest

# Ensure test JWT config is set
os.environ.setdefault("JWT_SECRET", "test_jwt_secret_for_testing")
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("JWT_EXPIRE_MINUTES", "30")

from app.shared.security.jwt_handler import (
    create_access_token,
    create_refresh_token,
    decode_token,
)


class TestCreateAccessToken:
    """Tests for access token creation."""

    def test_returns_token_jti_and_expiry(self):
        """Must return a 3-tuple: (token, jti, expires_in_seconds)."""
        token, jti, expires_in = create_access_token("user-id-123", "test@example.com")
        assert isinstance(token, str)
        assert isinstance(jti, str)
        assert expires_in == 30 * 60  # 30 minutes in seconds

    def test_token_is_decodable(self):
        """Created token must be decodable with our decode function."""
        token, jti, _ = create_access_token("user-id-123", "test@example.com")
        payload = decode_token(token)
        assert payload["sub"] == "user-id-123"
        assert payload["email"] == "test@example.com"
        assert payload["type"] == "access"
        assert payload["jti"] == jti


class TestCreateRefreshToken:
    """Tests for refresh token creation."""

    def test_returns_token_and_jti(self):
        """Must return a 2-tuple: (token, jti)."""
        token, jti = create_refresh_token("user-id-123")
        assert isinstance(token, str)
        assert isinstance(jti, str)

    def test_refresh_token_type(self):
        """Refresh token payload must have type='refresh'."""
        token, _ = create_refresh_token("user-id-123")
        payload = decode_token(token)
        assert payload["type"] == "refresh"
        assert payload["sub"] == "user-id-123"


class TestDecodeToken:
    """Tests for token decoding and validation."""

    def test_decode_valid_access_token(self):
        """Valid access token must decode successfully."""
        token, jti, _ = create_access_token("user-id-123", "test@example.com")
        payload = decode_token(token)
        assert payload["sub"] == "user-id-123"
        assert payload["email"] == "test@example.com"
        assert payload["jti"] == jti

    def test_decode_invalid_token_raises(self):
        """Invalid token string must raise ValueError."""
        with pytest.raises(ValueError, match="inválido"):
            decode_token("this-is-not-a-jwt")

    def test_decode_tampered_token_raises(self):
        """Tampered token must raise ValueError."""
        token, _, _ = create_access_token("user-id-123", "test@example.com")
        tampered = token[:-5] + "XXXXX"
        with pytest.raises(ValueError):
            decode_token(tampered)

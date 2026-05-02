"""
JWT token creation and validation.

Uses PyJWT to create access and refresh tokens with JTI claims
for blacklist support. Configuration is read from environment variables.
"""

import os
import uuid
from datetime import datetime, timedelta, timezone

import jwt
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET: str = os.getenv(
    "JWT_SECRET", "dev_jwt_secret_change_in_production")
JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES: int = int(os.getenv("JWT_EXPIRE_MINUTES", "30"))
JWT_REFRESH_EXPIRE_DAYS: int = 7


def create_access_token(user_id: str, email: str, first_name: str = None, last_name: str = None) -> tuple[str, str, int]:
    """Create a JWT access token.

    Args:
        user_id: The user's UUID as a string.
        email: The user's email address.
        first_name: The user's first name.
        last_name: The user's last name.

    Returns:
        A tuple of (token_string, jti, expires_in_seconds).
    """
    jti = str(uuid.uuid4())
    expires_in = JWT_EXPIRE_MINUTES * 60
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)

    payload = {
        "sub": user_id,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "jti": jti,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access",
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token, jti, expires_in


def create_refresh_token(user_id: str) -> tuple[str, str]:
    """Create a JWT refresh token.

    Args:
        user_id: The user's UUID as a string.

    Returns:
        A tuple of (token_string, jti).
    """
    jti = str(uuid.uuid4())
    expire = datetime.now(timezone.utc) + \
        timedelta(days=JWT_REFRESH_EXPIRE_DAYS)

    payload = {
        "sub": user_id,
        "jti": jti,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "refresh",
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token, jti


def decode_token(token: str) -> dict:
    """Decode and validate a JWT token.

    Args:
        token: The JWT string to decode.

    Returns:
        The decoded payload dictionary.

    Raises:
        ValueError: If the token is expired or invalid.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expirado")
    except jwt.InvalidTokenError:
        raise ValueError("Token inválido")

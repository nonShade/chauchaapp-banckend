"""
Authentication middleware — FastAPI dependency for protected endpoints.

Extracts Bearer token from the Authorization header, validates it,
checks the blacklist, and returns the authenticated user.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.modules.users.entities import User
from app.shared.database import get_db
from app.shared.security.jwt_handler import decode_token
from app.shared.security.token_blacklist import token_blacklist

security_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> User:
    """FastAPI dependency that extracts and validates the current user.

    Args:
        credentials: The Bearer token from the Authorization header.
        db: The database session.

    Returns:
        The authenticated User entity.

    Raises:
        HTTPException: 401 if the token is invalid, expired, blacklisted,
                       or the user is not found.
    """
    token = credentials.credentials

    try:
        payload = decode_token(token)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )

    # Check if token has been blacklisted (logged out)
    jti = payload.get("jti")
    if jti and token_blacklist.is_blacklisted(jti):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalidado",
        )

    # Find user in database
    user_id = payload.get("sub")
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
        )

    return user

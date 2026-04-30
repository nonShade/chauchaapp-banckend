"""
Users controller — HTTP endpoint layer.

Handles HTTP requests/responses, input validation via DTOs, and
delegates to the user profile service. Maps exceptions to HTTP status codes.
Must not contain business logic (per backend development rules).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.modules.users.dto import (
    ErrorResponseDTO,
    UpdateProfileRequestDTO,
    UserProfileResponseDTO,
)
from app.modules.users.exceptions import (
    EmailAlreadyInUseException,
    InvalidIncomeTypeException,
    InvalidTopicException,
    UserNotFoundException,
)
from app.modules.users.entities import User
from app.modules.users.repository import UserRepository
from app.modules.users.service import UserProfileService
from app.shared.database import get_db
from app.shared.security.auth_middleware import get_current_user

router = APIRouter(prefix="/v1/users", tags=["Users"])


def _get_user_service(db: Session = Depends(get_db)) -> UserProfileService:
    """FastAPI dependency that builds the user profile service with its repository."""
    repository = UserRepository(db)
    return UserProfileService(repository)


@router.get(
    "/profile",
    response_model=UserProfileResponseDTO,
    responses={
        401: {"model": ErrorResponseDTO},
        404: {"model": ErrorResponseDTO},
    },
    summary="Ver perfil de usuario",
    description="Retorna el perfil completo del usuario autenticado.",
)
def get_profile(
    current_user: User = Depends(get_current_user),
    service: UserProfileService = Depends(_get_user_service),
):
    """Retrieve the authenticated user's full profile."""
    try:
        return service.get_profile(current_user.user_id)
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )


@router.put(
    "/profile",
    response_model=UserProfileResponseDTO,
    responses={
        400: {"model": ErrorResponseDTO},
        401: {"model": ErrorResponseDTO},
        404: {"model": ErrorResponseDTO},
        409: {"model": ErrorResponseDTO},
    },
    summary="Editar perfil de usuario",
    description="Actualiza el perfil del usuario autenticado.",
)
def update_profile(
    dto: UpdateProfileRequestDTO,
    current_user: User = Depends(get_current_user),
    service: UserProfileService = Depends(_get_user_service),
    db: Session = Depends(get_db),
):
    """Update the authenticated user's profile."""
    try:
        result = service.update_profile(current_user.user_id, dto)
        db.commit()
        return result
    except EmailAlreadyInUseException:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El correo ya está registrado por otro usuario",
        )
    except (InvalidIncomeTypeException, InvalidTopicException) as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    except UserNotFoundException:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error interno. Intente más tarde.",
        )

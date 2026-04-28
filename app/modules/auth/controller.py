"""
Auth controller — HTTP endpoint layer.

Handles HTTP requests/responses, input validation via DTOs, and
delegates to the auth service. Maps exceptions to HTTP status codes.
Must not contain business logic (per backend development rules).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.modules.auth.dto import (
    ErrorResponseDTO,
    LoginRequestDTO,
    LoginResponseDTO,
    LogoutResponseDTO,
    RegisterRequestDTO,
    RegisterResponseDTO,
    VerifyEmailRequestDTO,
    VerifyEmailResponseDTO,
)
from app.modules.auth.exceptions import (
    EmailAlreadyExistsException,
    InvalidCredentialsException,
    InvalidIncomeTypeException,
)
from app.modules.auth.repository import AuthRepository
from app.modules.auth.service import AuthService
from app.shared.database import get_db
from app.shared.exceptions import ValidationException

router = APIRouter(prefix="/v1/auth", tags=["Authentication"])
security = HTTPBearer()


def _get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    """FastAPI dependency that builds the auth service with its repository."""
    repository = AuthRepository(db)
    return AuthService(repository)


@router.post(
    "/login",
    response_model=LoginResponseDTO,
    responses={
        400: {"model": ErrorResponseDTO},
        401: {"model": ErrorResponseDTO},
    },
    summary="Iniciar sesión",
    description="Autentica un usuario y devuelve tokens JWT.",
)
def login(
    dto: LoginRequestDTO,
    service: AuthService = Depends(_get_auth_service),
):
    """Authenticate a user with email and password."""
    try:
        return service.login(dto)
    except InvalidCredentialsException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )


@router.post(
    "/register",
    response_model=RegisterResponseDTO,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponseDTO},
        409: {"model": ErrorResponseDTO},
    },
    summary="Registrar usuario",
    description="Crea un nuevo usuario en el sistema.",
)
def register(
    dto: RegisterRequestDTO,
    service: AuthService = Depends(_get_auth_service),
    db: Session = Depends(get_db),
):
    """Register a new user account."""
    try:
        result = service.register(dto)
        db.commit()
        return result
    except EmailAlreadyExistsException:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Usuario ya registrado.",
        )
    except (ValidationException, InvalidIncomeTypeException) as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocurrió un error interno. Intente más tarde.",
        )


@router.post(
    "/logout",
    response_model=LogoutResponseDTO,
    responses={
        401: {"model": ErrorResponseDTO},
    },
    summary="Cerrar sesión",
    description="Cierra la sesión del usuario e invalida sus tokens.",
)
def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    service: AuthService = Depends(_get_auth_service),
):
    """Invalidate the current session by blacklisting the JWT."""
    try:
        return service.logout(credentials.credentials)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autenticado",
        )


@router.post(
    "/verify-email",
    response_model=VerifyEmailResponseDTO,
    summary="Verificar disponibilidad de correo",
    description="Comprueba si un correo electrónico ya existe en la base de datos.",
)
def verify_email(
    dto: VerifyEmailRequestDTO,
    service: AuthService = Depends(_get_auth_service),
):
    """Check if an email is already registered."""
    return service.verify_email(dto.email)

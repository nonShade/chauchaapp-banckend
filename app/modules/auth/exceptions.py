"""
Auth-specific exceptions.

These extend the shared exception hierarchy and are caught
by the controller to return appropriate HTTP status codes.
"""

from app.shared.exceptions import (
    ConflictException,
    UnauthorizedException,
    ValidationException,
)


class InvalidCredentialsException(UnauthorizedException):
    """Raised when email/password combination is incorrect."""

    def __init__(self):
        super().__init__(message="Credenciales inválidas")


class EmailAlreadyExistsException(ConflictException):
    """Raised when trying to register with an already-used email."""

    def __init__(self):
        super().__init__(message="Usuario ya registrado.")


class InvalidAgeException(ValidationException):
    """Raised when user age is outside the 18-50 range."""

    def __init__(self):
        super().__init__(message="La edad debe estar entre 18 y 50 años")


class InsufficientIncomeException(ValidationException):
    """Raised when monthly income does not meet the minimum threshold."""

    def __init__(self):
        super().__init__(message="El ingreso mensual debe ser mayor a 5000")


class NoTopicsSelectedException(ValidationException):
    """Raised when no interest topics are provided during registration."""

    def __init__(self):
        super().__init__(message="Debe seleccionar al menos un tópico")


class InvalidIncomeTypeException(ValidationException):
    """Raised when the provided income type does not exist in the database."""

    def __init__(self):
        super().__init__(message="Tipo de ingreso no válido")

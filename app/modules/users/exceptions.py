"""
Users-specific exceptions.

These extend the shared exception hierarchy and are caught
by the controller to return appropriate HTTP status codes.
"""

from app.shared.exceptions import (
    ConflictException,
    NotFoundException,
    ValidationException,
)


class UserNotFoundException(NotFoundException):
    """Raised when a user cannot be found by their ID."""

    def __init__(self):
        super().__init__(message="Usuario no encontrado")


class EmailAlreadyInUseException(ConflictException):
    """Raised when trying to update to an email that belongs to another user."""

    def __init__(self):
        super().__init__(message="El correo ya está registrado por otro usuario")


class InvalidIncomeTypeException(ValidationException):
    """Raised when the provided income_type_id does not exist in the database."""

    def __init__(self):
        super().__init__(message="Tipo de ingreso no válido")


class InvalidTopicException(ValidationException):
    """Raised when one or more topic UUIDs do not exist in the database."""

    def __init__(self):
        super().__init__(message="Uno o más tópicos de interés no son válidos")

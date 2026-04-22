"""
Shared exception hierarchy for ChauchaApp.

All custom exceptions inherit from AppException. Controllers map these
to HTTP status codes via the global exception handler in main.py.
"""


class AppException(Exception):
    """Base exception for all application errors."""

    def __init__(self, message: str, code: str = "INTERNAL_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class ValidationException(AppException):
    """Raised when input data fails business-rule validation."""

    def __init__(self, message: str):
        super().__init__(message=message, code="VALIDATION_ERROR")


class NotFoundException(AppException):
    """Raised when a requested resource does not exist."""

    def __init__(self, message: str):
        super().__init__(message=message, code="NOT_FOUND")


class ConflictException(AppException):
    """Raised when an operation conflicts with existing state (e.g., duplicates)."""

    def __init__(self, message: str):
        super().__init__(message=message, code="CONFLICT")


class UnauthorizedException(AppException):
    """Raised when authentication fails or is missing."""

    def __init__(self, message: str = "Usuario no autenticado"):
        super().__init__(message=message, code="UNAUTHORIZED")

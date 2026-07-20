"""Custom application exceptions."""


class DisasterMissingPersonsException(Exception):
    """Base application exception."""

    pass


class AuthenticationError(DisasterMissingPersonsException):
    """Authentication-related errors."""

    pass


class AuthorizationError(DisasterMissingPersonsException):
    """Authorization-related errors."""

    pass


class ResourceNotFoundError(DisasterMissingPersonsException):
    """Resource not found errors."""

    pass


class ValidationError(DisasterMissingPersonsException):
    """Data validation errors."""

    pass


class DuplicateResourceError(DisasterMissingPersonsException):
    """Duplicate resource errors."""

    pass

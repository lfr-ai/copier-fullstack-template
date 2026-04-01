"""Base exception hierarchy for the domain layer."""


class DomainError(Exception):
    """Base exception for all domain errors.

    Domain-specific exceptions inherit from 'DomainError'
    so boundary layers can catch them uniformly.
    """

    def __init__(self, message: str, *, code: str = "DOMAIN_ERROR") -> None:
        self.message = message
        self.code = code
        super().__init__(message)


class NotFoundError(DomainError):
    """Raised when requested entity is not found."""

    def __init__(self, *, entity_type: str, entity_id: str) -> None:
        super().__init__(
            message=f"{entity_type} with id '{entity_id}' not found",
            code="NOT_FOUND",
        )
        self.entity_type = entity_type
        self.entity_id = entity_id


class ConflictError(DomainError):
    """Raised when operation conflicts with current state."""

    def __init__(self, message: str) -> None:
        super().__init__(message=message, code="CONFLICT")


class AuthorizationError(DomainError):
    """Raised when user lacks required permissions."""

    def __init__(self, message: str = "Insufficient permissions") -> None:
        super().__init__(message=message, code="FORBIDDEN")

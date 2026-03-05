"""Base exception hierarchy for the domain layer."""

from __future__ import annotations


class DomainError(Exception):
    """Base exception for all domain errors.

    All domain-specific exceptions should inherit from
    this class to allow catch-all handling at boundaries.
    """

    def __init__(self, message: str, *, code: str = "DOMAIN_ERROR") -> None:
        """Initialize domain error.

        Args:
            message: Human-readable error description.
            code: Machine-readable error code.
        """
        self.message = message
        self.code = code
        super().__init__(message)


class NotFoundError(DomainError):
    """Raised when requested entity is not found."""

    def __init__(self, entity_type: str, entity_id: str) -> None:
        """Initialize not found error.

        Args:
            entity_type: Type name of the missing entity.
            entity_id: Identifier that was looked up.
        """
        super().__init__(
            message=f"{entity_type} with id '{entity_id}' not found",
            code="NOT_FOUND",
        )
        self.entity_type = entity_type
        self.entity_id = entity_id


class ConflictError(DomainError):
    """Raised when operation conflicts with current state."""

    def __init__(self, message: str) -> None:
        """Initialize conflict error.

        Args:
            message: Conflict description.
        """
        super().__init__(message=message, code="CONFLICT")


class AuthorizationError(DomainError):
    """Raised when user lacks required permissions."""

    def __init__(self, message: str = "Insufficient permissions") -> None:
        """Initialize authorization error.

        Args:
            message: Authorization failure description.
        """
        super().__init__(message=message, code="FORBIDDEN")

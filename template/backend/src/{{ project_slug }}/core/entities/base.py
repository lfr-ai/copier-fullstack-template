"""Base entity classes for domain modeling."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime


def utcnow() -> datetime:
    """Current UTC datetime."""
    return datetime.now(tz=UTC)


def generate_id() -> str:
    """Generate UUID4 entity identifier."""
    return str(uuid.uuid4())


@dataclass(frozen=True, slots=True)
class DomainEvent:
    """Base class for all domain events.

    Provides unique identification and timestamp
    for event tracking and sourcing.
    """

    event_id: str = field(default_factory=generate_id)
    occurred_at: datetime = field(default_factory=utcnow)


@dataclass(slots=True)
class Entity:
    """Base entity with identity and domain events.

    Provides unique identification and event collection
    for all domain entities.
    """

    id: str = field(default_factory=generate_id)
    _events: list[DomainEvent] = field(
        default_factory=list,
        init=False,
        repr=False,
        compare=False,
    )

    def register_event(self, event: DomainEvent) -> None:
        """Register domain event for later dispatch."""
        self._events.append(event)

    def collect_events(self) -> list[DomainEvent]:
        """Collect and clear all pending domain events."""
        events = self._events.copy()
        self._events.clear()
        return events

    def __eq__(self, other: object) -> bool:
        """Compare entities by identity."""
        if not isinstance(other, Entity):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash by entity identity."""
        return hash(self.id)


@dataclass(slots=True)
class AggregateRoot(Entity):
    """Base class for aggregate root entities.

    An aggregate root is the entry point to a consistency
    boundary.  External code should only interact with the
    aggregate through this root and never hold references
    to interior child entities.

    Aggregate roots own domain events: they register events
    during business operations, and the Unit of Work collects
    and dispatches them after a successful commit.

    Use ``AggregateRoot`` for entities that:
    - Are referenced directly by repositories
    - Enforce transactional invariants over child entities
    - Serve as the sole entry point for a cluster of objects
    """


@dataclass(frozen=True, slots=True)
class ValueObject:
    """Base class for immutable value objects.

    Value objects are compared by their attributes
    rather than identity.  Subclasses **must** call
    'validate()' from '__post_init__' to enforce
    domain invariants.
    """

    def validate(self) -> None:
        """Validate domain invariants.

        Override in subclasses and call from '__post_init__'
        to enforce constraints.

        Raises:
            DomainError: When invariants are violated.
        """

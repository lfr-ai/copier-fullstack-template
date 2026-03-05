"""Base entity classes for domain modeling."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone


def _utcnow() -> datetime:
    """Return current UTC datetime."""
    return datetime.now(tz=timezone.utc)


def _generate_id() -> str:
    """Generate unique entity identifier."""
    return str(uuid.uuid4())


@dataclass(frozen=True, slots=True)
class DomainEvent:
    """Base class for all domain events.

    Provides unique identification and timestamp
    for event tracking and sourcing.
    """

    event_id: str = field(default_factory=_generate_id)
    occurred_at: datetime = field(default_factory=_utcnow)


@dataclass(slots=True)
class Entity:
    """Base entity with identity and domain events.

    Provides unique identification and event collection
    for all domain entities.
    """

    id: str = field(default_factory=_generate_id)
    _events: list[DomainEvent] = field(
        default_factory=list,
        init=False,
        repr=False,
        compare=False,
    )

    def register_event(self, event: DomainEvent) -> None:
        """Register domain event for later dispatch.

        Args:
            event: Domain event to register.
        """
        self._events.append(event)

    def collect_events(self) -> list[DomainEvent]:
        """Collect and clear all pending domain events.

        Returns:
            List of pending domain events.
        """
        events = self._events.copy()
        self._events.clear()
        return events

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return NotImplemented
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


@dataclass(frozen=True, slots=True)
class ValueObject:
    """Base class for immutable value objects.

    Value objects are compared by their attributes
    rather than identity.
    """

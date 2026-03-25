"""Domain entity definitions.

Re-exports base entity types::

    from {{ project_slug }}.core.entities import (
        AggregateRoot,
        DomainEvent,
        Entity,
        ValueObject,
    )
"""

from __future__ import annotations

from {{ project_slug }}.core.entities.base import (
    AggregateRoot,
    DomainEvent,
    Entity,
    ValueObject,
)

__all__ = [
    "AggregateRoot",
    "DomainEvent",
    "Entity",
    "ValueObject",
]

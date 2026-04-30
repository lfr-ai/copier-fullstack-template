"""Domain entity definitions.

Re-exports base entity types::

    from package.core.entities import (
        AggregateRoot,
        DomainEvent,
        Entity,
        ValueObject,
    )
"""

from __future__ import annotations

from .base import (
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

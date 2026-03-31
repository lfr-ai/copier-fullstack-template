"""Abstract persistence mapper protocol.

Persistence mappers translate between ORM models (infrastructure)
and domain entities (core), ensuring the repository layer returns
pure domain objects while the database layer works with ORM models.
This enforces the Dependency Rule: adapters depend on core,
never the reverse.
"""

from __future__ import annotations

from typing import Protocol


class PersistenceMapper[EntityT, ModelT](Protocol):
    """Bidirectional mapper between a domain entity and an ORM model.

    Implementations live in ``adapters/persistence/mappers/`` and are
    used by repository adapters to cross the persistence boundary.
    """

    def to_entity(self, model: ModelT) -> EntityT:
        """Map an ORM model instance to a domain entity."""
        ...

    def to_model(self, entity: EntityT) -> ModelT:
        """Map a domain entity to an ORM model instance."""
        ...

    def update_model(self, *, model: ModelT, entity: EntityT) -> ModelT:
        """Apply domain entity state onto an existing ORM model."""
        ...

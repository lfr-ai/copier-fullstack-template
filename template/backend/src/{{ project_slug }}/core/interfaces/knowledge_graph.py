"""Knowledge graph gateway -- abstract interface for graph-based knowledge storage.

Concrete adapters may use NetworkX, Neo4j, RDFLib, or external knowledge
graphs (Wikidata, DBpedia) via SPARQL.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

DEFAULT_NEIGHBOR_DEPTH = 1

DEFAULT_NEIGHBOR_LIMIT = 50

DEFAULT_SPARQL_TIMEOUT_SECONDS = 30

DEFAULT_ENTITY_LOOKUP_LIMIT = 5

DEFAULT_RELATION_LIMIT = 50


@runtime_checkable
class KnowledgeGraphGateway(Protocol):
    """Gateway for knowledge graph CRUD and traversal."""

    async def add_triplet(
        self,
        *,
        subject: str,
        predicate: str,
        obj: str,
        metadata: dict[str, object] | None = None,
    ) -> None:
        """Add a subject-predicate-object triplet."""
        ...

    async def add_triplets(
        self,
        triplets: list[tuple[str, str, str]],
    ) -> None:
        """Bulk-add triplets."""
        ...

    async def query_neighbors(
        self,
        entity: str,
        *,
        depth: int = DEFAULT_NEIGHBOR_DEPTH,
        limit: int = DEFAULT_NEIGHBOR_LIMIT,
    ) -> list[dict[str, object]]:
        """Query neighbors of an entity."""
        ...

    async def query_triplets(
        self,
        *,
        subject: str | None = None,
        predicate: str | None = None,
        obj: str | None = None,
    ) -> list[tuple[str, str, str]]:
        """Query triplets by partial match."""
        ...

    async def delete_entity(self, entity: str) -> None:
        """Remove an entity and all its edges."""
        ...

    async def get_entity_count(self) -> int:
        """Return the number of entities in the graph."""
        ...

    async def get_triplet_count(self) -> int:
        """Return the number of triplets/edges in the graph."""
        ...


@runtime_checkable
class SPARQLQueryGateway(Protocol):
    """Gateway for SPARQL-capable knowledge graph stores (RDFLib, remote endpoints)."""

    async def sparql_query(
        self,
        query: str,
        *,
        timeout: int = DEFAULT_SPARQL_TIMEOUT_SECONDS,
    ) -> list[dict[str, str]]:
        """Execute a read-only SPARQL SELECT query."""
        ...


@runtime_checkable
class ExternalKnowledgeGraphGateway(Protocol):
    """Gateway for querying established external knowledge graphs.

    Supports lookup-oriented operations against Wikidata, DBpedia,
    ConceptNet, and similar public knowledge bases.
    """

    async def lookup_entity(
        self,
        entity: str,
        *,
        language: str = "en",
        limit: int = DEFAULT_ENTITY_LOOKUP_LIMIT,
    ) -> list[dict[str, object]]:
        """Look up an entity in the external knowledge graph.

        'language' is an ISO 639-1 code. 'entity_id' examples:
        Wikidata Q-ID, DBpedia URI.
        """
        ...

    async def get_entity_relations(
        self,
        entity_id: str,
        *,
        limit: int = DEFAULT_RELATION_LIMIT,
    ) -> list[tuple[str, str, str]]:
        """Get relations for a known entity ID (e.g. Wikidata Q-ID, DBpedia URI)."""
        ...

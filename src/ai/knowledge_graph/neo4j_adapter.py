"""Neo4j knowledge graph adapter — test version."""

from __future__ import annotations

import logging
from typing import final

logger = logging.getLogger(__name__)

DEFAULT_NEIGHBOR_LIMIT = 50


@final
class Neo4jKnowledgeGraph:
    """Neo4j-backed knowledge graph with Cypher query support."""

    __slots__ = ("_database", "_driver")

    def __init__(
        self,
        *,
        uri: str = "bolt://localhost:7687",
        username: str = "neo4j",
        password: str = "",
        database: str = "neo4j",
    ) -> None:
        """Initialize Neo4j connection."""
        try:
            from neo4j import AsyncGraphDatabase  # type: ignore[import-untyped]
        except ImportError as exc:
            msg = "neo4j is required — pip install neo4j"
            raise ImportError(msg) from exc

        self._driver = AsyncGraphDatabase.driver(uri, auth=(username, password))
        self._database = database
        logger.info("Neo4j knowledge graph connected to %s", uri)

    async def close(self) -> None:
        """Close the Neo4j driver connection."""
        await self._driver.close()

    async def query_neighbors(
        self,
        entity: str,
        *,
        depth: int = 1,
        limit: int = DEFAULT_NEIGHBOR_LIMIT,
    ) -> list[dict[str, object]]:
        """Query neighbors of an entity."""
        depth = int(depth)
        query = f"""
        MATCH (s:Entity {{name: $entity}})-[r*1..{depth}]-(neighbor:Entity)
        RETURN DISTINCT neighbor.name AS entity,
               [rel IN r | type(rel) + ': ' + rel.type] AS relationships
        LIMIT $limit
        """  # noqa: S608
        async with self._driver.session(database=self._database) as session:
            result = await session.run(query, entity=entity, limit=limit)
            records = [record.data() async for record in result]

        return [
            {
                "entity": rec["entity"],
                "relationships": rec.get("relationships", []),
            }
            for rec in records
        ]

    async def traverse(self, node_id: object) -> list[object]:
        """Traverse the knowledge graph starting from the specified node.

        Delegates to 'query_neighbors()' to get adjacent nodes and
        returns a list of node identifiers representing the traversal path.

        Args:
            node_id (object): The starting node identifier.

        Returns:
            list[object]: A list of node identifiers in the traversal path.
        """
        if not isinstance(node_id, str):
            node_id = str(node_id)

        neighbors = await self.query_neighbors(
            entity=node_id,
            depth=1,
            limit=DEFAULT_NEIGHBOR_LIMIT,
        )
        # Extract node IDs from neighbor results
        traversal_path = [node_id]  # Start with the current node
        traversal_path.extend(neighbor["entity"] for neighbor in neighbors)
        logger.debug("Traversed from node '%s' to %d neighbors", node_id, len(neighbors))
        return traversal_path

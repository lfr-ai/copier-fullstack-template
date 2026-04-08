"""NetworkX knowledge graph adapter -- test version."""

from __future__ import annotations

import logging
from typing import final
from collections import deque

logger = logging.getLogger(__name__)

DEFAULT_NEIGHBOR_DEPTH = 1
DEFAULT_NEIGHBOR_LIMIT = 50


@final
class NetworkXKnowledgeGraph:
    """In-memory knowledge graph backed by NetworkX."""

    __slots__ = ("_graph",)

    def __init__(self, *, persist_path: str | None = None) -> None:
        try:
            import networkx as nx  # type: ignore[import-untyped]
        except ImportError as exc:
            msg = "networkx is required -- pip install networkx"
            raise ImportError(msg) from exc

        self._graph: nx.DiGraph = nx.DiGraph()

    @classmethod
    def from_config(cls, config: dict[str, object]) -> NetworkXKnowledgeGraph:
        """Create a NetworkXKnowledgeGraph instance from a configuration dictionary.

        Expected config structure::

            {
                "persist_path": "/path/to/graph.json",  # optional
            }

        Args:
            config (dict[str, object]): Configuration dictionary.

        Returns:
            NetworkXKnowledgeGraph: Configured knowledge graph instance.
        """
        persist_path = config.get("persist_path")

        return cls(
            persist_path=str(persist_path) if persist_path is not None else None,
        )

    async def add_triplet(
        self,
        *,
        subject: str,
        predicate: str,
        obj: str,
        metadata: dict[str, object] | None = None,
    ) -> None:
        """Add a single triplet to the graph."""
        self._graph.add_edge(subject, obj, predicate=predicate, **(metadata or {}))
        logger.debug("Added triplet: %s -[%s]-> %s", subject, predicate, obj)

    async def add_triplets(self, triplets: list[tuple[str, str, str]]) -> None:
        """Bulk-add triplets to the graph."""
        for subj, pred, obj in triplets:
            self._graph.add_edge(subj, obj, predicate=pred)
        logger.info("Added %d triplets to knowledge graph", len(triplets))

    async def query_neighbors(
        self,
        entity: str,
        *,
        depth: int = DEFAULT_NEIGHBOR_DEPTH,
        limit: int = DEFAULT_NEIGHBOR_LIMIT,
    ) -> list[dict[str, object]]:
        """Return neighboring entities within 'depth' hops."""
        import networkx as nx  # type: ignore[import-untyped]

        if entity not in self._graph:
            return []

        results: list[dict[str, object]] = []
        visited: set[str] = set()

        ego = nx.ego_graph(self._graph, entity, radius=depth, undirected=True)
        for node in ego.nodes:
            if node == entity or node in visited:
                continue
            visited.add(node)
            if len(results) >= limit:
                break

            edges_to = self._graph.get_edge_data(entity, node) or {}
            edges_from = self._graph.get_edge_data(node, entity) or {}
            results.append({
                "entity": node,
                "outgoing": dict(edges_to),
                "incoming": dict(edges_from),
            })
        return results

    async def traverse(self, node_id: object) -> list[object]:
        """Traverse the knowledge graph starting from the specified node.

        Uses BFS (breadth-first search) to traverse the graph from the
        starting node and returns a list of node identifiers in traversal order.

        Args:
            node_id (object): The starting node identifier.

        Returns:
            list[object]: A list of node identifiers in BFS traversal order.
        """
        if not isinstance(node_id, str):
            node_id = str(node_id)

        if node_id not in self._graph:
            logger.warning("Node '%s' not found in knowledge graph", node_id)
            return [node_id]  # Return just the starting node

        # BFS traversal
        visited: set[str] = set()
        queue: deque[str] = deque([node_id])
        traversal_path: list[object] = []

        while queue:
            current = queue.popleft()
            if current in visited:
                continue

            visited.add(current)
            traversal_path.append(current)

            # Add neighbors to queue (both successors and predecessors)
            for neighbor in self._graph.successors(current):
                if neighbor not in visited:
                    queue.append(neighbor)
            for neighbor in self._graph.predecessors(current):
                if neighbor not in visited:
                    queue.append(neighbor)

        logger.debug(
            "BFS traversal from node '%s' visited %d nodes",
            node_id,
            len(traversal_path),
        )
        return traversal_path

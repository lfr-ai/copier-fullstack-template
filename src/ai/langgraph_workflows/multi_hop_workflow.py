"""Multi-hop workflow -- DEPRECATED.

.. deprecated::
    This module is deprecated. Use ``ai.rag.deep_rag_pipeline.DeepRAGPipeline``
    instead, which implements MDP-based adaptive retrieval (DeepRAG).

Legacy multi-hop reasoning with KG traversal and vector enrichment.
Kept for backward compatibility with existing tests.
"""

from __future__ import annotations

from typing import Any, Optional, final

import structlog

from core.interfaces.knowledge_graph import KnowledgeGraphBackend
from core.interfaces.retriever import RetrieverGateway

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


@final
class MultiHopWorkflow:
    """Multi-hop reasoning workflow with KG traversal and vector enrichment."""

    __slots__ = ("_kg_backend", "_retriever", "_max_hops")

    def __init__(
        self,
        *,
        kg_backend: Optional[KnowledgeGraphBackend],
        retriever: Optional[RetrieverGateway] = None,
        max_hops: int = 5,
    ) -> None:
        """Initialize the multi-hop workflow.

        Args:
            kg_backend: Optional knowledge graph backend for traversal.
            retriever: Optional retriever gateway for vector enrichment at each hop.
            max_hops: Maximum hops for graph traversal.
        """
        self._kg_backend = kg_backend
        self._retriever = retriever
        self._max_hops = max_hops

        log = logger.bind(
            workflow="multi-hop",
            kg_backend=type(kg_backend).__name__ if kg_backend else "None",
            retriever=type(retriever).__name__ if retriever else "None",
            max_hops=max_hops,
        )
        log.info(
            "MultiHopWorkflow initialized",
            has_kg=kg_backend is not None,
            has_retriever=retriever is not None,
        )

    async def traverse_and_enrich(self, start_node: Any) -> list[dict[str, Any]]:
        """Traverse the knowledge graph and enrich at each hop using vector context.

        Args:
            start_node: The starting node identifier.

        Returns:
            The enriched reasoning trace with combined graph and vector context.
        """
        log = logger.bind(workflow="multi-hop", start_node=str(start_node))
        log.info("Starting multi-hop traversal")

        trace: list[dict[str, Any]] = []

        # Get nodes via KG traversal or vector-only fallback
        if self._kg_backend:
            log.info("Using knowledge graph backend for traversal")
            nodes = await self._kg_backend.traverse(start_node)
        else:
            log.warning(
                "Knowledge graph backend unavailable. Falling back to vector-only traversal."
            )
            nodes = self._simulate_vector_only_traversal(start_node)

        # Enrich each node with vector context
        for i, node in enumerate(nodes[: self._max_hops]):
            enriched_context = await self._enrich_with_vector_context(node)
            trace.append({"node": node, "enrichment": enriched_context})
            log.debug(
                "Hop completed",
                hop=i + 1,
                total_hops=min(len(nodes), self._max_hops),
                node=str(node),
                enrichment_count=len(enriched_context),
            )

        log.info(
            "Multi-hop traversal completed",
            trace_length=len(trace),
            nodes_visited=len(trace),
        )
        return trace

    def _simulate_vector_only_traversal(self, start_node: Any) -> list[str]:
        """Simulate a vector-only traversal when no knowledge graph backend is available.

        Args:
            start_node: The starting node identifier.

        Returns:
            A simulated list of nodes for traversal.
        """
        return [f"Vector-{i}" for i in range(1, self._max_hops + 1)]

    async def _enrich_with_vector_context(
        self, node: Any
    ) -> list[dict[str, object]]:
        """Enrich a node with vector retrieval context.

        Args:
            node: The node to enrich.

        Returns:
            The enriched context for the node (retrieved documents).
        """
        if not self._retriever:
            logger.debug(
                "No retriever available for enrichment",
                node=str(node),
            )
            return []

        # Use retriever to get relevant context for this node
        query = str(node)
        log = logger.bind(workflow="multi-hop", query=query, node=str(node))

        try:
            log.debug("Retrieving vector context for node")
            results = await self._retriever.retrieve(query=query, top_k=3)

            enrichment = [
                {
                    "id": ctx.id,
                    "content": ctx.content,
                    "score": ctx.score,
                    "metadata": ctx.metadata,
                }
                for ctx in results
            ]

            log.debug(
                "Vector enrichment completed",
                result_count=len(enrichment),
                avg_score=sum(r["score"] for r in enrichment) / len(enrichment)
                if enrichment
                else 0.0,
            )
            return enrichment

        except Exception as exc:
            log.warning(
                "Vector enrichment failed",
                error=str(exc),
                error_type=type(exc).__name__,
            )
            return []
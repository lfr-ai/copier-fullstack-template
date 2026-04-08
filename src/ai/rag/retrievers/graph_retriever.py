"""Graph retriever -- knowledge graph traversal for RAG retrieval."""

from __future__ import annotations

import structlog
from typing import final, TYPE_CHECKING

if TYPE_CHECKING:
    from core.interfaces.knowledge_graph import KnowledgeGraphGateway
    from core.interfaces.llm import LLMGateway
    from core.interfaces.retriever import RetrievedContext

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)

DEFAULT_GRAPH_NEIGHBOR_LIMIT = 10
_ENTITY_EXTRACTION_MAX_TOKENS = 128
_ENTITY_EXTRACTION_TEMPERATURE = 0.0
_DEFAULT_GRAPH_DEPTH = 2
_BASE_DECAY_SCORE = 1.0
_RANK_OFFSET = 1


@final
class GraphRetriever:
    """Retriever that traverses a knowledge graph for context.

    Extracts entities from the query using the LLM, then
    traverses the graph to find relevant neighbors.

    Args:
        knowledge_graph (KnowledgeGraphGateway): Knowledge graph port implementation.
        llm (LLMGateway): LLM for entity extraction from queries.
        depth (int): Graph traversal depth.
    """

    __slots__ = ("_depth", "_kg", "_llm")

    def __init__(
        self,
        *,
        knowledge_graph: KnowledgeGraphGateway,
        llm: LLMGateway,
        depth: int = _DEFAULT_GRAPH_DEPTH,
    ) -> None:
        self._kg = knowledge_graph
        self._llm = llm
        self._depth = depth

    @classmethod
    def from_config(cls, config: dict[str, object]) -> GraphRetriever:
        """Create a GraphRetriever instance from a configuration dictionary.

        Expected config structure::

            {
                "knowledge_graph": <KnowledgeGraphGateway instance>,
                "llm": <LLMGateway instance>,
                "depth": 2,  # optional, defaults to 2
            }

        Args:
            config (dict[str, object]): Configuration dictionary.

        Returns:
            GraphRetriever: Configured graph retriever instance.

        Raises:
            ValueError: If required parameters are missing.
        """
        knowledge_graph = config.get("knowledge_graph")
        if knowledge_graph is None:
            msg = "knowledge_graph is required"
            raise ValueError(msg)

        llm = config.get("llm")
        if llm is None:
            msg = "llm is required"
            raise ValueError(msg)

        depth = int(config.get("depth", _DEFAULT_GRAPH_DEPTH))

        return cls(
            knowledge_graph=knowledge_graph,  # type: ignore[arg-type]
            llm=llm,  # type: ignore[arg-type]
            depth=depth,
        )

    async def retrieve(
        self,
        *,
        query: str,
        top_k: int = DEFAULT_GRAPH_NEIGHBOR_LIMIT,
        filters: dict[str, object] | None = None,
    ) -> list[RetrievedContext]:
        """Retrieve context by traversing the knowledge graph.

        Args:
            query (str): User query text.
            top_k (int): Maximum number of results.
            filters (dict[str, object] | None): Optional metadata filters (unused in graph traversal).

        Returns:
            list[RetrievedContext]: Retrieved context from graph traversal.
        """
        from core.interfaces.retriever import RetrievedContext

        # Extract entities from query via LLM
        extraction_prompt = (
            f"Extract the key entities (people, concepts, organizations, etc.) "
            f"from the following query. Return ONLY a comma-separated list.\n\n"
            f"Query: {query}"
        )
        entity_text = await self._llm.complete(
            prompt=extraction_prompt,
            system_prompt="Extract entities only. Return comma-separated list.",
            max_tokens=_ENTITY_EXTRACTION_MAX_TOKENS,
            temperature=_ENTITY_EXTRACTION_TEMPERATURE,
        )
        entities = [e.strip() for e in entity_text.split(",") if e.strip()]

        if not entities:
            logger.debug("No entities extracted from query")
            return []

        # Traverse graph for each entity
        results: list[RetrievedContext] = []
        seen: set[str] = set()

        for entity in entities:
            neighbors = await self._kg.query_neighbors(
                entity,
                depth=self._depth,
                limit=top_k,
            )
            for neighbor in neighbors:
                node_id = str(neighbor.get("entity", ""))
                if node_id and node_id not in seen:
                    seen.add(node_id)
                    results.append(RetrievedContext(
                        id=node_id,
                        score=_BASE_DECAY_SCORE / (_RANK_OFFSET + len(results)),
                        content=str(neighbor),
                        metadata={"source": "knowledge_graph", "entity": entity},
                    ))
                    if len(results) >= top_k:
                        break
            if len(results) >= top_k:
                break

        logger.info(
            "Graph retrieval complete: entities=%d results=%d",
            len(entities),
            len(results),
        )
        return results[:top_k]

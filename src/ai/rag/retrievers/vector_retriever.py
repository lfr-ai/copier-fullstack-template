"""Vector retriever -- implements 'RetrieverGateway' using embeddings + vector store.

The default retrieval strategy: embed the query, search the vector store,
and return matching context chunks.
"""

from __future__ import annotations

import structlog
from typing import TYPE_CHECKING, cast, final

if TYPE_CHECKING:
    from core.interfaces.embedding import EmbeddingGateway
    from core.interfaces.retriever import RetrievedContext
    from core.interfaces.vector_store import VectorStoreGateway

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)

DEFAULT_SIMILARITY_TOP_K = 5


@final
class VectorRetriever:
    """Retrieve context by embedding the query and searching the vector store."""

    __slots__ = ("_embedding", "_vector_store")

    def __init__(
        self,
        *,
        embedding: EmbeddingGateway,
        vector_store: VectorStoreGateway,
    ) -> None:
        self._embedding = embedding
        self._vector_store = vector_store

    @classmethod
    def from_config(cls, config: dict[str, object]) -> VectorRetriever:
        """Create a VectorRetriever instance from a configuration dictionary.

        Expected config structure::

            {
                "embedding": <EmbeddingGateway instance>,
                "vector_store": <VectorStoreGateway instance>,
            }

        Args:
            config (dict[str, object]): Configuration dictionary.

        Returns:
            VectorRetriever: Configured retriever instance.

        Raises:
            ValueError: If required parameters are missing.
        """
        embedding = config.get("embedding")
        if embedding is None:
            msg = "embedding is required"
            raise ValueError(msg)

        vector_store = config.get("vector_store")
        if vector_store is None:
            msg = "vector_store is required"
            raise ValueError(msg)

        return cls(
            embedding=cast("EmbeddingGateway", embedding),
            vector_store=cast("VectorStoreGateway", vector_store),
        )

    async def retrieve(
        self,
        *,
        query: str,
        top_k: int = DEFAULT_SIMILARITY_TOP_K,
        filters: dict[str, object] | None = None,
    ) -> list[RetrievedContext]:
        """Embed query and search the vector store.

        Args:
            query (str): User query text.
            top_k (int): Maximum number of results to return.
            filters (dict[str, object] | None): Optional metadata filters.

        Returns:
            list[RetrievedContext]: Ranked context chunks.
        """
        from core.interfaces.retriever import RetrievedContext

        query_vector = await self._embedding.embed_text(query)
        results = await self._vector_store.search(
            query_vector=query_vector,
            top_k=top_k,
            filters=filters,
        )
        return [
            RetrievedContext(
                id=r.id,
                content=str(r.metadata.get("content", "")) if r.metadata else "",
                score=r.score,
                metadata=r.metadata or {},
            )
            for r in results
        ]

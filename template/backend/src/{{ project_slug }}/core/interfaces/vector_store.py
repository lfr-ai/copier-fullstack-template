"""Vector store gateway — abstract interface for similarity search backends.

Concrete adapters: FAISS, Azure AI Search, Chroma, Pinecone, etc.
"""

from typing import Protocol, runtime_checkable, final

DEFAULT_SEARCH_TOP_K = 10


@runtime_checkable
class VectorStoreGateway(Protocol):
    """Gateway for vector-based similarity search and storage."""

    async def add_vectors(
        self,
        *,
        vectors: list[list[float]],
        ids: list[str],
        metadata: list[dict[str, object]] | None = None,
    ) -> None:
        """Add vectors with identifiers and optional metadata."""
        ...

    async def search(
        self,
        *,
        query_vector: list[float],
        top_k: int = DEFAULT_SEARCH_TOP_K,
        filters: dict[str, object] | None = None,
    ) -> list[VectorSearchResult]:
        """Search for nearest neighbors."""
        ...

    async def delete_vectors(self, ids: list[str]) -> None:
        """Delete vectors by identifiers."""
        ...

    async def count(self) -> int:
        """Return total number of stored vectors."""
        ...


@final
class VectorSearchResult:
    """Result from a vector similarity search."""

    __slots__ = ("id", "score", "metadata")

    def __init__(
        self,
        *,
        id: str,
        score: float,
        metadata: dict[str, object] | None = None,
    ) -> None:
        self.id = id
        self.score = score
        self.metadata = metadata or {}

    def __repr__(self) -> str:
        return f"VectorSearchResult(id={self.id!r}, score={self.score:.4f})"

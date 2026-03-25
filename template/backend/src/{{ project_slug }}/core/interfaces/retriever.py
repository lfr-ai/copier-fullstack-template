"""Retriever port — abstract interface for RAG retrieval strategies.

Concrete adapters may implement simple vector search, hybrid search
(vector + keyword), or re-ranking strategies.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

_DEFAULT_RETRIEVAL_TOP_K: int = 5


@dataclass(frozen=True, slots=True)
class RetrievedContext:
    """Retrieved context chunk with relevance metadata."""

    id: str
    content: str
    score: float
    metadata: dict[str, object] = field(default_factory=dict)


@runtime_checkable
class RetrieverPort(Protocol):
    """Protocol for retrieving relevant context for a query."""

    async def retrieve(
        self,
        *,
        query: str,
        top_k: int = _DEFAULT_RETRIEVAL_TOP_K,
        filters: dict[str, object] | None = None,
    ) -> list[RetrievedContext]:
        """Retrieve relevant context chunks for a query."""
        ...

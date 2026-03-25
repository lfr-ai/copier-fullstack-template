"""Reranker port — abstract interface for search result reranking.

Concrete adapters may use Cohere, Cross-Encoder models, LLM-based
reranking, or reciprocal rank fusion strategies.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

_DEFAULT_RERANK_TOP_K: int = 5


@dataclass(frozen=True, slots=True)
class RankedResult:
    """Reranked search result with updated relevance score."""

    id: str
    content: str
    original_score: float
    rerank_score: float
    metadata: dict[str, object] = field(default_factory=dict)


@runtime_checkable
class RerankerPort(Protocol):
    """Protocol for reranking search results by relevance."""

    async def rerank(
        self,
        *,
        query: str,
        results: list[dict[str, object]],
        top_k: int = _DEFAULT_RERANK_TOP_K,
    ) -> list[RankedResult]:
        """Rerank search results by relevance.

        Each dict in 'results' must contain 'content' and 'score' keys.
        """
        ...

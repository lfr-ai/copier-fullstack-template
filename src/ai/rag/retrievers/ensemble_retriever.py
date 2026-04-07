"""Ensemble retriever — weighted combination of multiple retriever strategies."""

from __future__ import annotations

import structlog
from typing import final, TYPE_CHECKING

if TYPE_CHECKING:
    from app.core.interfaces.retriever import RetrievedContext, RetrieverGateway

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)

DEFAULT_GRAPH_NEIGHBOR_LIMIT = 10
_OVERSAMPLE_FACTOR = 2


def reciprocal_rank_fusion(
    ranked_lists: list[tuple[list[RetrievedContext], float]],
    *,
    top_k: int,
) -> list[RetrievedContext]:
    """Merge multiple ranked result lists using Reciprocal Rank Fusion."""
    from app.core.interfaces.retriever import RetrievedContext

    scores: dict[str, float] = {}
    items: dict[str, RetrievedContext] = {}
    k = 60  # RRF constant

    for results, weight in ranked_lists:
        for rank, item in enumerate(results, start=1):
            score = weight / (k + rank)
            scores[item.id] = scores.get(item.id, 0.0) + score
            items[item.id] = item

    sorted_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
    return [
        RetrievedContext(
            id=item_id,
            content=items[item_id].content,
            score=scores[item_id],
            metadata=items[item_id].metadata,
        )
        for item_id in sorted_ids[:top_k]
    ]


@final
class EnsembleRetriever:
    """Ensemble retriever combining multiple strategies via RRF.

    Uses Reciprocal Rank Fusion to merge ranked result lists
    from multiple retrievers into a single unified ranking.

    Args:
        retrievers (list[tuple[RetrieverGateway, float]]): (retriever, weight) tuples.
    """

    __slots__ = ("_retrievers",)

    def __init__(self, *, retrievers: list[tuple[RetrieverGateway, float]]) -> None:
        if not retrievers:
            msg = "At least one retriever is required"
            raise ValueError(msg)
        self._retrievers = retrievers

    @classmethod
    def from_config(cls, config: dict[str, object]) -> EnsembleRetriever:
        """Create an EnsembleRetriever instance from a configuration dictionary.

        Expected config structure::

            {
                "retrievers": [
                    {"retriever": <RetrieverGateway instance>, "weight": 0.5},
                    {"retriever": <RetrieverGateway instance>, "weight": 0.5},
                ]
            }

        Args:
            config (dict[str, object]): Configuration dictionary.

        Returns:
            EnsembleRetriever: Configured ensemble retriever instance.

        Raises:
            ValueError: If required parameters are missing or invalid.
        """
        retrievers_config = config.get("retrievers")
        if retrievers_config is None:
            msg = "retrievers list is required"
            raise ValueError(msg)

        if not isinstance(retrievers_config, list):
            msg = "retrievers must be a list"
            raise ValueError(msg)

        retrievers: list[tuple[RetrieverGateway, float]] = []
        for item in retrievers_config:
            if not isinstance(item, dict):
                msg = "each retriever entry must be a dict with 'retriever' and 'weight'"
                raise ValueError(msg)

            retriever = item.get("retriever")
            if retriever is None:
                msg = "retriever is required in each entry"
                raise ValueError(msg)

            weight = item.get("weight", 1.0)
            retrievers.append((retriever, float(weight)))  # type: ignore[arg-type]

        return cls(retrievers=retrievers)

    async def retrieve(
        self,
        *,
        query: str,
        top_k: int = DEFAULT_GRAPH_NEIGHBOR_LIMIT,
        filters: dict[str, object] | None = None,
    ) -> list[RetrievedContext]:
        """Retrieve and fuse results from all configured retrievers.

        Args:
            query (str): User query text.
            top_k (int): Maximum number of results after fusion.
            filters (dict[str, object] | None): Optional metadata filters passed to sub-retrievers.

        Returns:
            list[RetrievedContext]: Fused and re-ranked retrieved context.
        """
        from app.core.interfaces.retriever import RetrievedContext

        ranked_lists: list[tuple[list[RetrievedContext], float]] = []
        for retriever, weight in self._retrievers:
            results = await retriever.retrieve(query=query, top_k=top_k * _OVERSAMPLE_FACTOR, filters=filters)
            ranked_lists.append((results, weight))

        fused = reciprocal_rank_fusion(ranked_lists, top_k=top_k)

        logger.info(
            "Ensemble retrieval complete: retrievers=%d results=%d",
            len(self._retrievers),
            len(fused),
        )
        return fused

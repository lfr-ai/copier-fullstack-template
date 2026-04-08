"""DeepRAG pipeline test version -- minimal implementation for integration testing.

This lightweight implementation keeps `AIConfigLoader` pipeline wiring working in
`src/` without pulling in the full template workflow stack.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast, final

import structlog

if TYPE_CHECKING:
    from core.interfaces.llm import LLMGateway
    from core.interfaces.retriever import RetrieverGateway

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


@final
class DeepRAGPipeline:
    """Minimal DeepRAG pipeline used by config-loader integration tests."""

    __slots__ = ("_llm", "_retriever")

    def __init__(
        self,
        *,
        llm: LLMGateway,
        retriever: RetrieverGateway,
    ) -> None:
        self._llm = llm
        self._retriever = retriever

        logger.info(
            "DeepRAGPipeline initialized",
            llm_type=type(llm).__name__,
            retriever_type=type(retriever).__name__,
        )

    @classmethod
    def from_config(cls, config: dict[str, object]) -> DeepRAGPipeline:
        """Create a DeepRAGPipeline instance from a configuration dictionary."""
        llm = config.get("llm")
        if llm is None:
            msg = "llm is required"
            raise ValueError(msg)

        retriever = config.get("retriever")
        if retriever is None:
            msg = "retriever is required"
            raise ValueError(msg)

        return cls(
            llm=cast("LLMGateway", llm),
            retriever=cast("RetrieverGateway", retriever),
        )

    @property
    def llm(self) -> LLMGateway:
        """Return the configured LLM gateway."""
        return self._llm

    @property
    def retriever(self) -> RetrieverGateway:
        """Return the configured retriever gateway."""
        return self._retriever

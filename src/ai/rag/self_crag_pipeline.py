"""Self-CRAG pipeline test version -- minimal implementation for integration testing."""

from __future__ import annotations

from typing import TYPE_CHECKING, final

import structlog

if TYPE_CHECKING:
    from core.interfaces.llm import LLMGateway
    from core.interfaces.retriever import RetrieverGateway

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


@final
class SelfCRAGPipeline:
    """Self-corrective RAG pipeline with LLM-based relevance grading.
    
    This is a minimal test version for integration testing of the config loader.
    The full implementation with LangGraph StateGraph is in the template directory.
    """

    __slots__ = ("_llm", "_retriever")

    def __init__(
        self,
        *,
        llm: LLMGateway,
        retriever: RetrieverGateway,
    ) -> None:
        """Initialize the Self-CRAG pipeline.

        Args:
            llm: LLM gateway for relevance grading, query rewriting, and answer generation.
            retriever: Retriever gateway for document retrieval.
        """
        self._llm = llm
        self._retriever = retriever
        
        logger.info(
            "SelfCRAGPipeline initialized",
            llm_type=type(llm).__name__,
            retriever_type=type(retriever).__name__,
        )

    @property
    def llm(self) -> LLMGateway:
        """Return the configured LLM gateway."""
        return self._llm

    @property
    def retriever(self) -> RetrieverGateway:
        """Return the configured retriever gateway."""
        return self._retriever

"""Self-CRAG retrieval pipeline -- self-corrective RAG with LLM-based grading.

Orchestrates the Self-CRAG workflow using LangGraph StateGraph:
- Initial retrieval
- Document relevance grading
- Adaptive query rewriting
- Bounded re-retrieval cycles
- Final answer generation
"""

from __future__ import annotations

from typing import final

import structlog

# Use relative imports to avoid template variable issues
from ...core.interfaces.llm import LLMGateway
from ...core.interfaces.retriever import RetrieverGateway
from ..rag.retrieval import RetrievalResult
from .self_crag_nodes import (
    generate_answer_node,
    grade_documents_node,
    initial_retrieve_node,
    re_retrieve_node,
    rewrite_query_node,
    route_after_grading,
)
from .self_crag_state import SelfCRAGState

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


@final
class SelfCRAGPipeline:
    """Self-corrective RAG pipeline with LLM-based relevance grading.

    Orchestrates a LangGraph workflow that:
    1. Retrieves documents for the query
    2. Grades document relevance using LLM
    3. If relevance is low, rewrites query and re-retrieves (bounded cycles)
    4. Generates final answer from graded documents

    The workflow uses LangGraph StateGraph to manage state transitions
    and conditional routing based on relevance scores.
    """

    __slots__ = ("_llm", "_retriever", "_graph")

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
        self._graph = None

    @classmethod
    def from_config(cls, config: dict[str, object]) -> SelfCRAGPipeline:
        """Create a SelfCRAGPipeline from a configuration dictionary.

        Expected config structure::

            {
                "llm": <LLMGateway instance>,
                "retriever": <RetrieverGateway instance>,
            }

        Args:
            config: Configuration dictionary.

        Returns:
            Configured pipeline instance.

        Raises:
            ValueError: If required parameters are missing.
        """
        llm = config.get("llm")
        if llm is None:
            msg = "llm is required"
            raise ValueError(msg)

        retriever = config.get("retriever")
        if retriever is None:
            msg = "retriever is required"
            raise ValueError(msg)

        return cls(llm=llm, retriever=retriever)  # type: ignore[arg-type]

    def _build_graph(self) -> object:
        """Lazily build the LangGraph StateGraph for Self-CRAG workflow.

        Returns:
            Compiled LangGraph StateGraph.
        """
        if self._graph is not None:
            return self._graph

        try:
            from langgraph.graph import END, START, StateGraph  # type: ignore[import-untyped]
        except ImportError as exc:
            msg = "langgraph is required -- pip install langgraph"
            raise ImportError(msg) from exc

        # Create graph with SelfCRAGState schema
        graph = StateGraph(SelfCRAGState)

        # Wire nodes with injected dependencies using closures
        # Each node gets llm or retriever via closure
        async def initial_retrieve_wrapper(state: SelfCRAGState) -> dict:
            return await initial_retrieve_node(state, retriever=self._retriever)

        async def grade_documents_wrapper(state: SelfCRAGState) -> dict:
            return await grade_documents_node(state, llm=self._llm)

        async def rewrite_query_wrapper(state: SelfCRAGState) -> dict:
            return await rewrite_query_node(state, llm=self._llm)

        async def re_retrieve_wrapper(state: SelfCRAGState) -> dict:
            return await re_retrieve_node(state, retriever=self._retriever)

        async def generate_answer_wrapper(state: SelfCRAGState) -> dict:
            return await generate_answer_node(state, llm=self._llm)

        # Add nodes to graph
        graph.add_node("initial_retrieve", initial_retrieve_wrapper)
        graph.add_node("grade_documents", grade_documents_wrapper)
        graph.add_node("rewrite_query", rewrite_query_wrapper)
        graph.add_node("re_retrieve", re_retrieve_wrapper)
        graph.add_node("generate_answer", generate_answer_wrapper)

        # Add static edges
        graph.add_edge(START, "initial_retrieve")
        graph.add_edge("initial_retrieve", "grade_documents")
        graph.add_edge("rewrite_query", "re_retrieve")
        graph.add_edge("re_retrieve", "grade_documents")
        graph.add_edge("generate_answer", END)

        # Add conditional edge: grade_documents routes to rewrite_query or generate_answer
        graph.add_conditional_edges(
            "grade_documents",
            route_after_grading,
            {
                "rewrite_query": "rewrite_query",
                "generate_answer": "generate_answer",
            },
        )

        # Compile graph
        self._graph = graph.compile()
        return self._graph

    async def query(
        self,
        question: str,
        *,
        top_k: int = 5,
        system_prompt: str | None = None,
    ) -> RetrievalResult:
        """Execute a Self-CRAG query with adaptive retrieval.

        Args:
            question: User's natural language question.
            top_k: Number of source chunks to retrieve (passed to retriever).
            system_prompt: Optional custom system prompt for LLM instructions.

        Returns:
            RetrievalResult with answer and workflow metadata.
        """
        log = logger.bind(
            workflow="self-crag",
            query_len=len(question),
            top_k=top_k,
        )
        log.info("Self-CRAG workflow: entry")

        # Build and invoke graph
        compiled_graph = self._build_graph()

        initial_state: SelfCRAGState = {
            "query": question,
            "original_query": question,
            "docs": [],
            "scores": [],
            "cycle_count": 0,
            "answer": "",
            "system_prompt": system_prompt,
            "top_k": top_k,
        }

        # Invoke graph with initial state
        final_state: SelfCRAGState = await compiled_graph.ainvoke(initial_state)

        # Extract workflow metadata
        retrieval_attempts = final_state.get("cycle_count", 0) + 1  # +1 for initial retrieval
        query_rewrite_count = final_state.get("cycle_count", 0)
        scores = final_state.get("scores", [])
        overall_relevance = sum(scores) / len(scores) if scores else 0.0
        answer = final_state.get("answer", "")
        docs = final_state.get("docs", [])

        log.info(
            "Self-CRAG workflow: completion",
            retrieval_attempts=retrieval_attempts,
            query_rewrite_count=query_rewrite_count,
            relevance_score=round(overall_relevance, 3),
            answer_len=len(answer),
            doc_count=len(docs),
        )

        # Convert to RetrievalResult for consistent interface
        # Map RetrievedContext to VectorSearchResult-like structure
        from ...core.interfaces.vector_store import VectorSearchResult

        sources = [
            VectorSearchResult(
                id=doc.source or f"doc_{i}",
                score=scores[i] if i < len(scores) else 0.0,
                metadata={"content": doc.content, "source": doc.source},
            )
            for i, doc in enumerate(docs)
        ]

        return RetrievalResult(
            query=question,
            answer=answer,
            sources=sources,
            graph_context=[],
        )

"""DeepRAG pipeline -- step-by-step retrieval via MDP-modeled reasoning.

Orchestrates the DeepRAG workflow using LangGraph StateGraph:
- Iterative query decomposition into atomic sub-queries
- Atomic decisions: retrieve external knowledge vs parametric reasoning
- Bounded retrieval budget to minimize noise
- Final answer synthesis from reasoning chain

The pipeline models retrieval-augmented reasoning as a Markov Decision
Process (MDP), dynamically determining at each step whether to retrieve
or rely on the LLM parametric knowledge.

Reference: DeepRAG (Guan et al., 2025) -- arXiv:2502.01142
"""

from __future__ import annotations

from typing import Any, final

import structlog

from ...core.interfaces.knowledge_graph import KnowledgeGraphGateway
from ...core.interfaces.llm import LLMGateway
from ...core.interfaces.retriever import RetrieverGateway
from ...core.interfaces.vector_store import VectorSearchResult
from ..rag.retrieval import RetrievalResult
from .deep_rag_nodes import (
    atomic_decision_node,
    decompose_query_node,
    parametric_answer_node,
    retrieve_node,
    route_after_decision,
    route_termination,
    synthesize_answer_node,
)
from .deep_rag_state import DeepRAGState

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


@final
class DeepRAGPipeline:
    """DeepRAG pipeline with MDP-based adaptive retrieval.

    Orchestrates a LangGraph workflow that:
    1. Decomposes the query into atomic sub-queries
    2. For each sub-query, decides whether to retrieve or use parametric knowledge
    3. Retrieves documents or generates parametric answers accordingly
    4. Loops back for the next sub-query (bounded by max steps)
    5. Synthesizes a final answer from the full reasoning chain

    The workflow uses LangGraph StateGraph with Annotated reducers
    for accumulating sub-query results and reasoning traces.
    """

    __slots__ = ("_graph", "_knowledge_graph", "_llm", "_retriever")

    def __init__(
        self,
        *,
        llm: LLMGateway,
        retriever: RetrieverGateway,
        knowledge_graph: KnowledgeGraphGateway | None = None,
    ) -> None:
        """Initialize the DeepRAG pipeline.

        Args:
            llm: LLM gateway for decomposition, decisions, and synthesis.
            retriever: Retriever gateway for external document retrieval.
            knowledge_graph: Optional KG gateway for graph-enhanced retrieval.
        """
        self._llm = llm
        self._retriever = retriever
        self._knowledge_graph = knowledge_graph
        self._graph: object | None = None

    @classmethod
    def from_config(cls, config: dict[str, object]) -> DeepRAGPipeline:
        """Create a DeepRAGPipeline from a configuration dictionary.

        Expected config structure::

            {
                "llm": <LLMGateway instance>,
                "retriever": <RetrieverGateway instance>,
                "knowledge_graph": <KnowledgeGraphGateway | None>,  # optional
            }

        Args:
            config: Configuration dictionary.

        Returns:
            DeepRAGPipeline: Configured pipeline instance.

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

        return cls(
            llm=llm,  # type: ignore[arg-type]
            retriever=retriever,  # type: ignore[arg-type]
            knowledge_graph=config.get("knowledge_graph"),  # type: ignore[arg-type]
        )

    def _build_graph(self) -> object:
        """Lazily build the LangGraph StateGraph for DeepRAG workflow.

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

        graph = StateGraph(DeepRAGState)

        # Create node wrappers with injected dependencies
        async def decompose_wrapper(state: DeepRAGState) -> dict[str, Any]:
            return await decompose_query_node(state, llm=self._llm)

        async def decision_wrapper(state: DeepRAGState) -> dict[str, Any]:
            return await atomic_decision_node(state, llm=self._llm)

        async def retrieve_wrapper(state: DeepRAGState) -> dict[str, Any]:
            return await retrieve_node(
                state,
                retriever=self._retriever,
                llm=self._llm,
                knowledge_graph=self._knowledge_graph,
            )

        async def parametric_wrapper(state: DeepRAGState) -> dict[str, Any]:
            return await parametric_answer_node(state, llm=self._llm)

        async def synthesize_wrapper(state: DeepRAGState) -> dict[str, Any]:
            return await synthesize_answer_node(state, llm=self._llm)

        # Add nodes
        graph.add_node("decompose_query", decompose_wrapper)
        graph.add_node("atomic_decision", decision_wrapper)
        graph.add_node("retrieve", retrieve_wrapper)
        graph.add_node("parametric_answer", parametric_wrapper)
        graph.add_node("synthesize_answer", synthesize_wrapper)

        # Static edges
        graph.add_edge(START, "decompose_query")
        graph.add_edge("decompose_query", "atomic_decision")
        graph.add_edge("synthesize_answer", END)

        # Conditional: atomic_decision -> retrieve or parametric_answer
        graph.add_conditional_edges(
            "atomic_decision",
            route_after_decision,
            {
                "retrieve": "retrieve",
                "parametric_answer": "parametric_answer",
            },
        )

        # After retrieve or parametric_answer -> check termination
        graph.add_conditional_edges(
            "retrieve",
            route_termination,
            {
                "decompose_query": "decompose_query",
                "synthesize_answer": "synthesize_answer",
            },
        )
        graph.add_conditional_edges(
            "parametric_answer",
            route_termination,
            {
                "decompose_query": "decompose_query",
                "synthesize_answer": "synthesize_answer",
            },
        )

        self._graph = graph.compile()
        return self._graph

    async def query(
        self,
        question: str,
        *,
        top_k: int = 5,
        system_prompt: str | None = None,
    ) -> RetrievalResult:
        """Execute a DeepRAG query with step-by-step adaptive retrieval.

        Args:
            question: User's natural language question.
            top_k: Number of source chunks per retrieval step.
            system_prompt: Optional custom system prompt.

        Returns:
            RetrievalResult with answer, sources, and reasoning trace.
        """
        log = logger.bind(
            workflow="deep-rag",
            query_len=len(question),
            top_k=top_k,
        )
        log.info("DeepRAG workflow: entry")

        compiled_graph = self._build_graph()

        initial_state: DeepRAGState = {
            "query": question,
            "sub_queries": [],
            "current_sub_query": "",
            "step_count": 0,
            "retrieval_count": 0,
            "should_terminate": False,
            "final_answer": "",
            "system_prompt": system_prompt,
            "reasoning_trace": [],
        }

        final_state: DeepRAGState = await compiled_graph.ainvoke(initial_state)

        # Extract results
        answer = final_state.get("final_answer", "")
        sub_queries = final_state.get("sub_queries", [])
        retrieval_count = final_state.get("retrieval_count", 0)
        step_count = final_state.get("step_count", 0)

        # Collect all retrieved documents as sources
        sources: list[VectorSearchResult] = []
        for sq in sub_queries:
            for doc in sq.get("retrieved_docs", []):
                sources.append(
                    VectorSearchResult(
                        id=doc.id,
                        score=doc.score,
                        metadata={
                            "content": doc.content,
                            "source": doc.metadata.get("source", ""),
                            "sub_query": sq.get("sub_query", ""),
                            "decision": sq.get("decision", ""),
                        },
                    )
                )

        # Build graph context from reasoning trace
        graph_context = [
            {
                "step": i + 1,
                "sub_query": sq.get("sub_query", ""),
                "decision": sq.get("decision", ""),
                "intermediate_answer": sq.get("intermediate_answer", ""),
                "doc_count": len(sq.get("retrieved_docs", [])),
            }
            for i, sq in enumerate(sub_queries)
        ]

        log.info(
            "DeepRAG workflow: completion",
            step_count=step_count,
            retrieval_count=retrieval_count,
            source_count=len(sources),
            answer_len=len(answer),
        )

        return RetrievalResult(
            query=question,
            answer=answer,
            sources=sources[:top_k],
            graph_context=graph_context,
        )

"""DeepRAG LangGraph nodes and routing logic.

Implements node functions for the DeepRAG pipeline modeled as an MDP:
- decompose_query_node: Decompose query into atomic sub-queries
- atomic_decision_node: Decide retrieve vs parametric for each sub-query
- retrieve_node: Retrieve external documents for a sub-query
- parametric_answer_node: Generate answer from LLM parametric knowledge
- synthesize_answer_node: Combine intermediate answers into final response
- route_after_decision: Route based on atomic decision
- route_termination: Decide whether to continue decomposing or finalize

Reference: DeepRAG (Guan et al., 2025) -- arXiv:2502.01142
"""

from __future__ import annotations

from typing import Any

import structlog

from ...core.interfaces.knowledge_graph import KnowledgeGraphGateway
from ...core.interfaces.llm import LLMGateway
from ...core.interfaces.retriever import RetrieverGateway
from ..prompts.rag_prompts import (
    DEEPRAG_DECOMPOSE_PROMPT,
    DEEPRAG_ATOMIC_DECISION_PROMPT,
    DEEPRAG_PARAMETRIC_ANSWER_PROMPT,
    DEEPRAG_SYNTHESIZE_PROMPT,
    RAG_QUERY_PROMPT,
)
from .deep_rag_state import (
    DeepRAGState,
    SubQueryResult,
    _MAX_REASONING_STEPS,
    _MAX_RETRIEVAL_BUDGET,
    _PARAMETRIC_CONFIDENCE_THRESHOLD,
)

logger = structlog.get_logger()


async def decompose_query_node(
    state: DeepRAGState,
    *,
    llm: LLMGateway,
) -> dict[str, Any]:
    """Decompose the query into the next atomic sub-query.

    Uses the LLM to generate the next sub-query based on the original
    question and previously gathered intermediate answers.

    Args:
        state: Current workflow state.
        llm: LLM gateway for sub-query generation.

    Returns:
        State update with current_sub_query and incremented step_count.
    """
    query = state["query"]
    sub_queries = state.get("sub_queries", [])
    step_count = state.get("step_count", 0)

    log = logger.bind(node="decompose_query", step=step_count)
    log.debug("decompose_query_node: entry")

    # Build context from previous sub-query results
    previous_context = ""
    for sq in sub_queries:
        previous_context += (
            f"Sub-query: {sq.get('sub_query', '')}\n"
            f"Answer: {sq.get('intermediate_answer', '')}\n\n"
        )

    prompt = DEEPRAG_DECOMPOSE_PROMPT.format(
        question=query,
        previous_context=previous_context or "None yet.",
        step_number=step_count + 1,
    )

    sub_query = await llm.complete(prompt=prompt, temperature=0.3)
    sub_query = sub_query.strip()

    log.debug("decompose_query_node: exit", sub_query_len=len(sub_query))

    return {
        "current_sub_query": sub_query,
        "step_count": step_count + 1,
        "reasoning_trace": [f"Step {step_count + 1}: Decomposed sub-query: {sub_query}"],
    }


async def atomic_decision_node(
    state: DeepRAGState,
    *,
    llm: LLMGateway,
) -> dict[str, Any]:
    """Make an atomic decision: retrieve external knowledge or use parametric.

    The LLM evaluates whether it can confidently answer the sub-query
    from its parametric knowledge, or if external retrieval is needed.

    Args:
        state: Current workflow state with current_sub_query.
        llm: LLM gateway for decision making.

    Returns:
        State update with the decision ('retrieve' or 'parametric')
        stored in the current sub-query result.
    """
    sub_query = state.get("current_sub_query", "")
    retrieval_count = state.get("retrieval_count", 0)
    query = state["query"]

    log = logger.bind(
        node="atomic_decision",
        sub_query_len=len(sub_query),
        retrieval_count=retrieval_count,
    )
    log.debug("atomic_decision_node: entry")

    # If retrieval budget exhausted, force parametric
    if retrieval_count >= _MAX_RETRIEVAL_BUDGET:
        log.debug("atomic_decision_node: retrieval budget exhausted, forcing parametric")
        return {
            "sub_queries": [SubQueryResult(
                sub_query=sub_query,
                decision="parametric",
                retrieved_docs=[],
                intermediate_answer="",
                confidence=0.0,
            )],
            "reasoning_trace": [f"Decision: parametric (budget exhausted, {retrieval_count}/{_MAX_RETRIEVAL_BUDGET})"],
        }

    prompt = DEEPRAG_ATOMIC_DECISION_PROMPT.format(
        question=query,
        sub_query=sub_query,
    )

    response = await llm.complete(prompt=prompt, temperature=0.0)
    response_lower = response.strip().lower()

    # Parse decision
    if "retrieve" in response_lower:
        decision = "retrieve"
    elif "parametric" in response_lower:
        decision = "parametric"
    else:
        # Default to retrieve when uncertain
        decision = "retrieve"

    log.debug("atomic_decision_node: exit", decision=decision)

    return {
        "sub_queries": [SubQueryResult(
            sub_query=sub_query,
            decision=decision,
            retrieved_docs=[],
            intermediate_answer="",
            confidence=0.0,
        )],
        "reasoning_trace": [f"Decision for '{sub_query}': {decision}"],
    }


async def retrieve_node(
    state: DeepRAGState,
    *,
    retriever: RetrieverGateway,
    llm: LLMGateway,
    knowledge_graph: KnowledgeGraphGateway | None = None,
) -> dict[str, Any]:
    """Retrieve external documents and generate intermediate answer.

    Optionally enriches retrieval with knowledge graph neighbors when
    a KG gateway is provided.

    Args:
        state: Current workflow state.
        retriever: Retriever gateway for document retrieval.
        llm: LLM gateway for answer generation with retrieved context.
        knowledge_graph: Optional KG gateway for graph-enhanced context.

    Returns:
        State update with retrieved docs, intermediate answer, and incremented retrieval_count.
    """
    sub_queries = state.get("sub_queries", [])
    retrieval_count = state.get("retrieval_count", 0)

    if not sub_queries:
        return {}

    current = sub_queries[-1]
    sub_query = current.get("sub_query", "")

    log = logger.bind(node="retrieve", sub_query_len=len(sub_query))
    log.debug("retrieve_node: entry")

    # Retrieve documents
    docs = await retriever.retrieve(query=sub_query, top_k=3)

    # Optionally enrich with KG neighbors
    kg_context = ""
    if knowledge_graph is not None:
        try:
            # Extract key entities from the sub-query to look up in the graph
            neighbors = await knowledge_graph.query_neighbors(entity=sub_query, depth=1, limit=5)
            if neighbors:
                kg_context = "\n".join(
                    f"[KG] {n.get('subject', '')} --{n.get('predicate', '')}--> {n.get('object', '')}"
                    for n in neighbors
                    if isinstance(n, dict)
                )
                log.debug("retrieve_node: KG enrichment", neighbor_count=len(neighbors))
        except Exception:  # noqa: BLE001 -- graceful fallback if KG query fails
            log.debug("retrieve_node: KG enrichment failed, continuing without")

    # Build context from retrieved docs
    context = "\n\n".join(
        f"[Document {i + 1}]: {doc.content}"
        for i, doc in enumerate(docs)
        if doc.content
    )
    if kg_context:
        context = f"{context}\n\n{kg_context}"

    # Generate intermediate answer using retrieved context
    prompt = RAG_QUERY_PROMPT.format(
        context=context,
        question=sub_query,
    )

    intermediate_answer = await llm.complete(prompt=prompt, temperature=0.2)

    # Update the last sub-query result (replace via new append, pop handled externally)
    updated = SubQueryResult(
        sub_query=sub_query,
        decision="retrieve",
        retrieved_docs=docs,
        intermediate_answer=intermediate_answer.strip(),
        confidence=1.0,
    )

    log.debug(
        "retrieve_node: exit",
        doc_count=len(docs),
        answer_len=len(intermediate_answer),
    )

    # Replace last entry: pop via negative indexing not supported in reducers,
    # so we track this with a separate update pattern
    return {
        "sub_queries": [updated],
        "retrieval_count": retrieval_count + 1,
        "reasoning_trace": [
            f"Retrieved {len(docs)} docs for '{sub_query}', "
            f"answer: {intermediate_answer.strip()[:100]}..."
        ],
    }


async def parametric_answer_node(
    state: DeepRAGState,
    *,
    llm: LLMGateway,
) -> dict[str, Any]:
    """Generate intermediate answer using LLM parametric knowledge only.

    Args:
        state: Current workflow state.
        llm: LLM gateway for parametric answer generation.

    Returns:
        State update with intermediate answer and confidence score.
    """
    sub_queries = state.get("sub_queries", [])

    if not sub_queries:
        return {}

    current = sub_queries[-1]
    sub_query = current.get("sub_query", "")

    log = logger.bind(node="parametric_answer", sub_query_len=len(sub_query))
    log.debug("parametric_answer_node: entry")

    prompt = DEEPRAG_PARAMETRIC_ANSWER_PROMPT.format(sub_query=sub_query)

    answer = await llm.complete(prompt=prompt, temperature=0.2)

    updated = SubQueryResult(
        sub_query=sub_query,
        decision="parametric",
        retrieved_docs=[],
        intermediate_answer=answer.strip(),
        confidence=_PARAMETRIC_CONFIDENCE_THRESHOLD,
    )

    log.debug("parametric_answer_node: exit", answer_len=len(answer))

    return {
        "sub_queries": [updated],
        "reasoning_trace": [
            f"Parametric answer for '{sub_query}': {answer.strip()[:100]}..."
        ],
    }


async def synthesize_answer_node(
    state: DeepRAGState,
    *,
    llm: LLMGateway,
) -> dict[str, Any]:
    """Synthesize final answer from all intermediate sub-query results.

    Combines all intermediate answers and retrieved context to produce
    a coherent final response.

    Args:
        state: Current workflow state with all sub-query results.
        llm: LLM gateway for answer synthesis.

    Returns:
        State update with final_answer.
    """
    query = state["query"]
    sub_queries = state.get("sub_queries", [])
    system_prompt = state.get("system_prompt")

    log = logger.bind(
        node="synthesize_answer",
        query_len=len(query),
        sub_query_count=len(sub_queries),
    )
    log.debug("synthesize_answer_node: entry")

    # Build reasoning chain from all sub-query results
    reasoning_parts: list[str] = []
    for i, sq in enumerate(sub_queries):
        sub_q = sq.get("sub_query", "")
        decision = sq.get("decision", "unknown")
        answer = sq.get("intermediate_answer", "")
        reasoning_parts.append(
            f"Step {i + 1} [{decision}]: {sub_q}\n"
            f"Answer: {answer}"
        )

    reasoning_chain = "\n\n".join(reasoning_parts)

    prompt = DEEPRAG_SYNTHESIZE_PROMPT.format(
        question=query,
        reasoning_chain=reasoning_chain,
    )

    if system_prompt:
        prompt = f"{system_prompt}\n\n{prompt}"

    final_answer = await llm.complete(prompt=prompt, temperature=0.2)

    log.debug("synthesize_answer_node: exit", answer_len=len(final_answer))

    return {
        "final_answer": final_answer.strip(),
        "should_terminate": True,
        "reasoning_trace": [f"Final answer synthesized ({len(final_answer)} chars)"],
    }


def route_after_decision(state: DeepRAGState) -> str:
    """Route based on the atomic decision for the current sub-query.

    Args:
        state: Current workflow state.

    Returns:
        'retrieve' if external retrieval needed, 'parametric_answer' otherwise.
    """
    sub_queries = state.get("sub_queries", [])
    if not sub_queries:
        return "parametric_answer"

    current = sub_queries[-1]
    decision = current.get("decision", "retrieve")

    log = logger.bind(node="route_after_decision", decision=decision)
    log.debug("route_after_decision: evaluating")

    if decision == "retrieve":
        return "retrieve"
    return "parametric_answer"


def route_termination(state: DeepRAGState) -> str:
    """Decide whether to continue decomposing or synthesize final answer.

    Terminates when:
    - step_count >= max reasoning steps
    - should_terminate is explicitly set
    - All sub-queries have been answered

    Args:
        state: Current workflow state.

    Returns:
        'decompose_query' to continue, 'synthesize_answer' to finalize.
    """
    step_count = state.get("step_count", 0)
    should_terminate = state.get("should_terminate", False)

    log = logger.bind(
        node="route_termination",
        step_count=step_count,
        should_terminate=should_terminate,
        max_steps=_MAX_REASONING_STEPS,
    )
    log.debug("route_termination: evaluating")

    if should_terminate or step_count >= _MAX_REASONING_STEPS:
        log.debug("route_termination: routing to synthesize_answer")
        return "synthesize_answer"

    log.debug("route_termination: routing to decompose_query")
    return "decompose_query"

"""Self-CRAG LangGraph nodes and routing logic.

Implements the node functions for the self-corrective RAG pipeline:
- initial_retrieve_node: Initial document retrieval
- grade_documents_node: LLM-based relevance grading
- rewrite_query_node: Query optimization for re-retrieval
- re_retrieve_node: Re-retrieval with rewritten query
- generate_answer_node: Final answer generation
- route_after_grading: Routing function for grade -> rewrite vs. generate
"""

from __future__ import annotations

from typing import Any

import structlog

# Use relative imports to avoid template variable issues
from ...core.interfaces.llm import LLMGateway
from ...core.interfaces.retriever import RetrieverGateway
from ..prompts.rag_prompts import (
    QUERY_REWRITE_PROMPT,
    RAG_QUERY_PROMPT,
    RELEVANCE_GRADING_PROMPT,
)
from .self_crag_state import (
    MAX_QUERY_REWRITES,
    RELEVANCE_THRESHOLD,
    SelfCRAGState,
)

logger = structlog.get_logger()


async def initial_retrieve_node(
    state: SelfCRAGState,
    *,
    retriever: RetrieverGateway,
) -> dict[str, Any]:
    """Initial retrieval node: retrieve documents for the original query.

    Args:
        state: Current workflow state containing the original query.
        retriever: Retriever gateway for document retrieval.

    Returns:
        State update with retrieved documents and initialized cycle_count.
    """
    query = state["query"]
    log = logger.bind(node="initial_retrieve", query_len=len(query))
    log.debug("initial_retrieve_node: entry")

    top_k = state.get("top_k", 5)
    docs = await retriever.retrieve(query=query, top_k=top_k)

    log.debug(
        "initial_retrieve_node: exit",
        doc_count=len(docs),
    )

    return {
        "docs": docs,
        "original_query": query,
        "cycle_count": 0,
    }


async def grade_documents_node(
    state: SelfCRAGState,
    *,
    llm: LLMGateway,
) -> dict[str, Any]:
    """Grade documents node: assess relevance of each retrieved document.

    Args:
        state: Current workflow state containing query and documents.
        llm: LLM gateway for relevance grading.

    Returns:
        State update with relevance scores for each document.
    """
    query = state["query"]
    docs = state["docs"]
    log = logger.bind(node="grade_documents", query_len=len(query), doc_count=len(docs))
    log.debug("grade_documents_node: entry")

    scores: list[float] = []

    for doc in docs:
        prompt = RELEVANCE_GRADING_PROMPT.format(
            document=doc.content,
            question=query,
        )

        # Call LLM to grade relevance
        response = await llm.complete(
            prompt=prompt,
            temperature=0.0,  # Deterministic grading
        )

        # Parse score from response
        try:
            score = float(response.strip())
            # Clamp to [0.0, 1.0]
            score = max(0.0, min(1.0, score))
        except ValueError:
            # If parsing fails, assign low relevance
            log.warning(
                "grade_documents_node: failed to parse score",
                response=response[:100],
            )
            score = 0.0

        scores.append(score)

    # Compute overall relevance (mean of scores)
    overall_relevance = sum(scores) / len(scores) if scores else 0.0

    log.debug(
        "grade_documents_node: exit",
        scores_count=len(scores),
        overall_relevance=round(overall_relevance, 3),
    )

    return {
        "scores": scores,
    }


async def rewrite_query_node(
    state: SelfCRAGState,
    *,
    llm: LLMGateway,
) -> dict[str, Any]:
    """Rewrite query node: optimize query for better retrieval.

    Args:
        state: Current workflow state containing original_query and cycle_count.
        llm: LLM gateway for query rewriting.

    Returns:
        State update with rewritten query and incremented cycle_count.
    """
    original_query = state["original_query"]
    cycle_count = state["cycle_count"]
    log = logger.bind(
        node="rewrite_query",
        original_query_len=len(original_query),
        cycle_count=cycle_count,
    )
    log.debug("rewrite_query_node: entry")

    prompt = QUERY_REWRITE_PROMPT.format(original_query=original_query)

    # Call LLM to rewrite query
    rewritten_query = await llm.complete(
        prompt=prompt,
        temperature=0.3,  # Some creativity for rewriting
    )

    rewritten_query = rewritten_query.strip()

    log.debug(
        "rewrite_query_node: exit",
        rewritten_query_len=len(rewritten_query),
        new_cycle_count=cycle_count + 1,
    )

    return {
        "query": rewritten_query,
        "cycle_count": cycle_count + 1,
    }


async def re_retrieve_node(
    state: SelfCRAGState,
    *,
    retriever: RetrieverGateway,
) -> dict[str, Any]:
    """Re-retrieve node: retrieve documents with rewritten query.

    Args:
        state: Current workflow state containing rewritten query.
        retriever: Retriever gateway for document retrieval.

    Returns:
        State update with newly retrieved documents.
    """
    query = state["query"]
    log = logger.bind(node="re_retrieve", query_len=len(query))
    log.debug("re_retrieve_node: entry")

    top_k = state.get("top_k", 5)
    docs = await retriever.retrieve(query=query, top_k=top_k)

    log.debug(
        "re_retrieve_node: exit",
        doc_count=len(docs),
    )

    return {
        "docs": docs,
    }


async def generate_answer_node(
    state: SelfCRAGState,
    *,
    llm: LLMGateway,
) -> dict[str, Any]:
    """Generate answer node: synthesize final answer from graded documents.

    Args:
        state: Current workflow state containing query, docs, scores, and optional system_prompt.
        llm: LLM gateway for answer generation.

    Returns:
        State update with final answer.
    """
    query = state["query"]
    docs = state["docs"]
    scores = state.get("scores", [])
    system_prompt = state.get("system_prompt")

    log = logger.bind(
        node="generate_answer",
        query_len=len(query),
        doc_count=len(docs),
        scores_count=len(scores),
        has_system_prompt=system_prompt is not None,
    )
    log.debug("generate_answer_node: entry")

    # Format context from documents
    context_parts = []
    for i, doc in enumerate(docs):
        score = scores[i] if i < len(scores) else 0.0
        context_parts.append(f"[Source {i+1}, relevance={score:.2f}]\n{doc.content}")

    context = "\n\n".join(context_parts)

    # Build base prompt
    base_prompt = RAG_QUERY_PROMPT.format(
        context=context,
        question=query,
    )

    # Prepend system_prompt if provided
    if system_prompt:
        prompt = f"{system_prompt}\n\n{base_prompt}"
    else:
        prompt = base_prompt

    # Call LLM to generate answer
    answer = await llm.complete(
        prompt=prompt,
        temperature=0.2,  # Mostly deterministic, slight creativity
    )

    log.debug(
        "generate_answer_node: exit",
        answer_len=len(answer),
    )

    return {
        "answer": answer,
    }


def route_after_grading(state: SelfCRAGState) -> str:
    """Routing function: decide whether to rewrite query or generate answer.

    Args:
        state: Current workflow state containing scores and cycle_count.

    Returns:
        'rewrite_query' if relevance is below threshold and rewrites < max,
        'generate_answer' otherwise.
    """
    scores = state.get("scores", [])
    cycle_count = state.get("cycle_count", 0)

    # Compute overall relevance
    overall_relevance = sum(scores) / len(scores) if scores else 0.0

    log = logger.bind(
        node="route_after_grading",
        overall_relevance=round(overall_relevance, 3),
        cycle_count=cycle_count,
        threshold=RELEVANCE_THRESHOLD,
        max_rewrites=MAX_QUERY_REWRITES,
    )
    log.debug("route_after_grading: evaluating")

    # Route to rewrite if relevance below threshold and rewrites not exhausted
    if overall_relevance < RELEVANCE_THRESHOLD and cycle_count < MAX_QUERY_REWRITES:
        log.debug("route_after_grading: routing to rewrite_query")
        return "rewrite_query"

    log.debug("route_after_grading: routing to generate_answer")
    return "generate_answer"

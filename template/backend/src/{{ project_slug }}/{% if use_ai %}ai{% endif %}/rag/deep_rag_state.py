"""DeepRAG state schema for LangGraph workflow.

Models retrieval-augmented reasoning as a Markov Decision Process (MDP).
Each state represents a partial solution with sub-queries, intermediate
answers, and atomic decisions about whether to retrieve or use parametric
knowledge at each reasoning step.

Reference: DeepRAG (Guan et al., 2025) -- arXiv:2502.01142
"""

import operator
from typing import Annotated, TypedDict

from ...core.interfaces.retriever import RetrievedContext

_MAX_REASONING_STEPS = 5

_MAX_RETRIEVAL_BUDGET = 3

_PARAMETRIC_CONFIDENCE_THRESHOLD = 0.7


class SubQueryResult(TypedDict, total=False):
    """Result of a single sub-query reasoning step.

    Attributes:
        sub_query: Decomposed atomic sub-query.
        decision: Atomic decision -- 'retrieve' or 'parametric'.
        retrieved_docs: Documents retrieved (empty if parametric).
        intermediate_answer: Answer for this sub-query step.
        confidence: LLM confidence in parametric answer (0.0-1.0).
    """

    sub_query: str
    decision: str
    retrieved_docs: list[RetrievedContext]
    intermediate_answer: str
    confidence: float


class DeepRAGState(TypedDict, total=False):
    """State schema for DeepRAG LangGraph workflow (MDP formulation).

    The state represents the partial solution at each reasoning step,
    tracking the original query, decomposed sub-queries, intermediate
    answers, and retrieval decisions.

    Attributes:
        query: Original user query.
        sub_queries: Accumulated sub-query results (append-only via reducer).
        current_sub_query: Sub-query being processed in the current step.
        step_count: Current reasoning step number.
        retrieval_count: Number of retrieval operations performed.
        should_terminate: Whether the model should finalize the answer.
        final_answer: Synthesized final answer.
        system_prompt: Optional custom system prompt.
        reasoning_trace: Full reasoning trace for debugging.
    """

    query: str
    sub_queries: Annotated[list[SubQueryResult], operator.add]
    current_sub_query: str
    step_count: int
    retrieval_count: int
    should_terminate: bool
    final_answer: str
    system_prompt: str | None
    reasoning_trace: Annotated[list[str], operator.add]

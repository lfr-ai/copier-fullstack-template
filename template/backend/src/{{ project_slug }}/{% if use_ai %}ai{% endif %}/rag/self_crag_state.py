"""Self-CRAG state schema for LangGraph workflow.

Defines the state structure for the self-corrective RAG pipeline,
including query, retrieved documents, relevance scores, and cycle tracking.
"""

from typing import TypedDict

# Use relative import to avoid template variable issues
from ...core.interfaces.retriever import RetrievedContext

# Configuration constants
RELEVANCE_THRESHOLD = 0.6
"""Minimum relevance score threshold for document acceptance."""

MAX_QUERY_REWRITES = 2
"""Maximum number of query rewrite cycles before falling back."""


class SelfCRAGState(TypedDict, total=False):
    """State schema for Self-CRAG LangGraph workflow.
    
    Attributes:
        query: Current query string (may be rewritten during cycles).
        original_query: The initial user query (preserved for fallback).
        docs: List of retrieved documents from the current retrieval.
        scores: List of LLM-graded relevance scores (0.0-1.0) for each doc.
        cycle_count: Number of query rewrite cycles executed (0-MAX_QUERY_REWRITES).
        answer: Final generated answer (populated at workflow end).
    """
    
    query: str
    original_query: str
    docs: list[RetrievedContext]
    scores: list[float]
    cycle_count: int
    answer: str

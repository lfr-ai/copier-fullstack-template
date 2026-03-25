"""AI module configuration — model settings, provider defaults, RAG pipeline constants."""

from __future__ import annotations


from {{ project_slug }}.core.value_objects.model_config import (  # noqa: F401
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE,
)

MAX_TOKEN_LIMIT = 128_000
"""Hard upper bound for max_tokens across all providers."""

MAX_PROMPT_LENGTH = 32_000
"""Maximum character length for user prompts."""

MAX_SYSTEM_PROMPT_LENGTH = 8_000
"""Maximum character length for system prompts."""

DEFAULT_CHAT_MODEL = "gpt-4o"
"""Default chat completion model identifier."""

DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
"""Default embedding model identifier."""

DEFAULT_ANTHROPIC_MODEL = "claude-sonnet-4-6"
"""Default Anthropic model identifier."""

DEFAULT_SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L6-v2"
"""Default sentence-transformers model for local embeddings."""

DEFAULT_CROSS_ENCODER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"
"""Default cross-encoder model for reranking."""


DEFAULT_EMBEDDING_DIMENSION = 1536
"""Default vector dimension (OpenAI text-embedding-3-small)."""

DEFAULT_SIMILARITY_TOP_K = 5
"""Default number of results in similarity search."""


DEFAULT_CHUNK_SIZE = 512
"""Default chunk size in characters for text splitting."""

DEFAULT_CHUNK_OVERLAP = 64
"""Default overlap between consecutive chunks."""

DEFAULT_GRAPH_NEIGHBOR_LIMIT = 10
"""Default limit for knowledge graph neighbor queries."""

DEFAULT_HISTORY_WINDOW = 10
"""Default number of recent messages to include in context."""

DEFAULT_AGENT_MAX_STEPS = 10
"""Default maximum reasoning steps for agent loops."""

DEFAULT_POOL_MIN_SIZE = 1
"""Default minimum connection pool size."""

DEFAULT_POOL_MAX_SIZE = 5
"""Default maximum connection pool size."""

EVAL_MAX_TOKENS = 256
"""Maximum tokens for evaluation LLM responses."""

EXTRACTION_INPUT_LIMIT = 4_000
"""Maximum character length for entity extraction input."""

DEFAULT_CONVERSATION_LIMIT = 50
"""Default maximum messages to retrieve from conversation history."""

DEFAULT_CONVERSATION_TTL = 86_400
"""Default TTL in seconds (24 h) for Redis conversation keys."""

DEFAULT_SEARCH_TOP_K = 10
"""Default top-k for vector store similarity search."""

RECURSION_LIMIT_MULTIPLIER = 2
"""LangGraph recursion limit is max_iterations × this multiplier."""

SOURCE_TEXT_PREVIEW_LENGTH = 500
"""Maximum character length for source-node text previews."""

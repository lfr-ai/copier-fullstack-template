"""Pydantic models for AI request/response payloads."""

from typing import final

from pydantic import BaseModel, ConfigDict, Field

__all__ = [
    "CompletionRequest",
    "CompletionResponse",
    "DocumentIngestRequest",
    "DocumentIngestResponse",
    "RAGQueryRequest",
    "RAGQueryResponse",
    "SourceReference",
    "VectorSearchRequest",
    "VectorSearchResponse",
]

from ..config import (
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE,
    MAX_PROMPT_LENGTH,
    MAX_SYSTEM_PROMPT_LENGTH,
    MAX_TOKEN_LIMIT,
)


@final
class CompletionRequest(BaseModel):
    """Request payload for an AI completion."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        frozen=True,
    )

    prompt: str = Field(
        ...,
        min_length=1,
        max_length=MAX_PROMPT_LENGTH,
        description="User prompt text",
        examples=["Summarize the following document..."],
    )
    system_prompt: str | None = Field(
        default=None,
        max_length=MAX_SYSTEM_PROMPT_LENGTH,
        description="Optional system-level instructions",
        examples=["You are a helpful assistant"],
    )
    max_tokens: int = Field(
        default=DEFAULT_MAX_TOKENS,
        ge=1,
        le=MAX_TOKEN_LIMIT,
        description="Maximum tokens in response",
        examples=[256, 1024, 4096],
    )
    temperature: float = Field(
        default=DEFAULT_TEMPERATURE,
        ge=0.0,
        le=2.0,
        description="Sampling temperature",
        examples=[0.0, 0.7, 1.5],
    )


@final
class CompletionResponse(BaseModel):
    """Response payload from an AI completion."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        frozen=True,
    )

    content: str = Field(
        ...,
        description="Generated text content",
        examples=["Here is a summary of the document..."],
    )
    model: str = Field(
        ...,
        description="Model identifier used for generation",
        examples=["gpt-4o", "claude-sonnet-4-6"],
    )
    prompt_tokens: int = Field(
        default=0,
        ge=0,
        description="Number of prompt tokens consumed",
        examples=[100, 500],
    )
    completion_tokens: int = Field(
        default=0,
        ge=0,
        description="Number of completion tokens generated",
        examples=[50, 200],
    )

    @property
    def total_tokens(self) -> int:
        """Calculate total token usage."""
        return self.prompt_tokens + self.completion_tokens


@final
class DocumentIngestRequest(BaseModel):
    """Request to ingest a document into the knowledge base."""

    model_config = ConfigDict(str_strip_whitespace=True, frozen=True)

    source: str = Field(..., min_length=1, description="Document source path or URL")


@final
class DocumentIngestResponse(BaseModel):
    """Summary of a document ingestion operation."""

    model_config = ConfigDict(str_strip_whitespace=True, frozen=True)

    source: str = Field(..., description="Ingested document source")
    document_count: int = Field(default=1, ge=0)
    chunk_count: int = Field(default=0, ge=0)


@final
class SourceReference(BaseModel):
    """Single source reference from vector search or RAG retrieval."""

    model_config = ConfigDict(str_strip_whitespace=True, frozen=True)

    id: str = Field(..., description="Chunk/document identifier")
    score: float = Field(default=0.0, ge=0.0, le=1.0)
    content: str = Field(default="", description="Snippet of matched content")


@final
class RAGQueryRequest(BaseModel):
    """Request for a RAG-augmented query."""

    model_config = ConfigDict(str_strip_whitespace=True, frozen=True)

    question: str = Field(..., min_length=1, max_length=MAX_PROMPT_LENGTH)
    top_k: int = Field(default=5, ge=1, le=50)
    system_prompt: str | None = Field(default=None, max_length=MAX_SYSTEM_PROMPT_LENGTH)
    use_graph: bool = Field(default=False)
    strategy: str = Field(default="auto")
    use_lightrag: bool = Field(default=False)
    lightrag_mode: str = Field(default="mix")
    combine_strategies: bool = Field(default=False)


@final
class RAGQueryResponse(BaseModel):
    """Response from a RAG-augmented query."""

    model_config = ConfigDict(str_strip_whitespace=True, frozen=True)

    question: str
    answer: str
    sources: list[SourceReference] = Field(default_factory=list)


@final
class VectorSearchRequest(BaseModel):
    """Direct vector similarity search request."""

    model_config = ConfigDict(str_strip_whitespace=True, frozen=True)

    query: str = Field(..., min_length=1, max_length=MAX_PROMPT_LENGTH)
    top_k: int = Field(default=5, ge=1, le=100)
    filters: dict[str, object] | None = Field(default=None)


@final
class VectorSearchResponse(BaseModel):
    """Vector similarity search results."""

    model_config = ConfigDict(str_strip_whitespace=True, frozen=True)

    query: str
    results: list[SourceReference] = Field(default_factory=list)

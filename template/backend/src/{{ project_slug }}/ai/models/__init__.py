"""Pydantic models for AI request/response payloads."""

from __future__ import annotations

__all__ = ["CompletionRequest", "CompletionResponse"]

from pydantic import BaseModel, ConfigDict, Field

from ..config import (
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE,
    MAX_PROMPT_LENGTH,
    MAX_SYSTEM_PROMPT_LENGTH,
    MAX_TOKEN_LIMIT,
)


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
        examples=["gpt-4o", "claude-sonnet-4-20250514"],
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

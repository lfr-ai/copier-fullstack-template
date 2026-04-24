"""LLM provider gateway."""

from collections.abc import AsyncIterator
from typing import Protocol, runtime_checkable

from ..value_objects.model_config import (
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE,
)


@runtime_checkable
class LLMGateway(Protocol):
    """Gateway for LLM completion providers."""

    @property
    def model(self) -> str:
        """Return the configured model identifier."""
        ...

    async def complete(
        self,
        *,
        prompt: str,
        system_prompt: str | None = None,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE,
    ) -> str:
        """Generate a text completion."""
        ...

    async def stream(
        self,
        *,
        prompt: str,
        system_prompt: str | None = None,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE,
    ) -> AsyncIterator[str]:
        """Stream completion chunks."""
        ...

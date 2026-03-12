"""AI provider protocol — abstract interface for LLM backends.

Implementations live in adapters/ or concrete provider modules.
The core application depends only on this protocol.
"""

from __future__ import annotations

__all__ = ["AIProvider"]

from typing import Protocol, runtime_checkable

from ..config import DEFAULT_MAX_TOKENS, DEFAULT_TEMPERATURE


@runtime_checkable
class AIProvider(Protocol):
    """Protocol for AI/LLM provider implementations."""

    async def complete(
        self,
        *,
        prompt: str,
        system_prompt: str | None = None,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE,
    ) -> str:
        """Generate a text completion.

        Args:
            prompt (str): User prompt text.
            system_prompt (str | None): Optional system-level instructions.
            max_tokens (int): Maximum tokens in response.
            temperature (float): Sampling temperature (0.0–2.0).

        Returns:
            str: Generated text response.
        """
        ...

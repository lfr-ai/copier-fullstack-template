"""Base LLM adapter — abstract interface for language model providers."""

from __future__ import annotations

import abc
from collections.abc import AsyncIterator

__all__ = ["BaseLLMAdapter"]


class BaseLLMAdapter(abc.ABC):
    """Abstract base for all LLM provider adapters.

    Subclasses must implement ``complete`` and ``stream``.
    """

    @abc.abstractmethod
    async def complete(self, prompt: str, **kwargs: object) -> str:
        """Generate a completion for *prompt* and return the text.

        Args:
            prompt (str): User prompt text.
            **kwargs: Provider-specific keyword arguments.

        Returns:
            str: Generated text response.
        """

    @abc.abstractmethod
    async def stream(self, prompt: str, **kwargs: object) -> AsyncIterator[str]:
        """Return an async iterator of completion chunks.

        Args:
            prompt (str): User prompt text.
            **kwargs: Provider-specific keyword arguments.

        Returns:
            AsyncIterator[str]: Async iterator yielding text chunks.
        """

"""OpenAI LLM adapter (placeholder).

Add ``openai`` to your project dependencies before using.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Final, override

from .base_llm_adapter import BaseLLMAdapter

__all__ = ["OpenAIAdapter"]

_DEFAULT_MODEL: Final[str] = "gpt-4o"


class OpenAIAdapter(BaseLLMAdapter):
    """Adapter for the OpenAI chat-completions API."""

    __slots__ = ("_client", "_model")

    def __init__(self, *, api_key: str, model: str = _DEFAULT_MODEL) -> None:
        """Initialize OpenAI adapter.

        Args:
            api_key (str): OpenAI API key.
            model (str): Model identifier to use for completions.

        Raises:
            ImportError: If the openai package is not installed.
        """
        try:
            import openai  # type: ignore[import-untyped]

            self._client = openai.AsyncOpenAI(api_key=api_key)
        except ImportError as exc:
            msg = "openai is required — pip install openai"
            raise ImportError(msg) from exc
        self._model = model

    @override
    async def complete(self, prompt: str, **kwargs: object) -> str:
        """Return a single completion string.

        Args:
            prompt (str): User prompt text.
            **kwargs: Additional OpenAI API parameters.

        Returns:
            str: Generated completion text.
        """
        response = await self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs,
        )
        return response.choices[0].message.content or ""

    @override
    async def stream(self, prompt: str, **kwargs: object) -> AsyncIterator[str]:  # noqa: RUF029
        """Return an async stream of delta content.

        Args:
            prompt (str): User prompt text.
            **kwargs: Additional OpenAI API parameters.

        Returns:
            AsyncIterator[str]: Async iterator yielding streamed text chunks.
        """
        return await self._client.chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            **kwargs,
        )

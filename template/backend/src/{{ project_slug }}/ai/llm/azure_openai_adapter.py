"""Azure OpenAI LLM adapter (placeholder).

Add ``openai`` to your project dependencies before using.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Final, override

from .base_llm_adapter import BaseLLMAdapter

__all__ = ["AzureOpenAIAdapter"]

_DEFAULT_API_VERSION: Final[str] = "2024-12-01-preview"


class AzureOpenAIAdapter(BaseLLMAdapter):
    """Adapter for Azure-hosted OpenAI models."""

    __slots__ = ("_client", "_deployment")

    def __init__(
        self,
        *,
        endpoint: str,
        api_key: str,
        deployment: str,
        api_version: str = _DEFAULT_API_VERSION,
    ) -> None:
        """Initialize Azure OpenAI adapter.

        Args:
            endpoint (str): Azure OpenAI endpoint URL.
            api_key (str): API key for authentication.
            deployment (str): Model deployment name.
            api_version (str): Azure API version string.

        Raises:
            ImportError: If the openai package is not installed.
        """
        try:
            import openai  # type: ignore[import-untyped]

            self._client = openai.AsyncAzureOpenAI(
                azure_endpoint=endpoint,
                api_key=api_key,
                api_version=api_version,
            )
        except ImportError as exc:
            msg = "openai is required — pip install openai"
            raise ImportError(msg) from exc
        self._deployment = deployment

    @override
    async def complete(self, prompt: str, **kwargs: object) -> str:
        """Return a single completion string.

        Args:
            prompt (str): User prompt text.
            **kwargs: Additional Azure OpenAI API parameters.

        Returns:
            str: Generated completion text.
        """
        response = await self._client.chat.completions.create(
            model=self._deployment,
            messages=[{"role": "user", "content": prompt}],
            **kwargs,
        )
        return response.choices[0].message.content or ""

    @override
    async def stream(self, prompt: str, **kwargs: object) -> AsyncIterator[str]:  # noqa: RUF029
        """Return an async stream of delta content.

        Args:
            prompt (str): User prompt text.
            **kwargs: Additional Azure OpenAI API parameters.

        Returns:
            AsyncIterator[str]: Async iterator yielding streamed text chunks.
        """
        return await self._client.chat.completions.create(
            model=self._deployment,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            **kwargs,
        )

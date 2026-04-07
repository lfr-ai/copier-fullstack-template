"""Universal LLM adapter via LiteLLM — one adapter for 100+ providers.

LiteLLM provides a single 'completion()' / 'acompletion()' interface
that routes to OpenAI, Anthropic, Azure, Bedrock, Vertex AI, Ollama,
and 100+ other providers based on the model string alone.

Model string examples::

    "gpt-4o"                           # OpenAI
    "anthropic/claude-sonnet-4-6"  # Anthropic
    "azure/<deployment>"               # Azure OpenAI
    "ollama/llama3"                    # Ollama (local)
    "bedrock/anthropic.claude-sonnet-4-6-v1:0"  # AWS Bedrock
    "vertex_ai/gemini-pro"             # Google Vertex
"""

from __future__ import annotations

import structlog
from collections.abc import AsyncIterator
from typing import final

from ai.config import DEFAULT_CHAT_MODEL, DEFAULT_MAX_TOKENS, DEFAULT_TEMPERATURE

from .base_llm_adapter import BaseLLMAdapter

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)

_DEFAULT_NUM_RETRIES = 2
@final
class LiteLLMAdapter(BaseLLMAdapter):
    """Universal LLM adapter backed by LiteLLM.

    Handles provider routing, retry, timeout, and streaming for
    any model that LiteLLM supports. Provider-specific API keys
    are read from environment variables following LiteLLM conventions
    ('OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'AZURE_API_KEY', etc.).

    Args:
        model (str): LiteLLM model string (e.g. '"gpt-4o"',
            '"anthropic/claude-sonnet-4-6"').
        api_key (str | None): Explicit API key (overrides env var).
        api_base (str | None): Custom API base URL (for Azure, proxies, local models).
        api_version (str | None): API version (Azure OpenAI).
        timeout (float | None): Request timeout in seconds.
        num_retries (int): Number of automatic retries on transient errors.
        drop_params (bool): Drop unsupported params instead of raising.
        extra_kwargs (object): Additional kwargs forwarded to every LiteLLM call.
    """

    __slots__ = ("_extra_kwargs", "_model")

    def __init__(
        self,
        *,
        model: str = DEFAULT_CHAT_MODEL,
        api_key: str | None = None,
        api_base: str | None = None,
        api_version: str | None = None,
        timeout: float | None = None,
        num_retries: int = _DEFAULT_NUM_RETRIES,
        drop_params: bool = True,
        **extra_kwargs: object,
    ) -> None:
        self._model = model
        self._extra_kwargs: dict[str, object] = {"drop_params": drop_params}
        if api_key is not None:
            self._extra_kwargs["api_key"] = api_key
        if api_base is not None:
            self._extra_kwargs["api_base"] = api_base
        if api_version is not None:
            self._extra_kwargs["api_version"] = api_version
        if timeout is not None:
            self._extra_kwargs["timeout"] = timeout
        if num_retries:
            self._extra_kwargs["num_retries"] = num_retries
        self._extra_kwargs.update(extra_kwargs)

        logger.info("LiteLLM adapter initialized: model=%s", model)

    @property
    def model(self) -> str:
        """Return the configured model string."""
        return self._model

    async def complete(
        self,
        *,
        prompt: str = "",
        system_prompt: str | None = None,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE,
        messages: list[dict[str, str]] | None = None,
        **kwargs: object,
    ) -> str:
        """Generate a completion via LiteLLM.

        Accepts either a simple 'prompt' string or a full
        'messages' list for multi-turn conversation.
        """
        import litellm

        msgs = self._build_messages(prompt, system_prompt, messages)
        call_kwargs: dict[str, object] = {
            "model": self._model,
            "messages": msgs,
            "max_tokens": max_tokens,
            "temperature": temperature,
            **self._extra_kwargs,
            **kwargs,
        }

        response = await litellm.acompletion(**call_kwargs)
        return response.choices[0].message.content or ""

    async def stream(
        self,
        *,
        prompt: str = "",
        system_prompt: str | None = None,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE,
        messages: list[dict[str, str]] | None = None,
        **kwargs: object,
    ) -> AsyncIterator[str]:
        """Stream completion chunks via LiteLLM."""
        import litellm

        msgs = self._build_messages(prompt, system_prompt, messages)
        call_kwargs: dict[str, object] = {
            "model": self._model,
            "messages": msgs,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": True,
            **self._extra_kwargs,
            **kwargs,
        }

        response = await litellm.acompletion(**call_kwargs)
        async for chunk in response:
            delta = chunk.choices[0].delta if chunk.choices else None
            if delta and delta.content:
                yield delta.content

    @classmethod
    def from_config(cls, config: dict[str, object]) -> LiteLLMAdapter:
        """Create a LiteLLMAdapter instance from a configuration dictionary.

        Expected config structure::

            {
                "model": "gpt-4o",
                "api_key": "sk-...",            # optional
                "api_base": "https://...",      # optional
                "api_version": "2024-02-01",    # optional
                "timeout": 30.0,                # optional
                "num_retries": 2,               # optional (default: 2)
                "drop_params": True,            # optional (default: True)
                "extra_kwarg_name": "value",    # optional extras
            }

        Args:
            config (dict[str, object]): Configuration dictionary.

        Returns:
            LiteLLMAdapter: Configured adapter instance.
        """
        model = str(config.get("model", DEFAULT_CHAT_MODEL))
        api_key = config.get("api_key")
        api_base = config.get("api_base")
        api_version = config.get("api_version")
        timeout = config.get("timeout")
        num_retries = int(config.get("num_retries", _DEFAULT_NUM_RETRIES))
        drop_params = bool(config.get("drop_params", True))

        # Collect any extra kwargs not already handled
        handled_keys = {
            "model", "api_key", "api_base", "api_version",
            "timeout", "num_retries", "drop_params",
        }
        extra_kwargs = {
            k: v for k, v in config.items() if k not in handled_keys
        }

        return cls(
            model=model,
            api_key=str(api_key) if api_key is not None else None,
            api_base=str(api_base) if api_base is not None else None,
            api_version=str(api_version) if api_version is not None else None,
            timeout=float(timeout) if timeout is not None else None,
            num_retries=num_retries,
            drop_params=drop_params,
            **extra_kwargs,
        )

    @staticmethod
    def _build_messages(
        prompt: str,
        system_prompt: str | None,
        messages: list[dict[str, str]] | None,
    ) -> list[dict[str, str]]:
        """Build a messages list from either a prompt or existing history."""
        if messages:
            return list(messages)
        msgs: list[dict[str, str]] = []
        if system_prompt:
            msgs.append({"role": "system", "content": system_prompt})
        if prompt:
            msgs.append({"role": "user", "content": prompt})
        return msgs

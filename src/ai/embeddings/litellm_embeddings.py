"""Universal embedding adapter via LiteLLM — one adapter for all providers.

Uses 'litellm.aembedding()' to route embedding requests to OpenAI,
Azure OpenAI, Cohere, Bedrock, Vertex AI, and other providers based
on the model string.

Model string examples::

    "text-embedding-3-small"                   # OpenAI
    "text-embedding-3-large"                   # OpenAI
    "azure/my-embedding-deployment"            # Azure OpenAI
    "cohere/embed-english-v3.0"                # Cohere
    "bedrock/amazon.titan-embed-text-v1"       # AWS Bedrock
    "vertex_ai/textembedding-gecko"            # Google Vertex
"""

from __future__ import annotations

import structlog
from typing import final

from ai.config import DEFAULT_EMBEDDING_DIMENSION, DEFAULT_EMBEDDING_MODEL
from core.interfaces.embedding import EmbeddingGateway

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)
@final
class LiteLLMEmbeddingAdapter(EmbeddingGateway):
    """Universal embedding adapter backed by LiteLLM.

    Provider-specific API keys are read from environment variables
    following LiteLLM conventions ('OPENAI_API_KEY', etc.).

    Args:
        model (str): LiteLLM model string for embeddings.
        dimension (int): Expected embedding vector dimension.
        api_key (str | None): Explicit API key (overrides env var).
        api_base (str | None): Custom API base URL.
        api_version (str | None): API version (Azure).
        timeout (float | None): Request timeout in seconds.
        extra_kwargs (object): Additional kwargs forwarded to every call.
    """

    __slots__ = ("_dimension", "_extra_kwargs", "_model")

    def __init__(
        self,
        *,
        model: str = DEFAULT_EMBEDDING_MODEL,
        dimension: int = DEFAULT_EMBEDDING_DIMENSION,
        api_key: str | None = None,
        api_base: str | None = None,
        api_version: str | None = None,
        timeout: float | None = None,
        **extra_kwargs: object,
    ) -> None:
        self._model = model
        self._dimension = dimension
        self._extra_kwargs: dict[str, object] = {}
        if api_key is not None:
            self._extra_kwargs["api_key"] = api_key
        if api_base is not None:
            self._extra_kwargs["api_base"] = api_base
        if api_version is not None:
            self._extra_kwargs["api_version"] = api_version
        if timeout is not None:
            self._extra_kwargs["timeout"] = timeout
        self._extra_kwargs.update(extra_kwargs)

        logger.info("LiteLLM embedding adapter initialized: model=%s, dim=%d", model, dimension)

    @property
    def model(self) -> str:
        """Return the configured embedding model string."""
        return self._model

    async def embed_text(self, text: str) -> list[float]:
        """Embed a single text string."""
        import litellm

        response = await litellm.aembedding(
            model=self._model,
            input=[text],
            **self._extra_kwargs,
        )
        return response.data[0]["embedding"]

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts in a single batch request."""
        import litellm

        response = await litellm.aembedding(
            model=self._model,
            input=texts,
            **self._extra_kwargs,
        )
        return [item["embedding"] for item in response.data]

    @property
    def dimension(self) -> int:
        """Return the embedding vector dimension."""
        return self._dimension

    @classmethod
    def from_config(cls, config: dict[str, object]) -> LiteLLMEmbeddingAdapter:
        """Create a LiteLLMEmbeddingAdapter instance from a configuration dictionary.

        Expected config structure::

            {
                "model": "text-embedding-3-small",
                "dimension": 1536,              # optional (default from config)
                "api_key": "sk-...",            # optional
                "api_base": "https://...",      # optional
                "api_version": "2024-02-01",    # optional
                "timeout": 30.0,                # optional
            }

        Args:
            config (dict[str, object]): Configuration dictionary.

        Returns:
            LiteLLMEmbeddingAdapter: Configured adapter instance.
        """
        model = str(config.get("model", DEFAULT_EMBEDDING_MODEL))
        dimension = int(config.get("dimension", DEFAULT_EMBEDDING_DIMENSION))
        api_key = config.get("api_key")
        api_base = config.get("api_base")
        api_version = config.get("api_version")
        timeout = config.get("timeout")

        # Collect any extra kwargs not already handled
        handled_keys = {
            "model", "dimension", "api_key", "api_base", "api_version", "timeout",
        }
        extra_kwargs = {
            k: v for k, v in config.items() if k not in handled_keys
        }

        return cls(
            model=model,
            dimension=dimension,
            api_key=str(api_key) if api_key is not None else None,
            api_base=str(api_base) if api_base is not None else None,
            api_version=str(api_version) if api_version is not None else None,
            timeout=float(timeout) if timeout is not None else None,
            **extra_kwargs,
        )

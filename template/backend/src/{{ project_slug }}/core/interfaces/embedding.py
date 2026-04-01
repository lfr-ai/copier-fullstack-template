"""Embedding gateway."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class EmbeddingGateway(Protocol):
    """Gateway for text-to-vector embedding providers."""

    @property
    def model(self) -> str:
        """Return the configured embedding model identifier."""
        ...

    async def embed_text(self, text: str) -> list[float]:
        """Embed a single text into a dense vector."""
        ...

    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Embed multiple texts into vectors."""
        ...

    @property
    def dimension(self) -> int:
        """Return the embedding vector dimension."""
        ...

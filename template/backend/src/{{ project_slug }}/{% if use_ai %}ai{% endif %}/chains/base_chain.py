"""Base chain -- abstract foundation for LLM chain compositions."""

from __future__ import annotations

from typing import final

import abc
import structlog

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)
@final
class ChainResult:
    """Result of a chain execution."""

    __slots__ = ("content", "metadata", "sources")

    def __init__(
        self,
        *,
        content: str = "",
        sources: list[dict[str, object]] | None = None,
        metadata: dict[str, object] | None = None,
    ) -> None:
        self.content = content
        self.sources = sources or []
        self.metadata = metadata or {}


class BaseChain(abc.ABC):
    """Abstract base for LLM chain compositions.

    Chains compose multiple LLM calls and/or retrieval
    operations into a multi-step pipeline.
    """

    @abc.abstractmethod
    async def run(self, *, input_text: str, **kwargs: object) -> ChainResult:
        """Execute the chain."""

    async def run_batch(
        self,
        *,
        inputs: list[str],
        **kwargs: object,
    ) -> list[ChainResult]:
        """Execute the chain on multiple inputs.

        Override for batch-optimized implementations.
        Default loops sequentially.
        """
        return [await self.run(input_text=text, **kwargs) for text in inputs]

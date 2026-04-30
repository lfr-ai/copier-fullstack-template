"""Chain gateway -- abstract interface for LLM chain compositions.

Chains compose multiple LLM calls, retrieval operations, or
tool invocations into multi-step pipelines. Concrete adapters
may use LangChain LCEL, LlamaIndex query engines, or custom
implementations.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class ChainGateway(Protocol):
    """Gateway for LLM chain compositions.

    Supports both batch and streaming execution modes.
    """

    async def run(self, *, input_text: str, **kwargs: object) -> object:
        """Execute the chain on the given input.

        Args:
            input_text (str): Primary input text (context, question, or document).
            **kwargs (object): Additional chain-specific parameters.

        Returns:
            object: Chain result (typically a ChainResult or dict).
        """
        ...

    async def run_batch(
        self,
        *,
        inputs: list[str],
        **kwargs: object,
    ) -> list[object]:
        """Execute the chain on multiple inputs.

        Default implementations loop sequentially, but concrete
        adapters can optimize for batch processing.
        """
        ...

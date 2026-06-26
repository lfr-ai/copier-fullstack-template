"""Tool gateway -- abstract interface for agent-callable tools.

Concrete adapters implement specific tools (web search, code execution,
database query, etc.) that agents can invoke during planning/execution.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class ToolGateway(Protocol):
    """Gateway for agent-callable tools.

    Each tool exposes a name, description, and parameter schema
    so agents can decide when and how to invoke it.
    """

    @property
    def name(self) -> str:
        """Unique tool identifier used for invocation."""
        ...

    @property
    def description(self) -> str:
        """Human-readable description of what the tool does."""
        ...

    @property
    def parameters_schema(self) -> dict[str, object]:
        """JSON Schema describing the tool's input parameters."""
        ...

    @property
    def output_schema(self) -> dict[str, object] | None:
        """Optional JSON Schema describing the tool's structured output."""
        ...

    async def execute(self, **kwargs: object) -> object:
        """Execute the tool with the given parameters.

        Returns:
            object: Tool execution result (string content, structured dict, or ToolResult).
        """
        ...

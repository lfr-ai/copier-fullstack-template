"""Base tool — abstract foundation for agent tools."""

from __future__ import annotations

import abc
import structlog

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)
class ToolResult:
    """Result of a tool execution."""

    __slots__ = ("content", "error", "metadata")

    def __init__(
        self,
        *,
        content: str = "",
        error: str | None = None,
        metadata: dict[str, object] | None = None,
    ) -> None:
        self.content = content
        self.error = error
        self.metadata = metadata or {}

    @property
    def is_error(self) -> bool:
        """Whether the tool execution resulted in an error."""
        return self.error is not None


class BaseTool(abc.ABC):
    """Abstract base class for agent-callable tools.

    Each tool has a name, description, and parameter schema
    that agents use to decide when and how to invoke it.
    """

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """Tool name used for invocation."""

    @property
    @abc.abstractmethod
    def description(self) -> str:
        """Human-readable description of what the tool does."""

    @property
    def parameters_schema(self) -> dict[str, object]:
        """JSON Schema for tool parameters.

        Override to provide structured parameter definitions.
        """
        return {}

    @property
    def output_schema(self) -> dict[str, object] | None:
        """Optional JSON Schema for structured tool output.

        When provided, MCP servers and agents can validate
        and parse tool results as structured data.
        """
        return None

    @abc.abstractmethod
    async def execute(self, **kwargs: object) -> ToolResult:
        """Execute the tool with the given parameters."""

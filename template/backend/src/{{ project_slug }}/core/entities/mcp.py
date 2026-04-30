"""MCP domain entities -- tool definitions, resources, results."""

from __future__ import annotations

from typing import final

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
@final
class ToolDefinition:
    """Definition of an MCP tool exposed by a server."""

    name: str = ""
    description: str = ""
    parameters: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
@final
class ToolResult:
    """Result of an MCP tool invocation."""

    tool_name: str = ""
    content: str = ""
    is_error: bool = False
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
@final
class ResourceDefinition:
    """Definition of an MCP resource served by a server."""

    uri: str = ""
    name: str = ""
    description: str = ""
    mime_type: str = "text/plain"


@dataclass(frozen=True, slots=True)
@final
class ResourceContent:
    """Content of an MCP resource."""

    uri: str = ""
    content: str = ""
    mime_type: str = "text/plain"

"""MCP client port — abstract interface for connecting to external MCP servers.

Concrete adapters use the official MCP Python SDK to communicate
via streamable-http, stdio, or SSE transports.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class MCPClientPort(Protocol):
    """Protocol for MCP client operations against external servers."""

    async def connect(
        self, *, server_url: str, transport: str = "streamable-http"
    ) -> None:
        """Establish connection to a remote MCP server.

        Args:
            server_url (str): URL of the MCP server.
            transport (str): Transport protocol (e.g. 'streamable-http', 'stdio').
        """
        ...

    async def disconnect(self) -> None:
        """Close the MCP server connection."""
        ...

    async def list_tools(self) -> list[dict[str, object]]:
        """List tools available on the connected server."""
        ...

    async def call_tool(
        self, *, name: str, arguments: dict[str, object] | None = None
    ) -> str:
        """Invoke a tool on the connected server.

        Args:
            name (str): Tool name.
            arguments (dict[str, object] | None): Tool arguments.

        Returns:
            str: Tool execution result.
        """
        ...

    async def list_resources(self) -> list[dict[str, object]]:
        """List resources available on the connected server."""
        ...

    async def read_resource(self, *, uri: str) -> str:
        """Read a resource from the connected server.

        Args:
            uri (str): Resource URI.

        Returns:
            str: Resource content.
        """
        ...

    async def list_prompts(self) -> list[dict[str, object]]:
        """List prompts available on the connected server."""
        ...

    async def get_prompt(
        self, *, name: str, arguments: dict[str, str] | None = None
    ) -> str:
        """Get a prompt from the connected server.

        Args:
            name (str): Prompt name.
            arguments (dict[str, str] | None): Prompt arguments.

        Returns:
            str: Prompt content.
        """
        ...

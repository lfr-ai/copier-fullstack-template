"""MCP client adapter."""

from __future__ import annotations

from typing import final

import structlog
from contextlib import AsyncExitStack

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)
@final
class MCPClientAdapter:
    """Client for connecting to external MCP servers.

    Implements tool calling, resource reading, and prompt
    invocation against remote MCP servers. Uses streamable-http
    transport by default (recommended for production by MCP SDK v1.26+).
    """

    __slots__ = ("_exit_stack", "_server_url", "_session", "_transport")

    def __init__(
        self,
        *,
        server_url: str = "",
        transport: str = "streamable-http",
    ) -> None:
        self._server_url = server_url
        self._transport = transport
        self._session: object | None = None
        self._exit_stack: AsyncExitStack | None = None

    async def connect(self, *, server_url: str = "", transport: str = "") -> None:
        """Establish connection to the MCP server.

        Args:
            server_url (str): Override the server URL set at init.
            transport (str): Override transport (streamable-http, sse, stdio).
        """
        url = server_url or self._server_url
        tp = transport or self._transport

        try:
            from mcp import ClientSession  # type: ignore[import-untyped]
        except ImportError as exc:
            msg = "mcp[cli]>=1.30 is required -- pip install 'mcp[cli]>=1.30'"
            raise ImportError(msg) from exc

        self._exit_stack = AsyncExitStack()

        if tp == "streamable-http" and url:
            from mcp.client.streamable_http import (
                streamable_http_client,  # type: ignore[import-untyped]
            )

            read_stream, write_stream, _ = await self._exit_stack.enter_async_context(
                streamable_http_client(url)
            )
        elif tp == "sse" and url:
            from mcp.client.sse import sse_client  # type: ignore[import-untyped]

            read_stream, write_stream = await self._exit_stack.enter_async_context(
                sse_client(url)
            )
        else:
            msg = f"Unsupported transport '{tp}' or missing server_url"
            raise ValueError(msg)

        self._session = await self._exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )
        await self._session.initialize()
        logger.info("MCP client connected via %s to %s", tp, url)

    async def disconnect(self) -> None:
        """Close the MCP server connection and clean up resources."""
        if self._exit_stack is not None:
            await self._exit_stack.aclose()
            self._exit_stack = None
        self._session = None
        logger.info("MCP client disconnected")

    async def list_tools(self) -> list[dict[str, object]]:
        """List tools available on the connected MCP server."""
        if self._session is None:
            msg = "Not connected. Call connect() first."
            raise RuntimeError(msg)
        result = await self._session.list_tools()
        return [
            {
                "name": t.name,
                "description": getattr(t, "description", ""),
                "parameters": getattr(t, "inputSchema", {}),
            }
            for t in result.tools
        ]

    async def call_tool(
        self,
        *,
        name: str,
        arguments: dict[str, object] | None = None,
    ) -> str:
        """Invoke a tool on the connected MCP server."""
        if self._session is None:
            msg = "Not connected. Call connect() first."
            raise RuntimeError(msg)
        result = await self._session.call_tool(name, arguments=arguments or {})
        logger.info("MCP tool called: %s", name)
        if result.content:
            return (
                str(result.content[0].text)
                if hasattr(result.content[0], "text")
                else str(result.content[0])
            )
        return ""

    async def list_resources(self) -> list[dict[str, object]]:
        """List resources available on the connected MCP server."""
        if self._session is None:
            msg = "Not connected. Call connect() first."
            raise RuntimeError(msg)
        result = await self._session.list_resources()
        return [
            {
                "uri": r.uri,
                "name": getattr(r, "name", ""),
                "description": getattr(r, "description", ""),
            }
            for r in result.resources
        ]

    async def read_resource(self, *, uri: str) -> str:
        """Read a resource from the connected MCP server."""
        if self._session is None:
            msg = "Not connected. Call connect() first."
            raise RuntimeError(msg)
        result = await self._session.read_resource(uri)
        if result.contents:
            return (
                str(result.contents[0].text)
                if hasattr(result.contents[0], "text")
                else str(result.contents[0])
            )
        return ""

    async def list_prompts(self) -> list[dict[str, object]]:
        """List prompts available on the connected MCP server."""
        if self._session is None:
            msg = "Not connected. Call connect() first."
            raise RuntimeError(msg)
        result = await self._session.list_prompts()
        return [
            {
                "name": p.name,
                "description": getattr(p, "description", ""),
                "arguments": [
                    {
                        "name": a.name,
                        "description": getattr(a, "description", ""),
                        "required": getattr(a, "required", False),
                    }
                    for a in (p.arguments or [])
                ],
            }
            for p in result.prompts
        ]

    async def get_prompt(
        self, *, name: str, arguments: dict[str, str] | None = None
    ) -> str:
        """Get a prompt from the connected MCP server."""
        if self._session is None:
            msg = "Not connected. Call connect() first."
            raise RuntimeError(msg)
        result = await self._session.get_prompt(name, arguments=arguments)
        if result.messages:
            content = result.messages[0].content
            return str(content.text) if hasattr(content, "text") else str(content)
        return ""

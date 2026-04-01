"""MCP server gateway — abstract interface for Model Context Protocol server lifecycle."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class MCPServerGateway(Protocol):
    """Gateway for managing an MCP server instance."""

    def create_app(self) -> object:
        """Create and return an ASGI-mountable MCP application.

        Returns:
            object: An ASGI application (e.g. Starlette or FastMCP app).
        """
        ...

    def streamable_http_app(self) -> object:
        """Return an ASGI app using streamable-http transport.

        Preferred for production (MCP SDK >= 1.26).

        Returns:
            object: An ASGI application.
        """
        ...

    async def start(self) -> None:
        """Start the MCP server."""
        ...

    async def stop(self) -> None:
        """Stop the MCP server and clean up resources."""
        ...

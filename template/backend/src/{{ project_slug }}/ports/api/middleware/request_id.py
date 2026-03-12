"""Request ID middleware for distributed tracing."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Final, override

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

if TYPE_CHECKING:
    from starlette.requests import Request
    from starlette.responses import Response

__all__ = ["RequestIdMiddleware"]

HEADER_REQUEST_ID: Final[str] = "X-Request-ID"


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Middleware injecting unique request ID into each response.

    Reads existing X-Request-ID header or generates a new UUID.
    """

    @override
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        """Process request with request ID injection.

        Args:
            request (Request): Incoming HTTP request.
            call_next (RequestResponseEndpoint): Next middleware or route handler.

        Returns:
            Response: HTTP response with X-Request-ID header.
        """
        request_id = request.headers.get(HEADER_REQUEST_ID, str(uuid.uuid4()))
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers[HEADER_REQUEST_ID] = request_id
        return response

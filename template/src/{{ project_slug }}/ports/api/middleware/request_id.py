"""Request ID middleware for distributed tracing."""

from __future__ import annotations

import uuid

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

HEADER_REQUEST_ID = "X-Request-ID"


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Middleware injecting unique request ID into each response.

    Reads existing X-Request-ID header or generates a new UUID.
    """

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        """Process request with request ID injection.

        Args:
            request: Incoming HTTP request.
            call_next: Next middleware or route handler.

        Returns:
            HTTP response with X-Request-ID header.
        """
        request_id = request.headers.get(HEADER_REQUEST_ID, str(uuid.uuid4()))
        response = await call_next(request)
        response.headers[HEADER_REQUEST_ID] = request_id
        return response

"""Request ID middleware for distributed tracing."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, override, final

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

if TYPE_CHECKING:
    from starlette.requests import Request
    from starlette.responses import Response


_HEADER_REQUEST_ID = "X-Request-ID"


@final
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
        """Process request with request ID injection."""
        raw_id = request.headers.get(_HEADER_REQUEST_ID, "")
        # Validate client-provided ID: accept only UUID-shaped values
        try:
            if raw_id:
                uuid.UUID(raw_id)
                request_id = raw_id
            else:
                request_id = str(uuid.uuid4())
        except ValueError:
            request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers[_HEADER_REQUEST_ID] = request_id
        return response

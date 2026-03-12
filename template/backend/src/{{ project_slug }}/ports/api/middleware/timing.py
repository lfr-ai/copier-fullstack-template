"""Timing middleware for request duration tracking and logging."""

from __future__ import annotations

__all__ = ["TimingMiddleware"]

import time
from typing import override

import structlog
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from {{ project_slug }}.config.constants import MS_PER_SECOND

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


class TimingMiddleware(BaseHTTPMiddleware):
    """Track request processing time, log it, and add Server-Timing header."""

    @override
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        """Process request, record timing, and log the result.

        Args:
            request (Request): Incoming HTTP request.
            call_next (RequestResponseEndpoint): Next middleware or route handler.

        Returns:
            Response: HTTP response with Server-Timing header.
        """
        start_time = time.perf_counter()

        response = await call_next(request)

        duration_ms = (time.perf_counter() - start_time) * MS_PER_SECOND

        response.headers["Server-Timing"] = f"total;dur={duration_ms:.1f}"

        logger.info(
            "request_completed",
            method=request.method,
            path=request.url.path,
            duration_ms=round(duration_ms, 2),
            status_code=response.status_code,
        )

        return response

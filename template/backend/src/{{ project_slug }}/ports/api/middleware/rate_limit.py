"""Rate limiting middleware using slowapi."""

from __future__ import annotations

from typing import TYPE_CHECKING, Final

from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

if TYPE_CHECKING:
    from fastapi import FastAPI, Request

__all__ = ["configure_rate_limiting", "limiter"]

DEFAULT_RATE_LIMIT: Final[str] = "60/minute"
HTTP_TOO_MANY_REQUESTS: Final[int] = 429

limiter: Final[Limiter] = Limiter(
    key_func=get_remote_address, default_limits=[DEFAULT_RATE_LIMIT]
)


async def _rate_limit_exceeded(
    request: Request, exc: RateLimitExceeded
) -> JSONResponse:
    """Return 429 response with Retry-After header.

    Args:
        request (Request): Incoming request.
        exc (RateLimitExceeded): The rate limit exception.

    Returns:
        JSONResponse: JSON error payload with appropriate status and header.
    """
    retry_after = getattr(exc, "retry_after", None)
    headers = {"Retry-After": str(retry_after)} if retry_after else {}
    return JSONResponse(
        status_code=HTTP_TOO_MANY_REQUESTS,
        content={"detail": "Rate limit exceeded"},
        headers=headers,
    )


def configure_rate_limiting(app: FastAPI) -> None:
    """Configure rate limiting on FastAPI app.

    Args:
        app (FastAPI): FastAPI application instance.
    """
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded)  # type: ignore[arg-type]

"""Rate limiting middleware using slowapi."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

if TYPE_CHECKING:
    from fastapi import FastAPI, Request


DEFAULT_RATE_LIMIT = "60/minute"
HTTP_TOO_MANY_REQUESTS = 429


def _get_real_client_ip(request: "Request") -> str:
    """Extract client IP respecting reverse proxy headers.

    Uses 'X-Forwarded-For' (first entry) when behind a trusted
    proxy (Caddy, nginx), falls back to 'request.client.host'.
    """
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return get_remote_address(request)


async def _rate_limit_exceeded(
    request: Request, exc: RateLimitExceeded
) -> JSONResponse:
    """Return 429 response with Retry-After header."""
    retry_after = getattr(exc, "retry_after", None)
    headers = {"Retry-After": str(retry_after)} if retry_after else {}
    return JSONResponse(
        status_code=HTTP_TOO_MANY_REQUESTS,
        content={"detail": "Rate limit exceeded"},
        headers=headers,
    )


def configure_rate_limiting(app: FastAPI) -> None:
    """Configure rate limiting on the FastAPI app.

    Uses 'rate_limit' from settings if available, otherwise
    falls back to :data:`DEFAULT_RATE_LIMIT`.

    Args:
        app (FastAPI): Application instance to configure.
    """
    settings = app.state.settings
    limit = getattr(settings, "rate_limit", DEFAULT_RATE_LIMIT)

    limiter = Limiter(key_func=_get_real_client_ip, default_limits=[limit])
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded)  # type: ignore[arg-type]

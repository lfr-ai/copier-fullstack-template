"""Rate limiting middleware using slowapi."""

from __future__ import annotations

from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

DEFAULT_RATE_LIMIT = "60/minute"

limiter = Limiter(key_func=get_remote_address, default_limits=[DEFAULT_RATE_LIMIT])


def configure_rate_limiting(app: FastAPI) -> None:
    """Configure rate limiting on FastAPI app.

    Args:
        app: FastAPI application instance.
    """
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

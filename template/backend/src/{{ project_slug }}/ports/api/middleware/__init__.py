"""API middleware stack.

Provides request-scoped middleware for security, observability, and error handling.
"""

from __future__ import annotations

from .error_handler import register_error_handlers
from .request_id import RequestIdMiddleware
from .security_headers import SecurityHeadersMiddleware
from .timing import TimingMiddleware

__all__ = [
    "RequestIdMiddleware",
    "SecurityHeadersMiddleware",
    "TimingMiddleware",
    "register_error_handlers",
]

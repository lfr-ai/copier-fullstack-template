"""Security headers middleware."""

from typing import override, final

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

_HSTS_MAX_AGE_SECONDS = 63_072_000  # 2 years


@final
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses.

    These headers provide defense-in-depth against common web vulnerabilities.
    In production, Caddy adds additional headers, but these serve as a fallback.
    """

    @override
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        """Process request and add security headers to response."""
        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "0"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=(), payment=()"
        )
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'"
        )

        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
        response.headers["Cache-Control"] = "no-store"

        if request.url.scheme == "https":
            response.headers["Strict-Transport-Security"] = (
                f"max-age={_HSTS_MAX_AGE_SECONDS}; includeSubDomains; preload"
            )

        return response

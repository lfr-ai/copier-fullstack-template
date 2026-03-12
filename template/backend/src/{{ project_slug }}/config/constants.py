"""Infrastructure constants — networking, API prefixes, pagination, security.

Domain validation constants (email lengths, password rules, etc.) live in
``core.constants``.  Import them from there directly.
"""

from __future__ import annotations

from typing import Final

__all__ = [
    "API_V1_PREFIX",
    "DEFAULT_FROM_ADDRESS",
    "DEFAULT_PAGE_SIZE",
    "DEFAULT_PORT",
    "DEFAULT_SMTP_PORT",
    "DEFAULT_TRUNCATE_LENGTH",
    "MAX_PAGE_SIZE",
    "MAX_PORT",
    "MS_PER_SECOND",
    "REFRESH_TOKEN_EXPIRY_DAYS",
    "TOKEN_EXPIRY_MINUTES",
]

API_V1_PREFIX: Final[str] = "/api/v1"
DEFAULT_PAGE_SIZE: Final[int] = 20
MAX_PAGE_SIZE: Final[int] = 100

DEFAULT_PORT: Final[int] = 8000
MAX_PORT: Final[int] = 65_535
DEFAULT_SMTP_PORT: Final[int] = 587
DEFAULT_FROM_ADDRESS: Final[str] = "noreply@example.com"
MS_PER_SECOND: Final[int] = 1_000

TOKEN_EXPIRY_MINUTES: Final[int] = 30
REFRESH_TOKEN_EXPIRY_DAYS: Final[int] = 7

DEFAULT_TRUNCATE_LENGTH: Final[int] = 100

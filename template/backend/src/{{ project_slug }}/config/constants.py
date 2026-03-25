"""Infrastructure constants — networking, API prefixes, pagination, security.

Domain validation constants (email lengths, password rules, etc.) live in
'core.constants'.  Import them from there directly.
"""

from __future__ import annotations

API_V1_PREFIX = "/api/v1"
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
MAX_PORT = 65_535
DEFAULT_SMTP_PORT = 587
DEFAULT_FROM_ADDRESS = "noreply@example.com"
MS_PER_SECOND = 1_000

TOKEN_EXPIRY_MINUTES = 30

DEFAULT_TRUNCATE_LENGTH = 100

PROFILING_INTERVAL = 0.001  # Pyinstrument sampling interval (seconds)

DEFAULT_CACHE_TTL_SECONDS = 3600  # 1 hour

"""Centralized retry policies using tenacity."""

from __future__ import annotations

from tenacity import retry, stop_after_attempt, wait_exponential

HTTP_RETRY_ATTEMPTS = 3
HTTP_BACKOFF_MULTIPLIER = 1.5
HTTP_BACKOFF_MIN = 2
HTTP_BACKOFF_MAX = 15

API_RETRY_ATTEMPTS = 5
API_BACKOFF_MULTIPLIER = 2.0
API_BACKOFF_MIN = 3
API_BACKOFF_MAX = 30

http_retry = retry(
    stop=stop_after_attempt(HTTP_RETRY_ATTEMPTS),
    wait=wait_exponential(
        multiplier=HTTP_BACKOFF_MULTIPLIER,
        min=HTTP_BACKOFF_MIN,
        max=HTTP_BACKOFF_MAX,
    ),
    reraise=True,
)
"""Retry decorator for general HTTP operations."""

api_retry = retry(
    stop=stop_after_attempt(API_RETRY_ATTEMPTS),
    wait=wait_exponential(
        multiplier=API_BACKOFF_MULTIPLIER,
        min=API_BACKOFF_MIN,
        max=API_BACKOFF_MAX,
    ),
    reraise=True,
)
"""Retry decorator for API calls with longer timeouts."""

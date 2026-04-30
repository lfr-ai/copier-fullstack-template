"""Centralized retry policies using tenacity."""

from __future__ import annotations

import logging  # noqa: LOG001 -- stdlib logger required by tenacity before_sleep_log

from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger: logging.Logger = logging.getLogger(__name__)

_HTTP_RETRY_ATTEMPTS = 3
_HTTP_BACKOFF_MULTIPLIER = 1.5
_HTTP_BACKOFF_MIN = 2.0
_HTTP_BACKOFF_MAX = 15.0

_API_RETRY_ATTEMPTS = 5
_API_BACKOFF_MULTIPLIER = 2.0
_API_BACKOFF_MIN = 3.0
_API_BACKOFF_MAX = 30.0

http_retry = retry(
    stop=stop_after_attempt(_HTTP_RETRY_ATTEMPTS),
    wait=wait_exponential(
        multiplier=_HTTP_BACKOFF_MULTIPLIER,
        min=_HTTP_BACKOFF_MIN,
        max=_HTTP_BACKOFF_MAX,
    ),
    reraise=True,
    before_sleep=before_sleep_log(logger, logging.WARNING),
    retry=retry_if_exception_type((ConnectionError, TimeoutError)),
)
"""Retry decorator for general HTTP operations with transient error filtering."""

api_retry = retry(
    stop=stop_after_attempt(_API_RETRY_ATTEMPTS),
    wait=wait_exponential(
        multiplier=_API_BACKOFF_MULTIPLIER,
        min=_API_BACKOFF_MIN,
        max=_API_BACKOFF_MAX,
    ),
    reraise=True,
    before_sleep=before_sleep_log(logger, logging.WARNING),
    retry=retry_if_exception_type(
        (ConnectionError, TimeoutError, ConnectionResetError, BrokenPipeError)
    ),
)
"""Retry decorator for API calls with longer timeouts and broader error matching."""

"""Centralized retry policies using tenacity."""

from __future__ import annotations

import logging  # noqa: LOG001 — stdlib logger required by tenacity before_sleep_log

from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger: logging.Logger = logging.getLogger(__name__)

HTTP_RETRY_ATTEMPTS = 3
HTTP_BACKOFF_MULTIPLIER = 1.5
HTTP_BACKOFF_MIN = 2.0
HTTP_BACKOFF_MAX = 15.0

API_RETRY_ATTEMPTS = 5
API_BACKOFF_MULTIPLIER = 2.0
API_BACKOFF_MIN = 3.0
API_BACKOFF_MAX = 30.0

http_retry = retry(
    stop=stop_after_attempt(HTTP_RETRY_ATTEMPTS),
    wait=wait_exponential(
        multiplier=HTTP_BACKOFF_MULTIPLIER,
        min=HTTP_BACKOFF_MIN,
        max=HTTP_BACKOFF_MAX,
    ),
    reraise=True,
    before_sleep=before_sleep_log(logger, logging.WARNING),
    retry=retry_if_exception_type((ConnectionError, TimeoutError)),
)
"""Retry decorator for general HTTP operations with transient error filtering."""

api_retry = retry(
    stop=stop_after_attempt(API_RETRY_ATTEMPTS),
    wait=wait_exponential(
        multiplier=API_BACKOFF_MULTIPLIER,
        min=API_BACKOFF_MIN,
        max=API_BACKOFF_MAX,
    ),
    reraise=True,
    before_sleep=before_sleep_log(logger, logging.WARNING),
    retry=retry_if_exception_type(
        (ConnectionError, TimeoutError, ConnectionResetError, BrokenPipeError)
    ),
)
"""Retry decorator for API calls with longer timeouts and broader error matching."""

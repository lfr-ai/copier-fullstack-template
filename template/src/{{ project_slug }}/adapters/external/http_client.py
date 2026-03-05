"""Async HTTP client adapter for external service calls."""

from __future__ import annotations

import logging

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential


logger = logging.getLogger(__name__)
MAX_RETRY_ATTEMPTS = 3
BACKOFF_MULTIPLIER = 1.5
BACKOFF_MIN_WAIT = 2
BACKOFF_MAX_WAIT = 15
DEFAULT_TIMEOUT_SECONDS = 30.0


class HTTPClientAdapter:
    """Async HTTP client with retry support.

    Wraps httpx.AsyncClient with tenacity retry policies
    for resilient external API communication.
    """

    def __init__(
        self,
        *,
        base_url: str = "",
        timeout: float = DEFAULT_TIMEOUT_SECONDS,
        headers: dict[str, str] | None = None,
    ) -> None:
        """Initialize HTTP client adapter.

        Args:
            base_url: Base URL for all requests.
            timeout: Request timeout in seconds.
            headers: Default request headers.
        """
        self._client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            headers=headers or {},
        )

    async def close(self) -> None:
        """Close underlying HTTP client."""
        await self._client.aclose()

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(
            multiplier=BACKOFF_MULTIPLIER,
            min=BACKOFF_MIN_WAIT,
            max=BACKOFF_MAX_WAIT,
        ),
        reraise=True,
    )
    async def get(self, url: str, **kwargs: object) -> httpx.Response:
        """Send GET request with retry policy.

        Args:
            url: Request URL (appended to base_url).
            **kwargs: Additional httpx request arguments.

        Returns:
            HTTP response.
        """
        response = await self._client.get(url, **kwargs)
        response.raise_for_status()
        return response

    @retry(
        stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
        wait=wait_exponential(
            multiplier=BACKOFF_MULTIPLIER,
            min=BACKOFF_MIN_WAIT,
            max=BACKOFF_MAX_WAIT,
        ),
        reraise=True,
    )
    async def post(self, url: str, **kwargs: object) -> httpx.Response:
        """Send POST request with retry policy.

        Args:
            url: Request URL (appended to base_url).
            **kwargs: Additional httpx request arguments.

        Returns:
            HTTP response.
        """
        response = await self._client.post(url, **kwargs)
        response.raise_for_status()
        return response

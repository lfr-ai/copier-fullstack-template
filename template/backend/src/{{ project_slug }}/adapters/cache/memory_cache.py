"""In-memory cache adapter for development and testing."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Final

__all__ = ["MemoryCacheAdapter"]

_DEFAULT_TTL_SECONDS: Final[int] = 3600


@dataclass(frozen=True, slots=True)
class _CacheEntry:
    """Internal cache entry with value and expiration."""

    value: str
    expires_at: float


class MemoryCacheAdapter:
    """Simple in-memory cache implementing CachePort.

    Provides TTL-based expiration with lazy cleanup.
    Suitable for development and testing environments.
    """

    def __init__(self) -> None:
        """Initialize empty in-memory cache."""
        self._store: dict[str, _CacheEntry] = {}

    async def get(self, key: str) -> str | None:
        """Retrieve value from memory cache.

        Args:
            key (str): Cache key.

        Returns:
            str | None: Cached string value or None if not found or expired.
        """
        entry = self._store.get(key)
        if entry is None:
            return None
        if time.monotonic() > entry.expires_at:
            del self._store[key]
            return None
        return entry.value

    async def set(
        self,
        *,
        key: str,
        value: str,
        ttl_seconds: int | None = None,
    ) -> None:
        """Store value in memory cache with TTL.

        Args:
            key (str): Cache key.
            value (str): String value to store.
            ttl_seconds (int | None): Time-to-live in seconds; uses default if None.
        """
        effective_ttl = ttl_seconds if ttl_seconds is not None else _DEFAULT_TTL_SECONDS
        expires_at = time.monotonic() + effective_ttl
        self._store[key] = _CacheEntry(value=value, expires_at=expires_at)

    async def delete(self, key: str) -> bool:
        """Remove value from memory cache.

        Args:
            key (str): Cache key.

        Returns:
            bool: True if key was removed.
        """
        return self._store.pop(key, None) is not None

    async def exists(self, key: str) -> bool:
        """Check if non-expired key exists.

        Args:
            key (str): Cache key.

        Returns:
            bool: True if key exists and is not expired.
        """
        result = await self.get(key)
        return result is not None

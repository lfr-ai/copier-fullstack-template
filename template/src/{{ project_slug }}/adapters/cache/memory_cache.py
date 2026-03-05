"""In-memory cache adapter for development and testing."""

from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class _CacheEntry:
    """Internal cache entry with value and expiration."""

    value: object
    expires_at: float


class MemoryCacheAdapter:
    """Simple in-memory cache implementing CachePort.

    Provides TTL-based expiration with lazy cleanup.
    Suitable for development and testing environments.
    """

    def __init__(self) -> None:
        """Initialize empty in-memory cache."""
        self._store: dict[str, _CacheEntry] = {}

    async def get(self, key: str) -> object | None:
        """Retrieve value from memory cache.

        Args:
            key: Cache key.

        Returns:
            Cached value or None if not found or expired.
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
        key: str,
        value: object,
        *,
        ttl: int = 3600,
    ) -> None:
        """Store value in memory cache with TTL.

        Args:
            key: Cache key.
            value: Value to store.
            ttl: Time-to-live in seconds.
        """
        expires_at = time.monotonic() + ttl
        self._store[key] = _CacheEntry(value=value, expires_at=expires_at)

    async def delete(self, key: str) -> bool:
        """Remove value from memory cache.

        Args:
            key: Cache key.

        Returns:
            True if key was removed.
        """
        return self._store.pop(key, None) is not None

    async def exists(self, key: str) -> bool:
        """Check if non-expired key exists.

        Args:
            key: Cache key.

        Returns:
            True if key exists and is not expired.
        """
        result = await self.get(key)
        return result is not None

"""Redis cache adapter implementation."""

from __future__ import annotations

import json
import logging

from redis.asyncio import Redis


logger = logging.getLogger(__name__)
DEFAULT_TTL_SECONDS = 3600


class RedisCacheAdapter:
    """Redis-backed cache adapter implementing CachePort.

    Provides get/set/delete/exists with automatic JSON
    serialization and configurable TTL.
    """

    def __init__(self, client: Redis, *, default_ttl: int = DEFAULT_TTL_SECONDS) -> None:
        """Initialize redis cache adapter.

        Args:
            client: Async Redis client instance.
            default_ttl: Default time-to-live in seconds.
        """
        self._client = client
        self._default_ttl = default_ttl

    async def get(self, key: str) -> object | None:
        """Retrieve value from cache by key.

        Args:
            key: Cache key.

        Returns:
            Deserialized value or None if not found.
        """
        raw = await self._client.get(key)
        if raw is None:
            return None
        return json.loads(raw)

    async def set(
        self,
        key: str,
        value: object,
        *,
        ttl: int | None = None,
    ) -> None:
        """Store value in cache with optional TTL.

        Args:
            key: Cache key.
            value: Value to cache, must be JSON-serializable.
            ttl: Time-to-live in seconds; uses default if None.
        """
        effective_ttl = ttl if ttl is not None else self._default_ttl
        serialized = json.dumps(value, default=str)
        await self._client.setex(key, effective_ttl, serialized)
        logger.debug("Cache SET key=%s ttl=%d", key, effective_ttl)

    async def delete(self, key: str) -> bool:
        """Remove value from cache.

        Args:
            key: Cache key.

        Returns:
            True if key was deleted.
        """
        result = await self._client.delete(key)
        return bool(result)

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache.

        Args:
            key: Cache key.

        Returns:
            True if key exists.
        """
        result = await self._client.exists(key)
        return bool(result)

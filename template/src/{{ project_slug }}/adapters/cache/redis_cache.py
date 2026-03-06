"""Redis cache adapter implementation."""

from __future__ import annotations

import logging
from typing import Final

from redis.asyncio import Redis

logger = logging.getLogger(__name__)

DEFAULT_TTL_SECONDS: Final[int] = 3600
CACHE_KEY_PREFIX: Final[str] = "app:cache"


class RedisCacheAdapter:
    """Redis-backed cache adapter implementing CachePort.

    Provides get/set/delete/exists with structured key
    prefixing and configurable TTL.
    """

    def __init__(
        self,
        client: Redis,  # type: ignore[type-arg]
        *,
        key_prefix: str = CACHE_KEY_PREFIX,
        default_ttl: int = DEFAULT_TTL_SECONDS,
    ) -> None:
        """Initialize redis cache adapter.

        Args:
            client: Async Redis client instance.
            key_prefix: Prefix for all cache keys.
            default_ttl: Default time-to-live in seconds.
        """
        self._client = client
        self._key_prefix = key_prefix
        self._default_ttl = default_ttl

    def _build_key(self, key: str) -> str:
        """Build fully qualified cache key with prefix.

        Args:
            key: Raw cache key.

        Returns:
            Prefixed cache key.
        """
        return f"{self._key_prefix}:{key}"

    async def get(self, key: str) -> str | None:
        """Retrieve cached value by key.

        Args:
            key: Cache key.

        Returns:
            Cached string value or None if not found.
        """
        result = await self._client.get(self._build_key(key))
        if result is not None:
            logger.debug("Cache hit for key %s", key)
        else:
            logger.debug("Cache miss for key %s", key)
        return result

    async def set(
        self,
        key: str,
        value: str,
        *,
        ttl_seconds: int | None = None,
    ) -> None:
        """Store value in cache with TTL.

        Args:
            key: Cache key.
            value: String value to cache.
            ttl_seconds: Time-to-live in seconds; uses default if None.
        """
        effective_ttl = ttl_seconds if ttl_seconds is not None else self._default_ttl
        await self._client.setex(
            name=self._build_key(key),
            time=effective_ttl,
            value=value,
        )
        logger.debug("Cache SET key=%s ttl=%d", key, effective_ttl)

    async def delete(self, key: str) -> bool:
        """Remove value from cache.

        Args:
            key: Cache key.

        Returns:
            True if key was deleted.
        """
        result = await self._client.delete(self._build_key(key))
        return bool(result)

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache.

        Args:
            key: Cache key.

        Returns:
            True if key exists.
        """
        result = await self._client.exists(self._build_key(key))
        return bool(result)

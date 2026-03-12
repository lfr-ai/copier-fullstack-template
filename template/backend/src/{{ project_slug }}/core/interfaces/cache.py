"""Cache protocol for abstracted caching operations."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

__all__ = ["CachePort"]


@runtime_checkable
class CachePort(Protocol):
    """Protocol for cache operations."""

    async def get(self, key: str) -> str | None:
        """Retrieve cached value by key.

        Args:
            key (str): Cache key.

        Returns:
            str | None: Cached string value or None if not found.
        """
        ...

    async def set(
        self,
        *,
        key: str,
        value: str,
        ttl_seconds: int | None = None,
    ) -> None:
        """Store value in cache.

        Args:
            key (str): Cache key.
            value (str): String value to cache.
            ttl_seconds (int | None): Time-to-live in seconds.
        """
        ...

    async def delete(self, key: str) -> bool:
        """Remove cached value.

        Args:
            key (str): Cache key.

        Returns:
            bool: True if key was deleted.
        """
        ...

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache.

        Args:
            key (str): Cache key.

        Returns:
            bool: True if key exists.
        """
        ...

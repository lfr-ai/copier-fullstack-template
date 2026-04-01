"""Cache gateway for abstracted caching operations."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class CacheGateway(Protocol):
    """Gateway for cache operations."""

    async def get(self, key: str) -> str | None:
        """Retrieve cached value by key."""
        ...

    async def set(
        self,
        *,
        key: str,
        value: str,
        ttl_seconds: int | None = None,
    ) -> None:
        """Store value in cache."""
        ...

    async def delete(self, key: str) -> bool:
        """Remove cached value."""
        ...

    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        ...

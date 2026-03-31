"""Storage gateway — contract for binary object storage."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from typing import BinaryIO


@runtime_checkable
class StorageGateway(Protocol):
    """Gateway for binary object storage operations.

    Adapters must implement this gateway to integrate with a
    storage backend (local filesystem, Azure Blob Storage, etc.).
    """

    async def upload(self, *, key: str, data: BinaryIO) -> str:
        """Upload binary data and return the URI or path of the stored object."""
        ...

    async def download(self, key: str) -> bytes:
        """Download object by key and return raw bytes."""
        ...

    async def delete(self, key: str) -> None:
        """Delete object by key."""
        ...

    async def exists(self, key: str) -> bool:
        """Check whether an object exists."""
        ...

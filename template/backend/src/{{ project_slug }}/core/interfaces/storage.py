"""Storage port — contract for binary object storage."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from typing import BinaryIO

__all__ = ["StoragePort"]


@runtime_checkable
class StoragePort(Protocol):
    """Port for binary object storage operations.

    Adapters must implement this protocol to integrate with a
    storage backend (local filesystem, Azure Blob Storage, etc.).
    """

    async def upload(self, *, key: str, data: BinaryIO) -> str:
        """Upload binary data under the given key.

        Args:
            key: Object key (path) in the storage backend.
            data: Binary stream to upload.

        Returns:
            URI or path of the uploaded object.
        """
        ...

    async def download(self, key: str) -> bytes:
        """Download object by key and return raw bytes.

        Args:
            key: Object key (path) in the storage backend.

        Returns:
            Raw bytes of the downloaded object.
        """
        ...

    async def delete(self, key: str) -> None:
        """Delete object by key.

        Args:
            key: Object key (path) in the storage backend.
        """
        ...

    async def exists(self, key: str) -> bool:
        """Check whether an object exists.

        Args:
            key: Object key (path) in the storage backend.

        Returns:
            True if the object exists.
        """
        ...

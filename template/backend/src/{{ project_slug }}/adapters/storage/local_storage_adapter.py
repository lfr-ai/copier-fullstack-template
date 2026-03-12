"""Local filesystem storage adapter."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import BinaryIO

import structlog

__all__ = ["LocalStorageAdapter"]

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


class LocalStorageAdapter:
    """Store and retrieve files on the local filesystem.

    Implements the storage service interface defined in core.
    """

    __slots__ = ("_base_path",)

    def __init__(self, base_path: str | Path) -> None:
        """Initialize with base directory for file storage.

        Args:
            base_path (str | Path): Root directory for stored files.
        """
        self._base_path = Path(base_path)
        self._base_path.mkdir(parents=True, exist_ok=True)

    async def upload(self, *, key: str, data: BinaryIO) -> str:
        """Write data to a local file and return the path.

        Args:
            key (str): Relative file path within the base directory.
            data (BinaryIO): Binary stream to write.

        Returns:
            str: Absolute path of the stored file.
        """
        dest = self._base_path / key
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("wb") as f:
            shutil.copyfileobj(data, f)
        logger.info("Stored file locally: %s", dest)
        return str(dest)

    async def download(self, key: str) -> bytes:
        """Read a file from the local filesystem.

        Args:
            key (str): Relative file path within the base directory.

        Returns:
            bytes: Raw bytes of the file contents.
        """
        path = self._base_path / key
        return path.read_bytes()

    async def delete(self, key: str) -> None:
        """Remove a file from the local filesystem.

        Args:
            key (str): Relative file path within the base directory.
        """
        path = self._base_path / key
        path.unlink(missing_ok=True)
        logger.info("Deleted local file: %s", key)

    async def exists(self, key: str) -> bool:
        """Check whether a file exists.

        Args:
            key (str): Relative file path within the base directory.

        Returns:
            bool: True if the file exists.
        """
        return (self._base_path / key).exists()

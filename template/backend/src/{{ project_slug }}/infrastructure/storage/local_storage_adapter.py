"""Local filesystem storage adapter."""

from __future__ import annotations

import asyncio
import shutil
from pathlib import Path
from typing import BinaryIO, final

import structlog

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


@final
class LocalStorageAdapter:
    """Store and retrieve files on the local filesystem.

    Implements the storage service interface defined in core.
    All file I/O is offloaded to a thread to avoid blocking the
    async event loop.
    """

    __slots__ = ("_base_path",)

    def __init__(self, base_path: str | Path) -> None:
        """Args:
        base_path (str | Path): Root directory for stored files.
        """
        self._base_path = Path(base_path)
        self._base_path.mkdir(parents=True, exist_ok=True)

    def _safe_path(self, key: str) -> Path:
        """Resolve a key to a path safely within the base directory.

        Raises:
            ValueError: If the key escapes the base directory.
        """
        resolved = (self._base_path / key).resolve()
        if not resolved.is_relative_to(self._base_path.resolve()):
            msg = f"Path traversal denied: {key!r}"
            raise ValueError(msg)
        return resolved

    def _sync_upload(self, key: str, data: BinaryIO) -> str:
        dest = self._safe_path(key)
        dest.parent.mkdir(parents=True, exist_ok=True)
        with dest.open("wb") as f:
            shutil.copyfileobj(data, f)
        return str(dest)

    async def upload(self, *, key: str, data: BinaryIO) -> str:
        """Write data to a local file and return the path.

        Args:
            key (str): Relative file path within the base directory.
            data (BinaryIO): Binary stream to write.

        Returns:
            str: Absolute path of the stored file.
        """
        result = await asyncio.to_thread(self._sync_upload, key, data)
        logger.info("Stored file locally: %s", result)
        return result

    async def download(self, key: str) -> bytes:
        """Read a file from the local filesystem.

        Args:
            key (str): Relative file path within the base directory.

        Returns:
            bytes: Raw bytes of the file contents.
        """
        path = self._safe_path(key)
        return await asyncio.to_thread(path.read_bytes)

    async def delete(self, key: str) -> None:
        """Remove a file from the local filesystem.

        Args:
            key (str): Relative file path within the base directory.
        """
        path = self._safe_path(key)
        await asyncio.to_thread(path.unlink, True)  # missing_ok=True
        logger.info("Deleted local file: %s", key)

    async def exists(self, key: str) -> bool:
        """Check whether a file exists.

        Args:
            key (str): Relative file path within the base directory.

        Returns:
            bool: 'True' if the file exists.
        """
        path = self._safe_path(key)
        return await asyncio.to_thread(path.exists)

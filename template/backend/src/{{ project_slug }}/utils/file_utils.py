"""File-system utility helpers."""

import hashlib
from pathlib import Path

_READ_CHUNK_SIZE = 8192


def ensure_directory(path: Path) -> Path:
    """Create *path* (and parents) if it does not exist, then return it.

    Args:
        path (Path): Directory path to create.

    Returns:
        Path: The same *path*, guaranteed to exist.
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def file_sha256(path: Path, *, chunk_size: int = _READ_CHUNK_SIZE) -> str:
    """Return the hex SHA-256 digest of a file.

    Args:
        path (Path): File to hash.
        chunk_size (int): Read buffer size in bytes.

    Returns:
        str: Lowercase hex-encoded SHA-256 digest string.
    """
    h = hashlib.sha256()
    with path.open("rb") as fh:
        while chunk := fh.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def safe_filename(name: str) -> str:
    """Sanitize *name* so it is safe as a filesystem path component.

    Args:
        name (str): Raw filename string.

    Returns:
        str: Sanitized filename with unsafe characters replaced by underscores.
    """
    keep = {" ", ".", "-", "_"}
    result = (
        "".join(c if (c.isalnum() or c in keep) else "_" for c in name)
        .strip()
        .lstrip(".")
    )
    return result or "_unnamed"

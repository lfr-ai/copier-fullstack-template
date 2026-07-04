"""Internal helpers for scanning and reading Python-like source files.

These helpers keep validation scripts consistent while avoiding repeated file
iteration and decoding logic.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

_PYTHON_LIKE_SUFFIXES = (".py", ".py.jinja")


def is_python_like_file(*, path: Path) -> bool:
    """Return whether 'path' is a Python or Python-Jinja file.

    Args:
        path (Path): Candidate filesystem path.

    Returns:
        bool: True when file suffix matches supported Python-like suffixes.
    """
    return path.is_file() and path.name.endswith(_PYTHON_LIKE_SUFFIXES)


def _iter_scan_candidates(*, root: Path) -> Iterator[Path]:
    """Yield candidate paths to evaluate under one scan root.

    Args:
        root (Path): Directory or file passed to the scanner.

    Yields:
        Iterator[Path]: Candidate file-system paths for suffix filtering.
    """
    if root.is_file():
        yield root
        return
    if not root.exists():
        return
    yield from root.rglob("*")


def iter_python_like_files(*, roots: list[Path]) -> list[Path]:
    """Collect Python-like files from the provided roots.

    Args:
        roots (list[Path]): Directories or files to scan.

    Returns:
        list[Path]: Sorted, de-duplicated Python-like file paths.
    """
    files = {
        candidate
        for root in roots
        for candidate in _iter_scan_candidates(root=root)
        if is_python_like_file(path=candidate)
    }
    return sorted(files)


def read_text_ignore_errors(*, path: Path) -> str:
    """Read UTF-8 text from 'path' and ignore undecodable bytes.

    Args:
        path (Path): File path to read.

    Returns:
        str: Decoded file contents.
    """
    return path.read_text(encoding="utf-8", errors="ignore")

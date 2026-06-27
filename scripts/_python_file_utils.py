"""Internal helpers for scanning and reading Python-like source files.

These helpers keep validation scripts consistent while avoiding repeated file
iteration and decoding logic.
"""

from __future__ import annotations

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


def iter_python_like_files(*, roots: list[Path]) -> list[Path]:
    """Collect Python-like files from the provided roots.

    Args:
        roots (list[Path]): Directories or files to scan.

    Returns:
        list[Path]: Sorted, de-duplicated Python-like file paths.
    """
    files: set[Path] = set()
    for root in roots:
        if root.is_file():
            if is_python_like_file(path=root):
                files.add(root)
            continue
        if not root.exists():
            continue
        for candidate in root.rglob("*"):
            if is_python_like_file(path=candidate):
                files.add(candidate)
    return sorted(files)


def read_text_ignore_errors(*, path: Path) -> str:
    """Read UTF-8 text from 'path' and ignore undecodable bytes.

    Args:
        path (Path): File path to read.

    Returns:
        str: Decoded file contents.
    """
    return path.read_text(encoding="utf-8", errors="ignore")

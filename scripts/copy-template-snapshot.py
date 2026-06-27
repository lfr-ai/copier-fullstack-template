"""Create a VCS-free copy of the template source for rendering."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil

_IGNORED = {
    ".git",
    ".venv",
    "node_modules",
    ".mypy_cache",
    ".ruff_cache",
    ".pytest_cache",
    "__pycache__",
}


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed CLI arguments.
    """
    parser = argparse.ArgumentParser(
        description="Create a VCS-free snapshot copy of the repository.",
    )
    parser.add_argument(
        "src",
        nargs="?",
        default=".",
        help="Source directory to copy (defaults to current directory).",
    )
    parser.add_argument("dst", help="Destination directory for the snapshot.")
    parser.add_argument(
        "exclude",
        nargs="?",
        default=None,
        help="Optional path to exclude entirely from the copy.",
    )
    return parser.parse_args()


def _make_ignore_fn(*, exclude: Path | None):
    """Build a 'copytree' ignore callback.

    Args:
        exclude (Path | None): Directory to exclude fully, if any.

    Returns:
        callable: Ignore callback compatible with 'shutil.copytree'.
    """

    def _ignore(path: str, names: list[str]) -> set[str]:
        current = Path(path).resolve()
        if exclude and current == exclude:
            return set(names)
        return {name for name in names if name in _IGNORED}

    return _ignore


def main() -> int:
    """Create snapshot copy using parsed CLI arguments.

    Returns:
        int: Process exit code.
    """
    args = _parse_args()
    src = Path(args.src).resolve()
    dst = Path(args.dst)
    exclude = Path(args.exclude).resolve() if args.exclude else None

    shutil.copytree(
        src,
        dst,
        ignore=_make_ignore_fn(exclude=exclude),
        dirs_exist_ok=True,
    )
    print(f"[OK] Template snapshot created at {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

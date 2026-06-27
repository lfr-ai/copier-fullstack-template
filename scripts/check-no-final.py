"""Verify no Final[] type annotations on module-level constants.

Applies to public and internal constants/variables.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from _python_file_utils import iter_python_like_files, read_text_ignore_errors

_FINAL_ANNOTATION_PATTERN = re.compile(r"^[A-Z_][A-Z0-9_]*\s*:\s*Final", re.MULTILINE)
_DEFAULT_ROOT = Path("template/backend/src")


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed CLI arguments.
    """
    parser = argparse.ArgumentParser(
        description="Fail when module-level constants use Final annotations.",
    )
    parser.add_argument(
        "root",
        nargs="?",
        default=str(_DEFAULT_ROOT),
        help="Root folder to scan recursively.",
    )
    return parser.parse_args()


def _collect_offenders(*, root: Path) -> list[str]:
    """Collect files containing module-level 'Final' annotations.

    Args:
        root (Path): Root folder to scan recursively.

    Returns:
        list[str]: Offending file paths formatted with POSIX separators.
    """
    offenders: list[str] = []
    for file_path in iter_python_like_files(roots=[root]):
        text = read_text_ignore_errors(path=file_path)
        if _FINAL_ANNOTATION_PATTERN.search(text):
            offenders.append(file_path.as_posix())
    return offenders


def main() -> int:
    """Run no-'Final' validation and print diagnostics.

    Returns:
        int: Process exit code.
    """
    args = _parse_args()
    root = Path(args.root)
    offenders = _collect_offenders(root=root)

    if offenders:
        print("[FAIL] Found Final[] annotations on module-level constants/variables:")
        for file_path in offenders:
            print(f"  - {file_path}")
        return 1

    print("[OK] No Final[] type annotations on module-level constants/variables")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

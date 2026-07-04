"""Verify FastAPI status-code conventions in API layer.

Rules:
- Never use numeric literals in 'status_code=...'.
- Never import status from Starlette.
- Always use FastAPI status constants (for example: status.HTTP_200_OK).
"""

from __future__ import annotations

from pathlib import Path
import re
import sys

from _python_file_utils import iter_python_like_files, read_text_ignore_errors


_NUMERIC_STATUS_CODE_PATTERN = re.compile(r"\bstatus_code\s*=\s*\d{3}\b")
_STARLETTE_STATUS_IMPORT_PATTERN = re.compile(
    r"^\s*(?:from\s+starlette(?:\.status)?\s+import\s+status|import\s+starlette\.status)\b",
    re.MULTILINE,
)


def _scan_file(*, file_path: Path) -> list[str]:
    """Scan one file and return convention violations.

    Args:
        file_path (Path): File path to inspect.

    Returns:
        list[str]: List of human-readable violations.
    """
    text = read_text_ignore_errors(path=file_path)
    violations: list[str] = []

    if _NUMERIC_STATUS_CODE_PATTERN.search(text):
        violations.append("Numeric HTTP status code literal found in status_code=...")

    if _STARLETTE_STATUS_IMPORT_PATTERN.search(text):
        violations.append(
            "Status import from Starlette detected; use 'from fastapi import status'"
        )

    return violations


def _resolve_root_path(*, argv: list[str]) -> Path:
    """Resolve scan root path from command-line arguments.

    Args:
        argv (list[str]): Raw process argument list.

    Returns:
        Path: Root path to scan for violations.
    """
    return Path(argv[1]) if len(argv) > 1 else Path("template/backend/src")


def _collect_offenders(*, root: Path) -> dict[Path, list[str]]:
    """Collect files violating FastAPI status-code conventions.

    Args:
        root (Path): Root directory to scan.

    Returns:
        dict[Path, list[str]]: Offending files mapped to their violations.
    """
    offenders: dict[Path, list[str]] = {}
    for file_path in iter_python_like_files(roots=[root]):
        file_violations = _scan_file(file_path=file_path)
        if not file_violations:
            continue
        offenders[file_path] = file_violations
    return offenders


def _print_result(*, offenders: dict[Path, list[str]]) -> int:
    """Print checker result and return process exit code.

    Args:
        offenders (dict[Path, list[str]]): Collected offending files.

    Returns:
        int: Exit code (0 when clean, 1 when violations exist).
    """
    if offenders:
        print("[FAIL] FastAPI status-code convention violations found:")
        for file_path, file_violations in offenders.items():
            print(f"  - {file_path.as_posix()}")
            for violation in file_violations:
                print(f"      * {violation}")
        return 1
    print("[OK] FastAPI status-code conventions satisfied")
    return 0


def main() -> int:
    """Run FastAPI status-code convention checks.

    Returns:
        int: Process exit code.
    """
    root = _resolve_root_path(argv=sys.argv)
    offenders = _collect_offenders(root=root)
    return _print_result(offenders=offenders)


if __name__ == "__main__":
    raise SystemExit(main())

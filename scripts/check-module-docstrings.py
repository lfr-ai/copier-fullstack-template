"""Enforce module-level docstrings for Python-like files.

Checks Python source files and Python Jinja templates and fails when a module
docstring is missing as the first significant statement.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from _python_file_utils import iter_python_like_files, read_text_ignore_errors

_DEFAULT_PATHS = ("scripts", "template/backend/src", "template/tools")
_INIT_MODULE_NAMES = frozenset({"__init__.py", "__init__.py.jinja"})
_TOP_JINJA_LINE_PATTERN = re.compile(r"^\s*{[%#].*[%#]}\s*$")
_STRING_START_PATTERN = re.compile(r"\s*(?:[rubfRUBF]{,2})?('''|\"\"\")")
_ENCODING_PATTERN = re.compile(r"^\s*#.*coding[:=]")


def _is_ignorable_preamble_line(*, stripped_line: str) -> bool:
    """Return whether a top-of-file line is ignorable before module code.

    Args:
        stripped_line (str): Line text with surrounding whitespace removed.

    Returns:
        bool: True when the line is blank/comment/shebang/encoding/Jinja control.
    """
    if not stripped_line:
        return True
    if stripped_line.startswith("#!"):
        return True
    if _ENCODING_PATTERN.match(stripped_line):
        return True
    if stripped_line.startswith("#"):
        return True
    return _TOP_JINJA_LINE_PATTERN.match(stripped_line) is not None


def _has_module_docstring(*, text: str) -> bool:
    """Return whether module text has a top-level module docstring.

    Args:
        text (str): Full module source text.

    Returns:
        bool: True when first significant statement is a triple-quoted string.
    """
    for line in text.splitlines():
        stripped_line = line.strip()
        if _is_ignorable_preamble_line(stripped_line=stripped_line):
            continue
        return _STRING_START_PATTERN.match(line) is not None
    return False


def _should_skip_file(*, file_path: Path, allow_init: bool) -> bool:
    """Return whether a file should be excluded from docstring checking.

    Args:
        file_path (Path): Candidate Python-like file path.
        allow_init (bool): Whether '__init__' modules are included.

    Returns:
        bool: True when the file should not be checked.
    """
    return not allow_init and file_path.name in _INIT_MODULE_NAMES


def _collect_missing_docstrings(*, files: list[Path], allow_init: bool) -> list[str]:
    """Collect files that are missing a valid module docstring.

    Args:
        files (list[Path]): Python-like files to evaluate.
        allow_init (bool): Whether '__init__' modules are included.

    Returns:
        list[str]: Offending file paths in POSIX form.
    """
    offenders: list[str] = []
    for file_path in files:
        if _should_skip_file(file_path=file_path, allow_init=allow_init):
            continue
        text = read_text_ignore_errors(path=file_path)
        if not _has_module_docstring(text=text):
            offenders.append(file_path.as_posix())
    return offenders


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Enforce module-level docstrings in Python-like files.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=list(_DEFAULT_PATHS),
        help="Paths to scan recursively. Defaults to scripts, template/backend/src, template/tools.",
    )
    parser.add_argument(
        "--allow-init",
        action="store_true",
        help="Include __init__.py files in the check. Disabled by default.",
    )
    return parser.parse_args()


def main() -> int:
    """Run module-docstring validation.

    Returns:
        int: Process exit code.
    """
    args = _parse_args()
    roots = [Path(raw_path) for raw_path in args.paths]
    files = iter_python_like_files(roots=roots)
    offenders = _collect_missing_docstrings(files=files, allow_init=args.allow_init)

    if offenders:
        print("[FAIL] Missing module-level docstring in:")
        for offender in offenders:
            print(f"  - {offender}")
        return 1

    print("[OK] Module-level docstrings are present")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

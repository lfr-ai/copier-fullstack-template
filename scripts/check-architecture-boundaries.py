"""Verify backend layer import boundaries for Clean Architecture."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from _python_file_utils import iter_python_like_files, read_text_ignore_errors

_LAYER_ORDER: dict[str, int] = {
    "utils": 0,
    "config": 1,
    "core": 2,
    "application": 3,
    "infrastructure": 4,
    "ai": 5,
    "presentation": 6,
    "composition": 7,
}
_ALLOWED_CROSS_LAYER_IMPORTS: dict[str, frozenset[str]] = {
    "presentation": frozenset({"application", "core", "config", "utils", "ai"}),
    "infrastructure": frozenset({"core", "config", "utils"}),
    "application": frozenset({"core", "config", "utils"}),
    "core": frozenset({"utils"}),
    "config": frozenset({"utils"}),
    # AI remains orchestration/domain-facing; infrastructure wiring stays in composition.
    "ai": frozenset({"core", "config", "utils"}),
}
_IMPORT_RE = re.compile(r"^\s*(?:from|import)\s+([A-Za-z0-9_\.]+)", re.MULTILINE)


def _detect_layer(*, path: Path) -> str | None:
    """Infer architecture layer from file path.

    Args:
        path (Path): Source file path.

    Returns:
        str | None: Layer name when found, otherwise None.
    """
    parts = path.as_posix().split("/")
    for layer_name in _LAYER_ORDER:
        if layer_name in parts:
            return layer_name
    return None


def _extract_layer_imports(*, text: str) -> set[str]:
    """Extract first-party layer imports from source text.

    Args:
        text (str): File contents.

    Returns:
        set[str]: Imported layer names.
    """
    imported_layers: set[str] = set()
    for module_name in _IMPORT_RE.findall(text):
        for layer_name in _LAYER_ORDER:
            if f".{layer_name}" in module_name or module_name.endswith(layer_name):
                imported_layers.add(layer_name)
    return imported_layers


def _is_violation(*, source_layer: str, target_layer: str) -> bool:
    """Determine whether an import violates configured layer direction.

    Args:
        source_layer (str): Layer of importing file.
        target_layer (str): Imported layer.

    Returns:
        bool: True when import is forbidden.
    """
    if source_layer == target_layer or source_layer == "composition":
        return False
    if target_layer in _ALLOWED_CROSS_LAYER_IMPORTS.get(source_layer, frozenset()):
        return False
    return _LAYER_ORDER[target_layer] > _LAYER_ORDER[source_layer]


def _resolve_root_path(*, argv: list[str]) -> Path:
    """Resolve the scan root path from CLI arguments.

    Args:
        argv (list[str]): Raw process arguments.

    Returns:
        Path: Root path for architecture scanning.
    """
    return Path(argv[1]) if len(argv) > 1 else Path("template/backend/src")


def _find_violating_targets(*, source_layer: str, text: str) -> list[str]:
    """Return violating imported layers for one source file.

    Args:
        source_layer (str): Layer containing the current file.
        text (str): File contents to inspect.

    Returns:
        list[str]: Sorted violating target layer names.
    """
    imported_layers = _extract_layer_imports(text=text)
    return sorted(
        target
        for target in imported_layers
        if _is_violation(source_layer=source_layer, target_layer=target)
    )


def _collect_boundary_violations(*, root: Path) -> list[str]:
    """Collect architecture boundary violations under one scan root.

    Args:
        root (Path): Root directory to scan.

    Returns:
        list[str]: Human-readable violation lines.
    """
    offenders: list[str] = []
    for file_path in iter_python_like_files(roots=[root]):
        source_layer = _detect_layer(path=file_path)
        if source_layer is None:
            continue
        text = read_text_ignore_errors(path=file_path)
        violating_targets = _find_violating_targets(
            source_layer=source_layer, text=text
        )
        if not violating_targets:
            continue
        offenders.append(
            f"{file_path.as_posix()}  [{source_layer} -> {', '.join(violating_targets)}]"
        )
    return offenders


def _print_result(*, offenders: list[str]) -> int:
    """Print architecture-check result and return process exit code.

    Args:
        offenders (list[str]): Collected violation lines.

    Returns:
        int: Exit code (0 when clean, 1 when violations exist).
    """
    if offenders:
        print("[FAIL] Architecture boundary violations detected:")
        for offender in offenders:
            print(f"  - {offender}")
        return 1
    print("[OK] Architecture boundary imports comply with configured rules")
    return 0


def main() -> int:
    """Validate architecture boundary imports and print diagnostics.

    Returns:
        int: Process exit code.
    """
    root = _resolve_root_path(argv=sys.argv)
    offenders = _collect_boundary_violations(root=root)
    return _print_result(offenders=offenders)


if __name__ == "__main__":
    raise SystemExit(main())

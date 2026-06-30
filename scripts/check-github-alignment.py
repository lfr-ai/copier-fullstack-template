"""Verify agentic governance alignment rules in a cross-platform way."""

from __future__ import annotations

import json
from collections.abc import Sequence
from pathlib import Path

_ROOT_HOOKS_CONFIG = ".github/hooks/hooks.json"
_TEMPLATE_HOOKS_CONFIG = "template/.github/hooks/hooks.json"
_EXPECTED_HOOK_COMMANDS: dict[str, tuple[str, str]] = {
    "PreToolUse": (
        ".github/hooks/scripts/guard-tool.sh",
        "powershell -ExecutionPolicy Bypass -File .github\\hooks\\scripts\\guard-tool.ps1",
    ),
    "Stop": (
        ".github/hooks/scripts/check-licenses.sh",
        "powershell -ExecutionPolicy Bypass -File .github\\hooks\\scripts\\check-licenses.ps1",
    ),
}
_OWNERSHIP_MATRIX_PATH = "docs/cross-cuttings/agentic-ownership-map.json"
_REQUIRED_FILES_KEY = "requiredFiles"
_LEGACY_FILES_KEY = "legacyFiles"
_AGENTIC_SCAN_PATHS_KEY = "agenticPathsToScan"
_MIRRORS_KEY = "mirrors"


def _collect_missing(*, repo_root: Path, required_files: Sequence[str]) -> list[str]:
    """Collect required alignment files that are currently missing.

    Args:
        repo_root (Path): Repository root path.
        required_files (Sequence[str]): Required file paths to check.

    Returns:
        list[str]: Missing required file paths.
    """

    missing: list[str] = []
    for relative_path in required_files:
        if not (repo_root / relative_path).is_file():
            missing.append(relative_path)
    return missing


def _collect_legacy_present(
    *, repo_root: Path, legacy_files: Sequence[str]
) -> list[str]:
    """Collect forbidden legacy files that are still present.

    Args:
        repo_root (Path): Repository root path.
        legacy_files (Sequence[str]): Legacy file paths that must not exist.

    Returns:
        list[str]: Legacy file paths that should be removed.
    """

    present: list[str] = []
    for relative_path in legacy_files:
        if (repo_root / relative_path).is_file():
            present.append(relative_path)
    return present


def _build_project_specific_tokens(*, repo_root: Path) -> tuple[str, ...]:
    """Build dynamic project-local tokens to reject in agentic assets.

    Args:
        repo_root (Path): Repository root path.

    Returns:
        tuple[str, ...]: Project-specific token values.
    """

    resolved_root = repo_root.resolve()
    tail_parts = resolved_root.parts[-3:]
    tail_posix = "/".join(tail_parts)
    tail_windows = "\\".join(tail_parts)

    tokens = {
        resolved_root.name,
        resolved_root.as_posix(),
        str(resolved_root).replace("/", "\\"),
        tail_posix,
        tail_windows,
    }
    return tuple(sorted(token for token in tokens if token))


def _validate_hook_entries(
    *,
    hooks: dict[str, object],
    relative_path: str,
) -> list[str]:
    """Validate expected hook command entries for one hooks config file.

    Args:
        hooks (dict[str, object]): Parsed 'hooks' mapping.
        relative_path (str): Config path used for diagnostics.

    Returns:
        list[str]: Validation failures for this config.
    """

    violations: list[str] = []
    for hook_name, (
        expected_command,
        expected_windows,
    ) in _EXPECTED_HOOK_COMMANDS.items():
        first_entry, error_message = _get_first_hook_entry(
            hooks=hooks,
            hook_name=hook_name,
            relative_path=relative_path,
        )
        if error_message is not None:
            violations.append(error_message)
            continue

        current_command = first_entry.get("command")
        current_windows = first_entry.get("windows")
        if current_command != expected_command:
            violations.append(
                f"{relative_path} '{hook_name}' command is '{current_command}', expected '{expected_command}'"
            )
        if current_windows != expected_windows:
            violations.append(
                f"{relative_path} '{hook_name}' windows command is '{current_windows}', expected '{expected_windows}'"
            )
    return violations


def _get_first_hook_entry(
    *,
    hooks: dict[str, object],
    hook_name: str,
    relative_path: str,
) -> tuple[dict[str, object], str | None]:
    """Return the first hook entry and any validation error message.

    Args:
        hooks (dict[str, object]): Parsed 'hooks' mapping.
        hook_name (str): Hook section name to inspect.
        relative_path (str): Config path used for diagnostics.

    Returns:
        tuple[dict[str, object], str | None]: First hook entry mapping and
            optional error message when missing or malformed.
    """

    entries_obj = hooks.get(hook_name)
    if not isinstance(entries_obj, list) or not entries_obj:
        return {}, f"Missing '{hook_name}' hook in {relative_path}"

    first_entry = entries_obj[0]
    if not isinstance(first_entry, dict):
        return (
            {},
            f"Invalid '{hook_name}' hook in {relative_path}: expected object entry",
        )

    normalized_entry = {str(key): value for key, value in first_entry.items()}
    return normalized_entry, None


def _scan_candidate_for_project_tokens(
    *,
    candidate: Path,
    repo_root: Path,
    suffixes: set[str],
    tokens: tuple[str, ...],
) -> list[str]:
    """Scan a single file for project-specific tokens.

    Args:
        candidate (Path): File to inspect.
        repo_root (Path): Repository root for relative formatting.
        suffixes (set[str]): File extensions to include.
        tokens (tuple[str, ...]): Project-specific token values to detect.

    Returns:
        list[str]: Token findings for this candidate file.
    """

    if not candidate.is_file() or candidate.suffix not in suffixes:
        return []

    findings: list[str] = []
    content = candidate.read_text(encoding="utf-8", errors="ignore")
    for token in tokens:
        if token in content:
            findings.append(
                f"{candidate.relative_to(repo_root)} contains project-specific token '{token}'"
            )
    return findings


def _collect_hook_path_violations(*, repo_root: Path) -> list[str]:
    """Validate hook command paths in root and template hook configs.

    Args:
        repo_root (Path): Repository root path.

    Returns:
        list[str]: Human-readable hook path violations.
    """

    violations: list[str] = []
    for relative_path in (_ROOT_HOOKS_CONFIG, _TEMPLATE_HOOKS_CONFIG):
        config_path = repo_root / relative_path
        if not config_path.is_file():
            violations.append(f"Missing hooks config: {relative_path}")
            continue

        try:
            parsed = json.loads(config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            violations.append(f"Invalid JSON in {relative_path}: {error}")
            continue

        hooks = parsed.get("hooks", {})
        violations.extend(
            _validate_hook_entries(hooks=hooks, relative_path=relative_path)
        )

    return violations


def _collect_project_specific_agentic_refs(
    *,
    repo_root: Path,
    agentic_paths_to_scan: Sequence[str],
) -> list[str]:
    """Detect project-specific repository tokens in agentic assets.

    Args:
        repo_root (Path): Repository root path.
        agentic_paths_to_scan (Sequence[str]): Agentic directories to inspect.

    Returns:
        list[str]: File-level findings with token matches.
    """

    findings: list[str] = []
    suffixes = {".md", ".jinja", ".json", ".yaml", ".yml", ".toml"}
    tokens = _build_project_specific_tokens(repo_root=repo_root)

    for relative_directory in agentic_paths_to_scan:
        directory = repo_root / relative_directory
        if not directory.exists():
            continue

        for candidate in directory.rglob("*"):
            findings.extend(
                _scan_candidate_for_project_tokens(
                    candidate=candidate,
                    repo_root=repo_root,
                    suffixes=suffixes,
                    tokens=tokens,
                )
            )

    return findings


def _load_ownership_matrix(
    *,
    repo_root: Path,
) -> tuple[dict[str, object] | None, list[str]]:
    """Load ownership matrix JSON as a normalized object.

    Args:
        repo_root (Path): Repository root path.

    Returns:
        tuple[dict[str, object] | None, list[str]]: Matrix object and
            matrix-level violations.
    """

    matrix_path = repo_root / _OWNERSHIP_MATRIX_PATH
    if not matrix_path.is_file():
        return None, [f"Missing ownership matrix: {_OWNERSHIP_MATRIX_PATH}"]

    try:
        matrix_obj = json.loads(matrix_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return None, [f"Invalid JSON in {_OWNERSHIP_MATRIX_PATH}: {error}"]

    if not isinstance(matrix_obj, dict):
        return (
            None,
            [f"Invalid ownership matrix in {_OWNERSHIP_MATRIX_PATH}: expected object"],
        )

    return {str(key): value for key, value in matrix_obj.items()}, []


def _load_matrix_path_list(
    *,
    matrix_obj: dict[str, object],
    key: str,
) -> tuple[tuple[str, ...], list[str]]:
    """Load one matrix top-level string-list field.

    Args:
        matrix_obj (dict[str, object]): Parsed matrix object.
        key (str): Top-level key to parse.

    Returns:
        tuple[tuple[str, ...], list[str]]: Normalized values and violations.
    """

    values_obj = matrix_obj.get(key)
    if not isinstance(values_obj, list):
        return (
            (),
            [
                f"Invalid ownership matrix in {_OWNERSHIP_MATRIX_PATH}: '{key}' must be list"
            ],
        )

    values: list[str] = []
    violations: list[str] = []
    for index, value_obj in enumerate(values_obj):
        if not isinstance(value_obj, str):
            violations.append(
                f"Invalid ownership matrix entry in '{key}' at index {index}: expected string"
            )
            continue

        value = value_obj.strip()
        if not value:
            violations.append(
                f"Invalid ownership matrix entry in '{key}' at index {index}: value cannot be empty"
            )
            continue
        values.append(value)

    return tuple(values), violations


def _load_ownership_mirrors(
    *,
    matrix_obj: dict[str, object],
) -> tuple[list[dict[str, object]], list[str]]:
    """Load and minimally validate ownership-matrix mirror entries.

    Args:
        matrix_obj (dict[str, object]): Parsed matrix object.

    Returns:
        tuple[list[dict[str, object]], list[str]]: Normalized mirror entries and
            matrix-level violations.
    """

    mirrors_obj = matrix_obj.get(_MIRRORS_KEY)
    if not isinstance(mirrors_obj, list):
        return (
            [],
            [
                f"Invalid ownership matrix in {_OWNERSHIP_MATRIX_PATH}: '{_MIRRORS_KEY}' must be list"
            ],
        )

    mirrors: list[dict[str, object]] = []
    violations: list[str] = []
    for mirror_index, mirror_obj in enumerate(mirrors_obj):
        if not isinstance(mirror_obj, dict):
            violations.append(
                f"Invalid mirror entry at index {mirror_index} in {_OWNERSHIP_MATRIX_PATH}: expected object"
            )
            continue

        mirrors.append({str(key): value for key, value in mirror_obj.items()})

    return mirrors, violations


def _parse_mirror_pair(
    *,
    pair_obj: object,
    mirror_name: str,
    pair_index: int,
) -> tuple[tuple[str, str] | None, str | None]:
    """Validate and normalize one [rootRel, templateRel] pair.

    Args:
        pair_obj (object): Raw pair object from matrix.
        mirror_name (str): Mirror entry name for diagnostics.
        pair_index (int): Pair index for diagnostics.

    Returns:
        tuple[tuple[str, str] | None, str | None]: Parsed pair and optional
            validation error.
    """

    if not isinstance(pair_obj, list):
        return (
            None,
            f"Invalid pair at {mirror_name}[{pair_index}] in {_OWNERSHIP_MATRIX_PATH}: expected [rootRel, templateRel]",
        )
    if len(pair_obj) != 2:
        return (
            None,
            f"Invalid pair at {mirror_name}[{pair_index}] in {_OWNERSHIP_MATRIX_PATH}: expected [rootRel, templateRel]",
        )

    root_rel_obj, template_rel_obj = pair_obj
    if not isinstance(root_rel_obj, str) or not isinstance(template_rel_obj, str):
        return (
            None,
            f"Invalid pair at {mirror_name}[{pair_index}] in {_OWNERSHIP_MATRIX_PATH}: expected [rootRel, templateRel]",
        )

    return (root_rel_obj, template_rel_obj), None


def _collect_mirror_base_path_violations(
    *,
    mirror_name: str,
    root_base: Path,
    template_base: Path,
    root_base_obj: str,
    template_base_obj: str,
) -> list[str]:
    """Collect violations for missing mirror base directories.

    Args:
        mirror_name (str): Mirror entry name for diagnostics.
        root_base (Path): Root mirror base path.
        template_base (Path): Template mirror base path.
        root_base_obj (str): Root base path text from matrix.
        template_base_obj (str): Template base path text from matrix.

    Returns:
        list[str]: Base-path validation violations.
    """

    violations: list[str] = []
    if not root_base.exists():
        violations.append(
            f"Missing mirror root base for '{mirror_name}': {root_base_obj}"
        )
    if not template_base.exists():
        violations.append(
            f"Missing mirror template base for '{mirror_name}': {template_base_obj}"
        )
    return violations


def _collect_missing_mirror_asset_violations(
    *,
    mirror_name: str,
    root_path: Path,
    template_path: Path,
    root_base_obj: str,
    template_base_obj: str,
    root_rel: str,
    template_rel: str,
    required_in_root: bool,
    required_in_template: bool,
    optional: bool,
) -> list[str]:
    """Collect violations for missing mirror assets in one pair.

    Args:
        mirror_name (str): Mirror entry name for diagnostics.
        root_path (Path): Candidate root mirror path.
        template_path (Path): Candidate template mirror path.
        root_base_obj (str): Root base path text from matrix.
        template_base_obj (str): Template base path text from matrix.
        root_rel (str): Root-relative asset path from matrix.
        template_rel (str): Template-relative asset path from matrix.
        required_in_root (bool): Whether root asset presence is required.
        required_in_template (bool): Whether template asset presence is required.
        optional (bool): Whether this mirror pair is optional in both locations.

    Returns:
        list[str]: Missing-asset violations for this pair.
    """

    if optional:
        return []

    violations: list[str] = []
    if required_in_root and not root_path.exists():
        violations.append(
            f"Missing mirrored root asset for '{mirror_name}': {root_base_obj}/{root_rel}"
        )
    if required_in_template and not template_path.exists():
        violations.append(
            f"Missing mirrored template asset for '{mirror_name}': {template_base_obj}/{template_rel}"
        )
    return violations


def _collect_mirror_pair_violations(
    *,
    mirror_name: str,
    root_base: Path,
    template_base: Path,
    root_base_obj: str,
    template_base_obj: str,
    pairs_obj: Sequence[object],
    required_in_root: bool,
    required_in_template: bool,
    optional: bool,
) -> list[str]:
    """Collect violations for all mirror pairs in one mirror entry.

    Args:
        mirror_name (str): Mirror entry name for diagnostics.
        root_base (Path): Root mirror base path.
        template_base (Path): Template mirror base path.
        root_base_obj (str): Root base path text from matrix.
        template_base_obj (str): Template base path text from matrix.
        pairs_obj (list[object]): Mirror pair entries.
        required_in_root (bool): Whether root assets are required.
        required_in_template (bool): Whether template assets are required.
        optional (bool): Whether mirror pairs are optional.

    Returns:
        list[str]: Pair-level validation violations.
    """

    violations: list[str] = []
    for pair_index, pair_obj in enumerate(pairs_obj):
        pair, error_message = _parse_mirror_pair(
            pair_obj=pair_obj,
            mirror_name=mirror_name,
            pair_index=pair_index,
        )
        if error_message is not None:
            violations.append(error_message)
            continue
        if pair is None:
            continue

        root_rel, template_rel = pair
        root_path = root_base / root_rel
        template_path = template_base / template_rel
        violations.extend(
            _collect_missing_mirror_asset_violations(
                mirror_name=mirror_name,
                root_path=root_path,
                template_path=template_path,
                root_base_obj=root_base_obj,
                template_base_obj=template_base_obj,
                root_rel=root_rel,
                template_rel=template_rel,
                required_in_root=required_in_root,
                required_in_template=required_in_template,
                optional=optional,
            )
        )

    return violations


def _collect_mirror_entry_violations(
    *,
    repo_root: Path,
    mirror_obj: dict[str, object],
    mirror_index: int,
) -> list[str]:
    """Validate one mirror entry from the ownership matrix.

    Args:
        repo_root (Path): Repository root path.
        mirror_obj (dict[str, object]): Mirror entry object.
        mirror_index (int): Mirror entry index for diagnostics.

    Returns:
        list[str]: Violations for this mirror entry.
    """

    mirror_name = str(mirror_obj.get("name", f"mirror[{mirror_index}]"))
    root_base_obj = mirror_obj.get("rootBase")
    template_base_obj = mirror_obj.get("templateBase")
    pairs_obj = mirror_obj.get("pairs")
    required_in_root_obj = mirror_obj.get("requiredInRoot", True)
    required_in_template_obj = mirror_obj.get("requiredInTemplate", True)
    optional_obj = mirror_obj.get("optional", False)

    if not isinstance(root_base_obj, str) or not isinstance(template_base_obj, str):
        return [
            f"Invalid '{mirror_name}' in {_OWNERSHIP_MATRIX_PATH}: 'rootBase' and 'templateBase' must be strings"
        ]
    if not isinstance(pairs_obj, list):
        return [
            f"Invalid '{mirror_name}' in {_OWNERSHIP_MATRIX_PATH}: 'pairs' must be list"
        ]
    if not isinstance(required_in_root_obj, bool):
        return [
            f"Invalid '{mirror_name}' in {_OWNERSHIP_MATRIX_PATH}: 'requiredInRoot' must be bool"
        ]
    if not isinstance(required_in_template_obj, bool):
        return [
            f"Invalid '{mirror_name}' in {_OWNERSHIP_MATRIX_PATH}: 'requiredInTemplate' must be bool"
        ]
    if not isinstance(optional_obj, bool):
        return [
            f"Invalid '{mirror_name}' in {_OWNERSHIP_MATRIX_PATH}: 'optional' must be bool"
        ]

    root_base = repo_root / root_base_obj
    template_base = repo_root / template_base_obj
    base_violations = _collect_mirror_base_path_violations(
        mirror_name=mirror_name,
        root_base=root_base,
        template_base=template_base,
        root_base_obj=root_base_obj,
        template_base_obj=template_base_obj,
    )
    if base_violations:
        return base_violations

    return _collect_mirror_pair_violations(
        mirror_name=mirror_name,
        root_base=root_base,
        template_base=template_base,
        root_base_obj=root_base_obj,
        template_base_obj=template_base_obj,
        pairs_obj=pairs_obj,
        required_in_root=required_in_root_obj,
        required_in_template=required_in_template_obj,
        optional=optional_obj,
    )


def _collect_mirror_drift_violations(
    *,
    repo_root: Path,
    mirrors: Sequence[dict[str, object]],
) -> list[str]:
    """Validate critical root/template mirror pairs from ownership matrix.

    Args:
        repo_root (Path): Repository root path.
        mirrors (Sequence[dict[str, object]]): Mirror entries from matrix.

    Returns:
        list[str]: Violations for missing/invalid mirror entries.
    """

    violations: list[str] = []
    for mirror_index, mirror_obj in enumerate(mirrors):
        violations.extend(
            _collect_mirror_entry_violations(
                repo_root=repo_root,
                mirror_obj=mirror_obj,
                mirror_index=mirror_index,
            )
        )

    return violations


def _build_failure_messages(
    *,
    missing_files: list[str],
    legacy_files: list[str],
    hook_path_violations: list[str],
    project_specific_refs: list[str],
    mirror_drift_violations: list[str],
) -> list[str]:
    """Build normalized failure messages for all alignment checks.

    Args:
        missing_files (list[str]): Required files that are absent.
        legacy_files (list[str]): Deprecated files that still exist.
        hook_path_violations (list[str]): Hook-path validation findings.
        project_specific_refs (list[str]): Project-token findings in agentic assets.
        mirror_drift_violations (list[str]): Root/template mirror drift findings.

    Returns:
        list[str]: Human-readable failures with stable prefixes.
    """

    failures: list[str] = []
    failures.extend(
        f"Missing required alignment file: {relative_path}"
        for relative_path in missing_files
    )
    failures.extend(
        f"Legacy file found: {relative_path} (should be removed)"
        for relative_path in legacy_files
    )
    failures.extend(hook_path_violations)
    failures.extend(project_specific_refs)
    failures.extend(mirror_drift_violations)
    return failures


def main() -> int:
    """Execute agentic alignment checks.

    Returns:
        int: Exit code (0 when alignment passes, 1 otherwise).
    """

    print("Checking agentic core alignment (agents/hooks/instructions/skills)...")
    repo_root = Path(__file__).resolve().parents[1]

    matrix_obj, matrix_violations = _load_ownership_matrix(repo_root=repo_root)

    required_files: tuple[str, ...] = ()
    legacy_files: tuple[str, ...] = ()
    agentic_paths_to_scan: tuple[str, ...] = ()
    mirrors: list[dict[str, object]] = []
    policy_violations = list(matrix_violations)

    if matrix_obj is not None:
        required_files, required_violations = _load_matrix_path_list(
            matrix_obj=matrix_obj,
            key=_REQUIRED_FILES_KEY,
        )
        legacy_files, legacy_violations = _load_matrix_path_list(
            matrix_obj=matrix_obj,
            key=_LEGACY_FILES_KEY,
        )
        agentic_paths_to_scan, scan_path_violations = _load_matrix_path_list(
            matrix_obj=matrix_obj,
            key=_AGENTIC_SCAN_PATHS_KEY,
        )
        mirrors, mirror_policy_violations = _load_ownership_mirrors(
            matrix_obj=matrix_obj
        )
        policy_violations.extend(required_violations)
        policy_violations.extend(legacy_violations)
        policy_violations.extend(scan_path_violations)
        policy_violations.extend(mirror_policy_violations)

    missing_files = _collect_missing(
        repo_root=repo_root,
        required_files=required_files,
    )
    present_legacy_files = _collect_legacy_present(
        repo_root=repo_root,
        legacy_files=legacy_files,
    )
    hook_path_violations = _collect_hook_path_violations(repo_root=repo_root)
    project_specific_refs = _collect_project_specific_agentic_refs(
        repo_root=repo_root,
        agentic_paths_to_scan=agentic_paths_to_scan,
    )
    mirror_drift_violations = [
        *policy_violations,
        *_collect_mirror_drift_violations(repo_root=repo_root, mirrors=mirrors),
    ]

    failures = _build_failure_messages(
        missing_files=missing_files,
        legacy_files=present_legacy_files,
        hook_path_violations=hook_path_violations,
        project_specific_refs=project_specific_refs,
        mirror_drift_violations=mirror_drift_violations,
    )
    if failures:
        for message in failures:
            print(f"[FAIL] {message}")
        return 1

    print("[OK] Agentic core alignment checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Verify template '.github' alignment rules in a cross-platform way.

This script is a Python equivalent of 'scripts/check-github-alignment.sh' so
alignment checks run consistently on Windows and Unix environments.
"""

from __future__ import annotations

import json
from pathlib import Path

_REQUIRED_FILES: tuple[str, ...] = (
    "template/.github/CODEOWNERS.jinja",
    "template/.github/copilot-instructions.md.jinja",
    "template/.github/agents/ddd.agent.md",
    "template/.github/agents/debug.agent.md",
    "template/.github/agents/deep-thinking.agent.md",
    "template/.github/agents/frontend-engineer.agent.md",
    "template/.github/agents/modernization.agent.md",
    "template/.github/agents/prompt-engineering.agent.md",
    "template/.github/agents/sdd.agent.md",
    "template/.github/agents/tdd.agent.md",
    "template/.github/hooks/hooks.json",
    "template/.github/hooks/scripts/guard-tool.sh",
    "template/.github/hooks/scripts/guard-tool.ps1",
    "template/.github/hooks/scripts/check-licenses.sh",
    "template/.github/hooks/scripts/check-licenses.ps1",
    "template/.github/instructions/architecture.instructions.md.jinja",
    "template/.github/instructions/coding-conventions.instructions.md",
    "template/.github/instructions/commit.instructions.md",
    "template/.github/instructions/frontend.instructions.md",
    "template/.github/instructions/no-heredoc.instructions.md",
    "template/.github/instructions/prompt.instructions.md",
    "template/.github/instructions/shell.instructions.md",
    "template/.github/instructions/testing.instructions.md.jinja",
    "template/.github/instructions/update-docs-on-code-change.instructions.md",
    "template/.github/skills/clean-architecture/SKILL.md",
    "template/.github/skills/accessibility/SKILL.md",
    "template/.github/skills/frontend-react-stack/SKILL.md",
    "template/.github/skills/naming-registry/SKILL.md",
    "template/.github/skills/playwright/SKILL.md",
    "template/.github/skills/python-conventions/SKILL.md",
    "template/.github/skills/shadcn-ui/SKILL.md",
    "template/.github/skills/testing-conventions/SKILL.md",
)

_LEGACY_FILES: tuple[str, ...] = (
    "template/.github/agents/coordinator.agent.md",
    "template/.github/agents/security-auditor.agent.md",
    "template/.github/hooks/dependency-license-checker.json",
    "template/.github/hooks/tool-guardian.json",
    "template/.github/hooks/auto-format.json",
    "template/.github/hooks/scripts/auto-format.sh",
    "template/.github/hooks/scripts/auto-format.ps1",
    "template/.github/hooks/scripts/scan-secrets.sh",
    "template/.github/hooks/scripts/scan-secrets.ps1",
    "template/.github/skills/shadcn-frontend/SKILL.md",
    "template/.github/skills/README.md",
)

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

_AGENTIC_PATHS_TO_SCAN: tuple[str, ...] = (
    ".github/agents",
    ".github/instructions",
    ".github/prompts",
    ".github/skills",
    "template/.github/agents",
    "template/.github/instructions",
    "template/.github/prompts",
    "template/.github/skills",
)
_PROJECT_SPECIFIC_TOKENS: tuple[str, ...] = ("copier-fullstack-template",)


def _collect_missing(*, repo_root: Path) -> list[str]:
    """Collect required alignment files that are currently missing.

    Args:
        repo_root (Path): Repository root path.

    Returns:
        list[str]: Missing required file paths.
    """

    missing: list[str] = []
    for relative_path in _REQUIRED_FILES:
        if not (repo_root / relative_path).is_file():
            missing.append(relative_path)
    return missing


def _collect_legacy_present(*, repo_root: Path) -> list[str]:
    """Collect forbidden legacy files that are still present.

    Args:
        repo_root (Path): Repository root path.

    Returns:
        list[str]: Legacy file paths that should be removed.
    """

    present: list[str] = []
    for relative_path in _LEGACY_FILES:
        if (repo_root / relative_path).is_file():
            present.append(relative_path)
    return present


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
) -> list[str]:
    """Scan a single file for project-specific tokens.

    Args:
        candidate (Path): File to inspect.
        repo_root (Path): Repository root for relative formatting.
        suffixes (set[str]): File extensions to include.

    Returns:
        list[str]: Token findings for this candidate file.
    """

    if not candidate.is_file() or candidate.suffix not in suffixes:
        return []

    findings: list[str] = []
    content = candidate.read_text(encoding="utf-8")
    for token in _PROJECT_SPECIFIC_TOKENS:
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


def _collect_project_specific_agentic_refs(*, repo_root: Path) -> list[str]:
    """Detect project-specific repository tokens in agentic assets.

    Args:
        repo_root (Path): Repository root path.

    Returns:
        list[str]: File-level findings with token matches.
    """

    findings: list[str] = []
    suffixes = {".md", ".jinja", ".json", ".yaml", ".yml", ".toml"}

    for relative_directory in _AGENTIC_PATHS_TO_SCAN:
        directory = repo_root / relative_directory
        if not directory.exists():
            continue

        for candidate in directory.rglob("*"):
            findings.extend(
                _scan_candidate_for_project_tokens(
                    candidate=candidate,
                    repo_root=repo_root,
                    suffixes=suffixes,
                )
            )

    return findings


def _build_failure_messages(
    *,
    missing_files: list[str],
    legacy_files: list[str],
    hook_path_violations: list[str],
    project_specific_refs: list[str],
) -> list[str]:
    """Build normalized failure messages for all alignment checks.

    Args:
        missing_files (list[str]): Required files that are absent.
        legacy_files (list[str]): Deprecated files that still exist.
        hook_path_violations (list[str]): Hook-path validation findings.
        project_specific_refs (list[str]): Project-token findings in agentic assets.

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
    return failures


def main() -> int:
    """Execute '.github' alignment checks.

    Returns:
        int: Exit code (0 when alignment passes, 1 otherwise).
    """

    print("Checking .github core alignment (agents/hooks/instructions/skills)...")
    repo_root = Path(__file__).resolve().parents[1]

    missing_files = _collect_missing(repo_root=repo_root)
    legacy_files = _collect_legacy_present(repo_root=repo_root)
    hook_path_violations = _collect_hook_path_violations(repo_root=repo_root)
    project_specific_refs = _collect_project_specific_agentic_refs(repo_root=repo_root)

    failures = _build_failure_messages(
        missing_files=missing_files,
        legacy_files=legacy_files,
        hook_path_violations=hook_path_violations,
        project_specific_refs=project_specific_refs,
    )
    if failures:
        for message in failures:
            print(f"[FAIL] {message}")
        return 1

    print("[OK] .github core alignment checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

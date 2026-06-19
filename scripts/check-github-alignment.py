"""Verify template '.github' alignment rules in a cross-platform way.

This script is a Python equivalent of 'scripts/check-github-alignment.sh' so
alignment checks run consistently on Windows and Unix environments.
"""

from __future__ import annotations

from pathlib import Path

_REQUIRED_FILES: tuple[str, ...] = (
    "template/.github/CODEOWNERS.jinja",
    "template/.github/copilot-instructions.md.jinja",
    "template/.github/agents/debug.agent.md",
    "template/.github/agents/deep-thinking.agent.md",
    "template/.github/agents/expert-react-frontend-engineer.agent.md",
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
    "template/.github/skills/frontend-react-stack/SKILL.md",
    "template/.github/skills/naming-registry/SKILL.md",
    "template/.github/skills/python-conventions/SKILL.md",
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


def main() -> int:
    """Execute '.github' alignment checks.

    Returns:
        int: Exit code (0 when alignment passes, 1 otherwise).
    """

    print("Checking .github core alignment (agents/hooks/instructions/skills)...")
    repo_root = Path(__file__).resolve().parents[1]

    missing_files = _collect_missing(repo_root=repo_root)
    legacy_files = _collect_legacy_present(repo_root=repo_root)

    if missing_files:
        for relative_path in missing_files:
            print(f"[FAIL] Missing required alignment file: {relative_path}")

    if legacy_files:
        for relative_path in legacy_files:
            print(f"[FAIL] Legacy file found: {relative_path} (should be removed)")

    if missing_files or legacy_files:
        return 1

    print("[OK] .github core alignment checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

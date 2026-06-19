"""Audit structural/config alignment against a reference repository.

This script compares this template repository with a baseline app repository
(e.g. 'reference_automation') and reports production-readiness alignment gaps while
respecting template-repo semantics.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

_EPHEMERAL_NAMES = {
    ".git",
    ".venv",
    ".tox",
    ".pytest_cache",
    ".ruff_cache",
    ".pre-commit-cache",
    "__pycache__",
    ".hypothesis",
    ".coverage",
}
_SEMVERISH_TOP_LEVEL_NAME_RE = re.compile(r"^\d+\.\d+\.\d+$")

_REFERENCE_ROOT_DEFAULT = Path(
    "C:/Users/LFR/OneDrive - AP Pension/Documents/projects/reference_automation"
)
_REFERENCE_PROFILE_DEFAULT = "reference"
_CLAUDE_DIRNAME = ".claude"
_GITHUB_DIRNAME = ".github"

_EXPECTED_ROOT_ONLY_VS_REFERENCE = {
    ".coderabbit.yaml",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "SECURITY.md",
    "copier.yml",
    "template",
}

_EXPECTED_REFERENCE_ONLY_VS_ROOT = {
    ".coveragerc",
    ".devcontainer",
    ".env.dev",
    ".env.example",
    ".env.local",
    ".env.prod",
    ".gitnexus",
    ".gitnexusignore",
    ".python-version",
    "bandit.toml",
    "data",
    "frontend",
    "openspec",
    "pyproject.toml",
    "pytest.ini",
    "renovate.json",
    "ruff.toml",
    "sql",
    "src",
    "storage",
    "tests",
    "tox.ini",
    "uv.lock",
}

_PROFILE_EXPECTED_ROOT_ONLY_VS_REFERENCE: dict[str, set[str]] = {
    "reference": _EXPECTED_ROOT_ONLY_VS_REFERENCE,
    "frontend_frontend": {
        ".bg-shell",
        ".coderabbit.yaml",
        ".env",
        ".gsd",
        ".gsd-id",
        ".lycheecache",
        ".python-version",
        "CODE_OF_CONDUCT.md",
        "CONTRIBUTING.md",
        "LICENSE",
        "SECURITY.md",
        "copier.yml",
        "ruff.toml",
        "scripts",
        "template",
        "ty.toml",
    },
}

_PROFILE_EXPECTED_REFERENCE_ONLY_VS_ROOT: dict[str, set[str]] = {
    "reference": _EXPECTED_REFERENCE_ONLY_VS_ROOT,
    "frontend_frontend": {
        ".containerignore",
        ".devcontainer",
        ".dockerignore",
        ".env.example",
        ".storybook",
        "biome.json",
        "bun.lock",
        "bunfig.toml",
        "components.json",
        "coverage",
        "index.html",
        "node_modules",
        "package.json",
        "playwright-report",
        "playwright.config.ts",
        "public",
        "renovate.json",
        "src",
        "test-results",
        "tests",
        "tsconfig.json",
        "vite.config.ts",
        "vitest.config.ts",
    },
}

_ALLOWED_MISSING_ROOT_SKILLS_FROM_REFERENCE = {
    "gitnexus",
    "openspec",
}

_ROOT_REFERENCE_TARGETS = {
    ".agents",
    ".azuredevops",
    _CLAUDE_DIRNAME,
    _GITHUB_DIRNAME,
    ".editorconfig",
    ".gitattributes",
    ".gitignore",
    ".markdownlint-cli2.yaml",
    ".mcp.json",
    ".pre-commit-config.yaml",
    ".secrets.baseline",
    ".typos.toml",
    ".yamllint.yaml",
    "AGENTS.md",
    "CHANGELOG.md",
    "CLAUDE.md",
    "README.md",
    "Taskfile.yml",
    "azure",
    "caddy",
    "cspell.json",
    "docker",
}

_TEMPLATE_REFERENCE_TARGETS = {
    _CLAUDE_DIRNAME,
    _GITHUB_DIRNAME,
    ".editorconfig",
    ".gitattributes.jinja",
    ".gitignore.jinja",
    ".markdownlint-cli2.yaml",
    ".mcp.json.jinja",
    ".pre-commit-config.yaml.jinja",
    ".secrets.baseline",
    ".typos.toml.jinja",
    ".yamllint.yaml",
    "AGENTS.md.jinja",
    "CHANGELOG.md.jinja",
    "CLAUDE.md.jinja",
    "README.md.jinja",
    "Taskfile.yml.jinja",
    "cspell.json.jinja",
}


@dataclass(frozen=True, slots=True, kw_only=True)
class AuditResult:
    """Container for audit findings.

    Args:
        missing_in_root (list[str]): Missing required parity artifacts in repo root.
        missing_in_template (list[str]): Missing required parity artifacts in template root.
        missing_root_prompts_dir (bool): True when '.github/prompts' is missing in root.
        missing_template_prompts_dir (bool): True when '.github/prompts' is missing in template.
        missing_claude_cognitive_rule_root (bool): True when cognitive-load rule is missing in root.
        missing_claude_cognitive_rule_template (bool): True when cognitive-load rule is missing in template.
        root_only_vs_reference (list[str]): Root entries not present in reference repo.
        reference_only_vs_root (list[str]): Reference entries not present in root repo.
        unexpected_root_only_vs_reference (list[str]): Root-only top-level entries that are not expected.
        unexpected_reference_only_vs_root (list[str]): Reference-only top-level entries that are not expected.
        missing_root_github_agents (list[str]): Missing '.github/agents' files present in reference.
        missing_root_github_hooks_files (list[str]): Missing '.github/hooks' files (excluding scripts dir).
        missing_root_github_hook_scripts (list[str]): Missing '.github/hooks/scripts' files.
        missing_root_github_instructions (list[str]): Missing '.github/instructions' files.
        missing_root_claude_rules (list[str]): Missing '.claude/rules' files.
        missing_root_github_skills (list[str]): Missing '.github/skills' directories after allowed exemptions.
    """

    missing_in_root: list[str]
    missing_in_template: list[str]
    missing_root_prompts_dir: bool
    missing_template_prompts_dir: bool
    missing_claude_cognitive_rule_root: bool
    missing_claude_cognitive_rule_template: bool
    root_only_vs_reference: list[str]
    reference_only_vs_root: list[str]
    unexpected_root_only_vs_reference: list[str]
    unexpected_reference_only_vs_root: list[str]
    missing_root_github_agents: list[str]
    missing_root_github_hooks_files: list[str]
    missing_root_github_hook_scripts: list[str]
    missing_root_github_instructions: list[str]
    missing_root_claude_rules: list[str]
    missing_root_github_skills: list[str]

    @property
    def has_failures(self) -> bool:
        """Whether any mandatory alignment checks failed.

        Returns:
            bool: True when mandatory checks report any missing required item.
        """

        return any(
            [
                bool(self.missing_in_root),
                bool(self.missing_in_template),
                self.missing_root_prompts_dir,
                self.missing_template_prompts_dir,
                self.missing_claude_cognitive_rule_root,
                self.missing_claude_cognitive_rule_template,
                bool(self.unexpected_root_only_vs_reference),
                bool(self.unexpected_reference_only_vs_root),
                bool(self.missing_root_github_agents),
                bool(self.missing_root_github_hooks_files),
                bool(self.missing_root_github_hook_scripts),
                bool(self.missing_root_github_instructions),
                bool(self.missing_root_claude_rules),
                bool(self.missing_root_github_skills),
            ]
        )


def _list_top_level_names(*, root: Path) -> set[str]:
    """Return normalized top-level entry names for a path.

    Args:
        root (Path): Directory to inspect.

    Returns:
        set[str]: Names excluding ephemeral runtime/cache artifacts.
    """

    names = set()
    for entry in root.iterdir():
        name = entry.name
        if name in _EPHEMERAL_NAMES:
            continue
        if _SEMVERISH_TOP_LEVEL_NAME_RE.fullmatch(name):
            continue
        names.add(name)
    return names


def _assert_exists(*, path: Path, label: str) -> None:
    """Exit early when required path is missing.

    Args:
        path (Path): Path to validate.
        label (str): Human-readable path label.

    Raises:
        SystemExit: If the required path does not exist.
    """

    if not path.exists():
        raise SystemExit(f"[ERROR] Required path not found for {label}: {path}")


def _list_dir_child_names(*, path: Path) -> set[str]:
    """List direct child names for an existing directory.

    Args:
        path (Path): Directory whose immediate children should be listed.

    Returns:
        set[str]: Child file/directory names.
    """

    if not path.exists():
        return set()
    return {entry.name for entry in path.iterdir()}


def _build_result(*, repo_root: Path, reference_root: Path, reference_profile: str) -> AuditResult:
    """Build the full alignment report.

    Args:
        repo_root (Path): Current template repository root.
        reference_root (Path): Reference repository root.

    Returns:
        AuditResult: Computed structural/configuration findings.
    """

    root_names = _list_top_level_names(root=repo_root)
    reference_names = _list_top_level_names(root=reference_root)

    missing_in_root = sorted(
        name for name in _ROOT_REFERENCE_TARGETS if name not in root_names
    )

    template_root = repo_root / "template"
    template_names = _list_top_level_names(root=template_root)
    missing_in_template = sorted(
        name for name in _TEMPLATE_REFERENCE_TARGETS if name not in template_names
    )

    missing_root_prompts_dir = not (repo_root / _GITHUB_DIRNAME / "prompts").exists()
    missing_template_prompts_dir = not (
        template_root / _GITHUB_DIRNAME / "prompts"
    ).exists()

    missing_claude_cognitive_rule_root = not (
        repo_root / _CLAUDE_DIRNAME / "rules" / "cognitive-load.md"
    ).exists()
    missing_claude_cognitive_rule_template = not (
        template_root / _CLAUDE_DIRNAME / "rules" / "cognitive-load.md"
    ).exists()

    root_only_vs_reference = sorted(root_names - reference_names)
    reference_only_vs_root = sorted(reference_names - root_names)

    expected_root_only = _PROFILE_EXPECTED_ROOT_ONLY_VS_REFERENCE.get(
        reference_profile,
        _EXPECTED_ROOT_ONLY_VS_REFERENCE,
    )
    expected_reference_only = _PROFILE_EXPECTED_REFERENCE_ONLY_VS_ROOT.get(
        reference_profile,
        _EXPECTED_REFERENCE_ONLY_VS_ROOT,
    )

    unexpected_root_only_vs_reference = sorted(
        set(root_only_vs_reference) - expected_root_only
    )
    unexpected_reference_only_vs_root = sorted(
        set(reference_only_vs_root) - expected_reference_only
    )

    root_github = repo_root / _GITHUB_DIRNAME
    ref_github = reference_root / _GITHUB_DIRNAME
    root_claude = repo_root / _CLAUDE_DIRNAME
    ref_claude = reference_root / _CLAUDE_DIRNAME

    root_agent_names = _list_dir_child_names(path=root_github / "agents")
    ref_agent_names = _list_dir_child_names(path=ref_github / "agents")
    missing_root_github_agents = sorted(ref_agent_names - root_agent_names)

    root_hook_names = _list_dir_child_names(path=root_github / "hooks") - {"scripts"}
    ref_hook_names = _list_dir_child_names(path=ref_github / "hooks") - {"scripts"}
    missing_root_github_hooks_files = sorted(ref_hook_names - root_hook_names)

    root_hook_script_names = _list_dir_child_names(
        path=root_github / "hooks" / "scripts"
    )
    ref_hook_script_names = _list_dir_child_names(path=ref_github / "hooks" / "scripts")
    missing_root_github_hook_scripts = sorted(
        ref_hook_script_names - root_hook_script_names
    )

    root_instruction_names = _list_dir_child_names(path=root_github / "instructions")
    ref_instruction_names = _list_dir_child_names(path=ref_github / "instructions")
    missing_root_github_instructions = sorted(
        ref_instruction_names - root_instruction_names
    )

    root_rule_names = _list_dir_child_names(path=root_claude / "rules")
    ref_rule_names = _list_dir_child_names(path=ref_claude / "rules")
    missing_root_claude_rules = sorted(ref_rule_names - root_rule_names)

    root_skill_names = _list_dir_child_names(path=root_github / "skills")
    ref_skill_names = _list_dir_child_names(path=ref_github / "skills")
    missing_root_github_skills = sorted(
        (ref_skill_names - root_skill_names)
        - _ALLOWED_MISSING_ROOT_SKILLS_FROM_REFERENCE
    )

    return AuditResult(
        missing_in_root=missing_in_root,
        missing_in_template=missing_in_template,
        missing_root_prompts_dir=missing_root_prompts_dir,
        missing_template_prompts_dir=missing_template_prompts_dir,
        missing_claude_cognitive_rule_root=missing_claude_cognitive_rule_root,
        missing_claude_cognitive_rule_template=missing_claude_cognitive_rule_template,
        root_only_vs_reference=root_only_vs_reference,
        reference_only_vs_root=reference_only_vs_root,
        unexpected_root_only_vs_reference=unexpected_root_only_vs_reference,
        unexpected_reference_only_vs_root=unexpected_reference_only_vs_root,
        missing_root_github_agents=missing_root_github_agents,
        missing_root_github_hooks_files=missing_root_github_hooks_files,
        missing_root_github_hook_scripts=missing_root_github_hook_scripts,
        missing_root_github_instructions=missing_root_github_instructions,
        missing_root_claude_rules=missing_root_claude_rules,
        missing_root_github_skills=missing_root_github_skills,
    )


def _to_json(*, result: AuditResult, repo_root: Path, reference_root: Path) -> str:
    """Serialize findings to JSON.

    Args:
        result (AuditResult): Findings to serialize.
        repo_root (Path): Current repo path.
        reference_root (Path): Reference repo path.

    Returns:
        str: Pretty-formatted JSON report.
    """

    payload: dict[str, object] = {
        "repo_root": str(repo_root),
        "reference_root": str(reference_root),
        "mandatory_checks": {
            "missing_in_root": result.missing_in_root,
            "missing_in_template": result.missing_in_template,
            "missing_root_prompts_dir": result.missing_root_prompts_dir,
            "missing_template_prompts_dir": result.missing_template_prompts_dir,
            "missing_claude_cognitive_rule_root": result.missing_claude_cognitive_rule_root,
            "missing_claude_cognitive_rule_template": result.missing_claude_cognitive_rule_template,
            "missing_root_github_agents": result.missing_root_github_agents,
            "missing_root_github_hooks_files": result.missing_root_github_hooks_files,
            "missing_root_github_hook_scripts": result.missing_root_github_hook_scripts,
            "missing_root_github_instructions": result.missing_root_github_instructions,
            "missing_root_claude_rules": result.missing_root_claude_rules,
            "missing_root_github_skills": result.missing_root_github_skills,
        },
        "informational_deltas": {
            "root_only_vs_reference": result.root_only_vs_reference,
            "reference_only_vs_root": result.reference_only_vs_root,
            "unexpected_root_only_vs_reference": result.unexpected_root_only_vs_reference,
            "unexpected_reference_only_vs_root": result.unexpected_reference_only_vs_root,
        },
        "status": "fail" if result.has_failures else "pass",
    }
    return json.dumps(payload, indent=2)


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command options.
    """

    parser = argparse.ArgumentParser(
        description="Audit copier template repository alignment against a reference app repo."
    )
    parser.add_argument(
        "--reference-root",
        type=Path,
        default=_REFERENCE_ROOT_DEFAULT,
        help="Absolute path to reference repository root.",
    )
    parser.add_argument(
        "--write-json",
        type=Path,
        default=None,
        help="Optional path for writing JSON report output.",
    )
    parser.add_argument(
        "--reference-profile",
        type=str,
        default=_REFERENCE_PROFILE_DEFAULT,
        choices=("reference", "frontend_frontend"),
        help="Reference profile used for top-level delta expectations.",
    )
    return parser.parse_args()


def main() -> int:
    """Run alignment audit and emit report.

    Returns:
        int: Exit code (0 pass, 1 fail).
    """

    args = _parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    reference_root: Path = args.reference_root.resolve()

    _assert_exists(path=repo_root, label="current repository")
    _assert_exists(path=repo_root / "template", label="template directory")
    _assert_exists(path=reference_root, label="reference repository")

    result = _build_result(
        repo_root=repo_root,
        reference_root=reference_root,
        reference_profile=args.reference_profile,
    )
    output = _to_json(result=result, repo_root=repo_root, reference_root=reference_root)

    if args.write_json is not None:
        args.write_json.parent.mkdir(parents=True, exist_ok=True)
        args.write_json.write_text(output + "\n", encoding="utf-8")

    print(output)
    return 1 if result.has_failures else 0


if __name__ == "__main__":
    sys.exit(main())

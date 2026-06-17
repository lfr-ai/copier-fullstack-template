"""Audit structural/config alignment against a reference repository.

This script compares this template repository with a baseline app repository
(e.g. 'reference_automation') and reports production-readiness alignment gaps while
respecting template-repo semantics.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path

_EPHEMERAL_NAMES = {
    '.git',
    '.venv',
    '.tox',
    '.pytest_cache',
    '.ruff_cache',
    '.pre-commit-cache',
    '__pycache__',
    '.hypothesis',
    '.coverage',
}

_REFERENCE_ROOT_DEFAULT = Path(
    'C:/Users/LFR/OneDrive - AP Pension/Documents/projects/reference_automation'
)

_ROOT_REFERENCE_TARGETS = {
    '.claude',
    '.github',
    '.editorconfig',
    '.gitattributes',
    '.gitignore',
    '.markdownlint-cli2.yaml',
    '.mcp.json',
    '.pre-commit-config.yaml',
    '.secrets.baseline',
    '.typos.toml',
    '.yamllint.yaml',
    'AGENTS.md',
    'CHANGELOG.md',
    'CLAUDE.md',
    'README.md',
    'Taskfile.yml',
    'cspell.json',
}

_TEMPLATE_REFERENCE_TARGETS = {
    '.claude',
    '.github',
    '.editorconfig',
    '.gitattributes.jinja',
    '.gitignore.jinja',
    '.markdownlint-cli2.yaml',
    '.mcp.json.jinja',
    '.pre-commit-config.yaml.jinja',
    '.secrets.baseline',
    '.typos.toml.jinja',
    '.yamllint.yaml',
    'AGENTS.md.jinja',
    'CHANGELOG.md.jinja',
    'CLAUDE.md.jinja',
    'README.md.jinja',
    'Taskfile.yml.jinja',
    'cspell.json.jinja',
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
    """

    missing_in_root: list[str]
    missing_in_template: list[str]
    missing_root_prompts_dir: bool
    missing_template_prompts_dir: bool
    missing_claude_cognitive_rule_root: bool
    missing_claude_cognitive_rule_template: bool
    root_only_vs_reference: list[str]
    reference_only_vs_root: list[str]

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


def _build_result(*, repo_root: Path, reference_root: Path) -> AuditResult:
    """Build the full alignment report.

    Args:
        repo_root (Path): Current template repository root.
        reference_root (Path): Reference repository root.

    Returns:
        AuditResult: Computed structural/configuration findings.
    """

    root_names = _list_top_level_names(root=repo_root)
    reference_names = _list_top_level_names(root=reference_root)

    missing_in_root = sorted(name for name in _ROOT_REFERENCE_TARGETS if name not in root_names)

    template_root = repo_root / 'template'
    template_names = _list_top_level_names(root=template_root)
    missing_in_template = sorted(
        name for name in _TEMPLATE_REFERENCE_TARGETS if name not in template_names
    )

    missing_root_prompts_dir = not (repo_root / '.github' / 'prompts').exists()
    missing_template_prompts_dir = not (template_root / '.github' / 'prompts').exists()

    missing_claude_cognitive_rule_root = not (
        repo_root / '.claude' / 'rules' / 'cognitive-load.md'
    ).exists()
    missing_claude_cognitive_rule_template = not (
        template_root / '.claude' / 'rules' / 'cognitive-load.md'
    ).exists()

    root_only_vs_reference = sorted(root_names - reference_names)
    reference_only_vs_root = sorted(reference_names - root_names)

    return AuditResult(
        missing_in_root=missing_in_root,
        missing_in_template=missing_in_template,
        missing_root_prompts_dir=missing_root_prompts_dir,
        missing_template_prompts_dir=missing_template_prompts_dir,
        missing_claude_cognitive_rule_root=missing_claude_cognitive_rule_root,
        missing_claude_cognitive_rule_template=missing_claude_cognitive_rule_template,
        root_only_vs_reference=root_only_vs_reference,
        reference_only_vs_root=reference_only_vs_root,
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
        'repo_root': str(repo_root),
        'reference_root': str(reference_root),
        'mandatory_checks': {
            'missing_in_root': result.missing_in_root,
            'missing_in_template': result.missing_in_template,
            'missing_root_prompts_dir': result.missing_root_prompts_dir,
            'missing_template_prompts_dir': result.missing_template_prompts_dir,
            'missing_claude_cognitive_rule_root': result.missing_claude_cognitive_rule_root,
            'missing_claude_cognitive_rule_template': result.missing_claude_cognitive_rule_template,
        },
        'informational_deltas': {
            'root_only_vs_reference': result.root_only_vs_reference,
            'reference_only_vs_root': result.reference_only_vs_root,
        },
        'status': 'fail' if result.has_failures else 'pass',
    }
    return json.dumps(payload, indent=2)


def _parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command options.
    """

    parser = argparse.ArgumentParser(
        description='Audit copier template repository alignment against a reference app repo.'
    )
    parser.add_argument(
        '--reference-root',
        type=Path,
        default=_REFERENCE_ROOT_DEFAULT,
        help='Absolute path to reference repository root.',
    )
    parser.add_argument(
        '--write-json',
        type=Path,
        default=None,
        help='Optional path for writing JSON report output.',
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

    _assert_exists(path=repo_root, label='current repository')
    _assert_exists(path=repo_root / 'template', label='template directory')
    _assert_exists(path=reference_root, label='reference repository')

    result = _build_result(repo_root=repo_root, reference_root=reference_root)
    output = _to_json(result=result, repo_root=repo_root, reference_root=reference_root)

    if args.write_json is not None:
        args.write_json.parent.mkdir(parents=True, exist_ok=True)
        args.write_json.write_text(output + '\n', encoding='utf-8')

    print(output)
    return 1 if result.has_failures else 0


if __name__ == '__main__':
    sys.exit(main())

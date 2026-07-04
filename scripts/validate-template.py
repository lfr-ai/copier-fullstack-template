#!/usr/bin/env python3
"""Validate template renders successfully with both VCS platform choices."""

from __future__ import annotations

import subprocess  # nosec B404
import sys
import tempfile
from pathlib import Path

_COPIER_RENDER_BASE_ARGS = (
    "uvx",
    "copier",
    "copy",
    "--trust",
    "--defaults",
    "-d",
    "project_name=Test",
    "-d",
    "author_name=Test",
    "-d",
    "author_email=test@test.com",
)
_OPENSPEC_REQUIRED_RELATIVE_PATHS = (
    Path("openspec/config.yaml"),
    Path("openspec/specs/architecture/spec.md"),
    Path("openspec/schemas/clean-arch-spec-driven/schema.yaml"),
    Path("tasks/openspec.yml"),
    Path("docs/OPENSPEC.md"),
    Path(".github/skills/openspec-workflow/SKILL.md"),
    Path(".claude/skills/openspec-workflow/SKILL.md"),
    Path(".github/prompts/opsx-propose.prompt.md"),
)


def configure_git_author() -> None:
    """Configure git author for Copier post-copy git commits."""
    subprocess.run(  # nosec B603 B607
        ["git", "config", "--global", "user.name", "Test"],
        check=True,
        capture_output=True,
    )
    subprocess.run(  # nosec B603 B607
        ["git", "config", "--global", "user.email", "test@test.com"],
        check=True,
        capture_output=True,
    )


def _build_render_command(*, vcs_choice: str, output_dir: str) -> list[str]:
    """Build a Copier render command for a VCS platform choice.

    Args:
        vcs_choice (str): VCS platform, such as 'github' or 'azuredevops'.
        output_dir (str): Target path for rendered output.

    Returns:
        list[str]: Command arguments for 'subprocess.run'.
    """
    return [
        *_COPIER_RENDER_BASE_ARGS,
        "-d",
        f"vcs_platform={vcs_choice}",
        ".",
        output_dir,
    ]


def _collect_missing_openspec_files(*, output_path: Path) -> list[str]:
    """Collect required OpenSpec files missing from rendered output.

    Args:
        output_path (Path): Rendered project root path.

    Returns:
        list[str]: Missing required-file paths as strings.
    """
    return [
        str(output_path / relative_path)
        for relative_path in _OPENSPEC_REQUIRED_RELATIVE_PATHS
        if not (output_path / relative_path).exists()
    ]


def render_template(*, vcs_choice: str, output_dir: str) -> bool:
    """Render template with given VCS platform choice.

    Args:
        vcs_choice (str): One of 'github' or 'azuredevops'.
        output_dir (str): Target directory for rendered output.

    Returns:
        bool: True if render succeeded, otherwise False.
    """
    result = subprocess.run(  # nosec B603 B607
        _build_render_command(vcs_choice=vcs_choice, output_dir=output_dir),
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"[FAIL] Template render failed with vcs_platform={vcs_choice}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        return False

    missing = _collect_missing_openspec_files(output_path=Path(output_dir))
    if missing:
        print(f"[FAIL] Missing rendered OpenSpec files for vcs_platform={vcs_choice}")
        for path in missing:
            print(f"  - {path}")
        return False

    print(f"[OK] Template rendered successfully with vcs_platform={vcs_choice}")
    return True


def main() -> int:
    """Run validation checks."""
    print("Configuring git author...")
    configure_git_author()

    print("\nValidating template renders...")

    with tempfile.TemporaryDirectory(prefix="validate-template-") as temp_dir:
        temp_path = Path(temp_dir)

        # Test GitHub VCS choice
        github_success = render_template(
            vcs_choice="github",
            output_dir=str(temp_path / "github"),
        )

        # Test Azure DevOps VCS choice
        azuredevops_success = render_template(
            vcs_choice="azuredevops",
            output_dir=str(temp_path / "azuredevops"),
        )

    # Report final status
    if github_success and azuredevops_success:
        print("\n[OK] All VCS platform choices validated successfully")
        return 0
    else:
        print("\n[FAIL] Template validation failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())

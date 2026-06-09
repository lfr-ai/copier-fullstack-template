#!/usr/bin/env python3
"""Validate template renders successfully with both VCS platform choices."""

from __future__ import annotations

from pathlib import Path
import subprocess  # nosec B404
import sys
import tempfile


def configure_git_author() -> None:
    """Configure git author for copier post-copy git commits."""
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


def render_template(vcs_choice: str, output_dir: str) -> bool:
    """Render template with given VCS platform choice.

    Args:
        vcs_choice: One of 'github' or 'azuredevops'
        output_dir: Target directory for rendered output

    Returns:
        True if render succeeded, False otherwise
    """
    result = subprocess.run(  # nosec B603 B607
        [
            "uvx",
            "copier",
            "copy",
            "--trust",
            "--defaults",
            "-d",
            f"vcs_platform={vcs_choice}",
            "-d",
            "project_name=Test",
            "-d",
            "author_name=Test",
            "-d",
            "author_email=test@test.com",
            ".",
            output_dir,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"[FAIL] Template render failed with vcs_platform={vcs_choice}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        return False

    output_path = Path(output_dir)
    openspec_required_files = [
        output_path / "openspec" / "config.yaml",
        output_path / "openspec" / "specs" / "architecture" / "spec.md",
        output_path
        / "openspec"
        / "schemas"
        / "clean-arch-spec-driven"
        / "schema.yaml",
        output_path / "tasks" / "openspec.yml",
        output_path / "docs" / "OPENSPEC.md",
        output_path / ".github" / "skills" / "openspec-workflow" / "SKILL.md",
        output_path / ".claude" / "skills" / "openspec-workflow" / "SKILL.md",
        output_path / ".github" / "prompts" / "opsx-propose.prompt.md",
    ]

    missing = [str(path) for path in openspec_required_files if not path.exists()]
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
        github_success = render_template("github", str(temp_path / "github"))

        # Test Azure DevOps VCS choice
        azuredevops_success = render_template(
            "azuredevops", str(temp_path / "azuredevops")
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

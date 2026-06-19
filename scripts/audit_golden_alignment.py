"""Run multi-reference golden alignment checks.

This wrapper executes 'audit_koda_alignment.py' against both golden references
('koda_automation' and 'kris_frontend') to ensure parity checks stay green
across backend-heavy and frontend-heavy baselines.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

_DEFAULT_KODA_ROOT = Path(
    "C:/Users/LFR/OneDrive - AP Pension/Documents/projects/koda_automation"
)
_DEFAULT_KRIS_ROOT = Path(
    "C:/Users/LFR/OneDrive - AP Pension/Documents/projects/kris_frontend"
)


@dataclass(frozen=True, slots=True, kw_only=True)
class AuditExecutionResult:
    """Container for a single audit command execution result.

    Args:
        label (str): Human-friendly reference label.
        command (list[str]): Executed command.
        exit_code (int): Process exit code.
    """

    label: str
    command: list[str]
    exit_code: int


def _parse_args() -> argparse.Namespace:
    """Parse CLI arguments.

    Returns:
        argparse.Namespace: Parsed options.
    """

    parser = argparse.ArgumentParser(
        description="Run alignment audits against multiple golden references."
    )
    parser.add_argument(
        "--koda-root",
        type=Path,
        default=_DEFAULT_KODA_ROOT,
        help="Absolute path to the koda_automation repository root.",
    )
    parser.add_argument(
        "--kris-root",
        type=Path,
        default=_DEFAULT_KRIS_ROOT,
        help="Absolute path to the kris_frontend repository root.",
    )
    return parser.parse_args()


def _assert_exists(*, path: Path, label: str) -> None:
    """Validate required paths before running audits.

    Args:
        path (Path): Path to validate.
        label (str): Human-readable label for diagnostics.

    Raises:
        SystemExit: If the path does not exist.
    """

    if not path.exists():
        raise SystemExit(f"[ERROR] Missing {label}: {path}")


def _run_single_audit(
    *,
    script_path: Path,
    reference_root: Path,
    label: str,
    reference_profile: str,
) -> AuditExecutionResult:
    """Run one alignment audit process.

    Args:
        script_path (Path): Path to 'audit_koda_alignment.py'.
        reference_root (Path): Reference repository root path.
        label (str): Human-friendly label.

    Returns:
        AuditExecutionResult: Execution metadata and exit code.
    """

    command = [
        sys.executable,
        str(script_path),
        "--reference-root",
        str(reference_root),
        "--reference-profile",
        reference_profile,
    ]
    completed = subprocess.run(command, check=False)
    return AuditExecutionResult(label=label, command=command, exit_code=completed.returncode)


def main() -> int:
    """Execute both golden audits and return consolidated status.

    Returns:
        int: 0 when all audits pass, otherwise 1.
    """

    args = _parse_args()
    scripts_root = Path(__file__).resolve().parent
    audit_script = scripts_root / "audit_koda_alignment.py"

    _assert_exists(path=audit_script, label="audit script")
    _assert_exists(path=args.koda_root, label="koda reference root")
    _assert_exists(path=args.kris_root, label="kris reference root")

    results = [
        _run_single_audit(
            script_path=audit_script,
            reference_root=args.koda_root.resolve(),
            label="koda_automation",
            reference_profile="koda",
        ),
        _run_single_audit(
            script_path=audit_script,
            reference_root=args.kris_root.resolve(),
            label="kris_frontend",
            reference_profile="kris_frontend",
        ),
    ]

    failed = [result for result in results if result.exit_code != 0]
    if failed:
        print("[FAIL] Golden alignment audits failed:")
        for result in failed:
            print(f"  - {result.label}: exit {result.exit_code}")
        return 1

    print("[OK] Golden alignment audits passed (koda_automation + kris_frontend).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

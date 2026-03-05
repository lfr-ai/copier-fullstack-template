"""Generate Alembic migration convenience wrapper."""

from __future__ import annotations

import subprocess
import sys


def main() -> None:
    """Generate Alembic migration with provided message."""
    if len(sys.argv) < 2:
        print("Usage: python tools/generate_migration.py <message>")
        sys.exit(1)

    message = " ".join(sys.argv[1:])
    subprocess.run(
        ["alembic", "revision", "--autogenerate", "-m", message],
        check=True,
    )


if __name__ == "__main__":
    main()

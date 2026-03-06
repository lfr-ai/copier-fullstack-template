"""Generate Alembic migration convenience wrapper."""

from __future__ import annotations

import sys

from alembic.config import main as alembic_main

_MIN_ARGC = 2


def main() -> None:
    """Generate Alembic migration with provided message."""
    if len(sys.argv) < _MIN_ARGC:
        sys.stderr.write("Usage: python tools/generate_migration.py <message>\n")
        sys.exit(1)

    message = " ".join(sys.argv[1:])
    alembic_main(argv=["revision", "--autogenerate", "-m", message])


if __name__ == "__main__":
    main()

"""Date and time utility functions."""

from __future__ import annotations

from datetime import UTC, datetime


def utc_now() -> datetime:
    """Get current UTC datetime.

    Returns:
        Timezone-aware UTC datetime.
    """
    return datetime.now(UTC)


def format_iso(dt: datetime) -> str:
    """Format datetime as ISO 8601 string.

    Args:
        dt: Datetime to format.

    Returns:
        ISO 8601 formatted string.
    """
    return dt.isoformat()


def parse_iso(value: str) -> datetime:
    """Parse ISO 8601 string to datetime.

    Args:
        value: ISO 8601 datetime string.

    Returns:
        Parsed datetime instance.
    """
    return datetime.fromisoformat(value)

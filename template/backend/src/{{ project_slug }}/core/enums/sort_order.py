"""Sort direction enumeration."""

from __future__ import annotations

from enum import auto, unique

from {{ project_slug }}.core.enums.base import ParseableEnum

__all__ = ["SortOrder"]


@unique
class SortOrder(ParseableEnum):
    """Sort direction for query results."""

    ASC = auto()
    DESC = auto()

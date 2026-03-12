"""Status enumerations for domain entities."""

from __future__ import annotations

from enum import auto, unique

from {{ project_slug }}.core.enums.base import ParseableEnum

__all__ = ["Status"]


@unique
class Status(ParseableEnum):
    """Entity lifecycle status."""

    ACTIVE = auto()
    INACTIVE = auto()
    SUSPENDED = auto()
    DELETED = auto()

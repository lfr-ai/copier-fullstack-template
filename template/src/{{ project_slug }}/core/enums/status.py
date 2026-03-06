"""Status enumerations for domain entities."""

from __future__ import annotations

from enum import StrEnum, auto, unique


@unique
class Status(StrEnum):
    """Entity lifecycle status."""

    ACTIVE = auto()
    INACTIVE = auto()
    SUSPENDED = auto()
    DELETED = auto()

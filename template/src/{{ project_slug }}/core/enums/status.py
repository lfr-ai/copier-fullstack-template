"""Status enumerations for domain entities."""

from enum import StrEnum, auto, unique


@unique
class Status(StrEnum):
    """Entity lifecycle status."""

    ACTIVE = auto()
    INACTIVE = auto()
    SUSPENDED = auto()
    DELETED = auto()

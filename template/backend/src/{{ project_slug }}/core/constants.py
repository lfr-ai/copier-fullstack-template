"""Domain validation constants.

Shared by core, application, and adapter layers. Constants that are
infrastructure-specific (DB pool sizes, networking defaults, etc.)
live in ``config.constants`` instead.
"""

from __future__ import annotations

from typing import Final

__all__ = [
    "DEFAULT_LIST_LIMIT",
    "DISPLAY_NAME_MAX_LENGTH",
    "DISPLAY_NAME_MIN_LENGTH",
    "EMAIL_MAX_LENGTH",
    "EMAIL_MIN_LENGTH",
    "MIN_PASSWORD_LENGTH",
    "PASSWORD_HASH_MAX_LENGTH",
    "PASSWORD_MAX_LENGTH",
]

DEFAULT_LIST_LIMIT: Final[int] = 100

EMAIL_MIN_LENGTH: Final[int] = 5
EMAIL_MAX_LENGTH: Final[int] = 255
DISPLAY_NAME_MIN_LENGTH: Final[int] = 1
DISPLAY_NAME_MAX_LENGTH: Final[int] = 100

MIN_PASSWORD_LENGTH: Final[int] = 8
PASSWORD_MAX_LENGTH: Final[int] = 128
PASSWORD_HASH_MAX_LENGTH: Final[int] = 255

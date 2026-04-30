"""Domain validation constants.

Shared by core, application, and adapter layers. Constants that are
infrastructure-specific (DB pool sizes, networking defaults, etc.)
live in 'config.constants' instead.
"""

from __future__ import annotations

DEFAULT_LIST_LIMIT = 100

EMAIL_MIN_LENGTH = 5
EMAIL_MAX_LENGTH = 255
DISPLAY_NAME_MIN_LENGTH = 1
DISPLAY_NAME_MAX_LENGTH = 100

MIN_PASSWORD_LENGTH = 8
PASSWORD_MAX_LENGTH = 128
PASSWORD_HASH_MAX_LENGTH = 255

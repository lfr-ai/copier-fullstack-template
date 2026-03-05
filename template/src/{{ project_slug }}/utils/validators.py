"""Common validation utility functions."""

from __future__ import annotations

import re

EMAIL_PATTERN = re.compile(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)
MIN_PASSWORD_LENGTH = 8


def is_valid_email(email: str) -> bool:
    """Validate email address format.

    Args:
        email: Email address to validate.

    Returns:
        True if email format is valid.
    """
    return bool(EMAIL_PATTERN.match(email))


def is_strong_password(password: str) -> bool:
    """Validate password strength.

    Requires minimum length, uppercase, lowercase, and digit.

    Args:
        password: Password to validate.

    Returns:
        True if password meets strength requirements.
    """
    if len(password) < MIN_PASSWORD_LENGTH:
        return False
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    return has_upper and has_lower and has_digit

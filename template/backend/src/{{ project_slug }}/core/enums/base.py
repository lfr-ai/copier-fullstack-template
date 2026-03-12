"""Base enum with reusable parsing support."""

from __future__ import annotations

from enum import StrEnum
from typing import Self

__all__ = ["ParseableEnum"]


class ParseableEnum(StrEnum):
    """``StrEnum`` subclass with a reusable ``from_str`` parser.

    Subclasses inherit a ``from_str`` class method that performs
    case-insensitive parsing and raises ``ValueError`` with a clear
    message on mismatch.
    """

    @classmethod
    def from_str(cls, value: str) -> Self:
        """Parse a case-insensitive string into a member.

        Args:
            value (str): String representation of the member.

        Returns:
            Self: The matching enum member.

        Raises:
            ValueError: If *value* does not match any member.
        """
        try:
            return cls(value.lower())
        except ValueError:
            msg = f"Unknown {cls.__name__}: '{value}'"
            raise ValueError(msg) from None

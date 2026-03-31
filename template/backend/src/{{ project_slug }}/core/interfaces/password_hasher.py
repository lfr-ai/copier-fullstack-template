"""Password hashing protocol for domain-layer abstraction."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class PasswordHasher(Protocol):
    """Protocol defining password hashing operations.

    Allows the application layer to hash and verify passwords
    without depending on a concrete infrastructure implementation.
    """

    def hash(self, password: str) -> str:
        """Hash a plain-text password.

        Args:
            password (str): Plain-text password to hash.

        Returns:
            str: Encoded hash string.
        """
        ...

    def verify(self, *, password: str, hashed: str) -> bool:
        """Verify a password against a stored hash.

        Args:
            password (str): Plain-text password to verify.
            hashed (str): Previously hashed password string.

        Returns:
            bool: 'True' if the password matches.
        """
        ...

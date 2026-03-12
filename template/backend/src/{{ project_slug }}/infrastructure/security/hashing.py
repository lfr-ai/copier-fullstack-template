"""Cryptographic hashing utilities."""

from __future__ import annotations

__all__ = ["hash_password", "verify_password"]

import hashlib
import secrets
from typing import Final

_SALT_LENGTH: Final[int] = 32
_PBKDF2_ITERATIONS: Final[int] = 600_000


def hash_password(password: str, *, salt: bytes | None = None) -> str:
    """Hash a password using PBKDF2-SHA256 with a random salt.

    Args:
        password (str): The plaintext password to hash.
        salt (bytes | None): Optional salt bytes. Generated randomly if not provided.

    Returns:
        str: A string in the format ``salt_hex$hash_hex``.
    """
    if salt is None:
        salt = secrets.token_bytes(_SALT_LENGTH)

    dk = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        iterations=_PBKDF2_ITERATIONS,
    )
    return f"{salt.hex()}${dk.hex()}"


def verify_password(*, password: str, hashed: str) -> bool:
    """Verify a password against a PBKDF2-SHA256 hash.

    Args:
        password (str): The plaintext password to verify.
        hashed (str): The hash string in ``salt_hex$hash_hex`` format.

    Returns:
        bool: True if the password matches the hash.
    """
    try:
        salt_hex, hash_hex = hashed.split("$", maxsplit=1)
    except ValueError:
        return False

    salt = bytes.fromhex(salt_hex)
    expected = hash_password(password, salt=salt)
    return secrets.compare_digest(expected, hashed)

"""Backward-compatible re-export — canonical location: ``adapters.security.hashing``.

.. deprecated::
    Import from :mod:`{{ project_slug }}.adapters.security.hashing` instead.
    This module will be removed in a future release.
"""

from __future__ import annotations

import hashlib
import secrets
import warnings

warnings.warn(
    "infrastructure.security.hashing is deprecated. "
    "Use adapters.security.hashing instead.",
    DeprecationWarning,
    stacklevel=2,
)

_SALT_LENGTH: int = 32
_PBKDF2_ITERATIONS: int = 600_000

__all__ = ["hash_password", "verify_password"]


def hash_password(password: str, *, salt: bytes | None = None) -> str:
    """Hash a password using PBKDF2-SHA256."""
    if salt is None:
        salt = secrets.token_bytes(_SALT_LENGTH)
    dk = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, iterations=_PBKDF2_ITERATIONS
    )
    return f"{salt.hex()}${dk.hex()}"


def verify_password(*, password: str, hashed: str) -> bool:
    """Verify a password against a PBKDF2-SHA256 hash."""
    try:
        salt_hex, _ = hashed.split("$", maxsplit=1)
        salt = bytes.fromhex(salt_hex)
    except ValueError:
        return False
    expected = hash_password(password, salt=salt)
    return secrets.compare_digest(expected, hashed)

"""Cryptographic utility functions."""

from __future__ import annotations

import hashlib
import secrets

_TOKEN_BYTES = 32


def generate_token(*, nbytes: int = _TOKEN_BYTES) -> str:
    """Generate cryptographically secure random token.

    Args:
        nbytes (int): Number of random bytes.

    Returns:
        str: URL-safe base64-encoded token.
    """
    return secrets.token_urlsafe(nbytes)


def hash_sha256(value: str) -> str:
    """Compute SHA-256 hex digest of string.

    Args:
        value (str): String to hash.

    Returns:
        str: Hex-encoded SHA-256 digest.
    """
    return hashlib.sha256(value.encode()).hexdigest()

"""Cryptographic hashing utilities — implements :class:`PasswordHasher` port."""

from __future__ import annotations

import hashlib
import secrets

_SALT_LENGTH: int = 32
_PBKDF2_ITERATIONS: int = 600_000


class PBKDF2PasswordHasher:
    """PBKDF2-SHA256 password hasher implementing the :class:`PasswordHasher` port."""

    def hash(self, password: str, *, salt: bytes | None = None) -> str:
        """Hash a password using PBKDF2-SHA256 with a random salt.

        Args:
            password (str): Plain-text password to hash.
            salt (bytes | None): Optional salt; generated randomly if omitted.

        Returns:
            str: Hash encoded as 'salt_hex$hash_hex'.
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

    def verify(self, *, password: str, hashed: str) -> bool:
        """Verify a password against a PBKDF2-SHA256 hash.

        Args:
            password (str): Plain-text password to verify.
            hashed (str): 'salt_hex$hash_hex' encoded hash.

        Returns:
            bool: 'True' if the password matches.
        """
        try:
            salt_hex, _ = hashed.split("$", maxsplit=1)
            salt = bytes.fromhex(salt_hex)
        except ValueError:
            return False

        expected = self.hash(password, salt=salt)
        return secrets.compare_digest(expected, hashed)


# Convenience functions for backward compatibility
_default_hasher = PBKDF2PasswordHasher()
hash_password = _default_hasher.hash
verify_password = _default_hasher.verify

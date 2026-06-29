"""Token decoder protocol for authentication boundaries."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class TokenDecoder(Protocol):
    """Protocol for decoding and validating authentication tokens."""

    def decode_token(self, token: str) -> object | None:
        """Decode and validate bearer token text.

        Args:
            token (str): Encoded bearer token.

        Returns:
            object | None: Decoded token payload when valid, otherwise None.
        """

        ...

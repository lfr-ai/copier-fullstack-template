"""Core type aliases and NewType definitions.

Keep domain-specific type aliases here so they can be shared across core
without importing from external packages.
"""

from typing import NewType

UserId = NewType("UserId", str)

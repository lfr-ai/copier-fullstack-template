"""SQLAlchemy declarative base and common mixins."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

_UUID_STRING_LENGTH = 36


def _generate_uuid() -> str:
    """Generate a new UUID4 string for use as a primary key.

    Returns:
        str: UUID4 string.
    """
    return str(uuid.uuid4())


class ORMBase(DeclarativeBase):
    """Declarative base for all ORM models."""


class AuditMixin:
    """Mixin providing standard audit timestamp columns.

    Adds created_at and updated_at with server-side defaults.
    """

    created_at: Mapped[datetime] = mapped_column(
        "created_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        "updated_at",
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        index=True,
    )


class IdentityMixin:
    """Mixin providing UUID string primary key.

    Uses a 36-character UUID4 string to match domain
    'Entity.id' for database-agnostic identity.
    """

    id: Mapped[str] = mapped_column(
        "id",
        String(_UUID_STRING_LENGTH),
        primary_key=True,
        default=_generate_uuid,
    )

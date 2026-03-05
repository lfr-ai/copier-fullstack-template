"""SQLAlchemy declarative base and common mixins."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import TIMESTAMP, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


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
    """Mixin providing auto-incrementing integer primary key."""

    id: Mapped[int] = mapped_column(
        "id",
        Integer,
        primary_key=True,
        autoincrement=True,
    )

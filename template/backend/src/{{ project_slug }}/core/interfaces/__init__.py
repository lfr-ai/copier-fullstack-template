"""Domain interface protocols.

Re-exports the most commonly used interfaces for convenient import::

    from {{ project_slug }}.core.interfaces import (
        DocumentRepository,
        EventBus,
        PasswordHasher,
        Repository,
        UnitOfWork,
        UserRepository,
        WorkflowRepository,
    )
"""

from __future__ import annotations

from {{ project_slug }}.core.interfaces.document_repository import DocumentRepository
from {{ project_slug }}.core.interfaces.event_bus import EventBus
from {{ project_slug }}.core.interfaces.password_hasher import PasswordHasher
from {{ project_slug }}.core.interfaces.repository import Repository
from {{ project_slug }}.core.interfaces.unit_of_work import UnitOfWork
from {{ project_slug }}.core.interfaces.user_repository import UserRepository
from {{ project_slug }}.core.interfaces.workflow_repository import WorkflowRepository

__all__ = [
    "DocumentRepository",
    "EventBus",
    "PasswordHasher",
    "Repository",
    "UnitOfWork",
    "UserRepository",
    "WorkflowRepository",
]

"""Domain interface protocols (ports).

Re-exports the most commonly used ports for convenient import::

    from {{ project_slug }}.core.interfaces import (
        DocumentRepositoryPort,
        EventBus,
        PasswordHasher,
        Repository,
        UnitOfWork,
        UserRepositoryPort,
        WorkflowRepositoryPort,
    )
"""

from __future__ import annotations

from {{ project_slug }}.core.interfaces.document_repository import DocumentRepositoryPort
from {{ project_slug }}.core.interfaces.event_bus import EventBus
from {{ project_slug }}.core.interfaces.password_hasher import PasswordHasher
from {{ project_slug }}.core.interfaces.repository import Repository
from {{ project_slug }}.core.interfaces.unit_of_work import UnitOfWork
from {{ project_slug }}.core.interfaces.user_repository import UserRepositoryPort
from {{ project_slug }}.core.interfaces.workflow_repository import WorkflowRepositoryPort

__all__ = [
    "DocumentRepositoryPort",
    "EventBus",
    "PasswordHasher",
    "Repository",
    "UnitOfWork",
    "UserRepositoryPort",
    "WorkflowRepositoryPort",
]

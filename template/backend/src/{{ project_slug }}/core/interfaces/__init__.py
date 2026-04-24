"""Domain interface protocols.

Re-exports the most commonly used interfaces for convenient import::

    from package.core.interfaces import (
        DocumentRepository,
        EventBus,
        PasswordHasher,
        Repository,
        UnitOfWork,
        UserRepository,
        WorkflowRepository,
    )
"""

from .document_repository import DocumentRepository
from .event_bus import EventBus
from .password_hasher import PasswordHasher
from .repository import Repository
from .unit_of_work import UnitOfWork
from .user_repository import UserRepository
from .workflow_repository import WorkflowRepository

__all__ = [
    "DocumentRepository",
    "EventBus",
    "PasswordHasher",
    "Repository",
    "UnitOfWork",
    "UserRepository",
    "WorkflowRepository",
]

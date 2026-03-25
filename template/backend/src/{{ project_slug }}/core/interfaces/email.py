"""Email port — contract for sending email messages."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class EmailPort(Protocol):
    """Port for sending email messages.

    Adapters must implement this protocol to integrate with
    an email delivery backend (SMTP, SendGrid, Azure Communication
    Services, etc.).
    """

    async def send(
        self,
        *,
        to: str,
        subject: str,
        body: str,
        from_addr: str = "",
    ) -> None:
        """Send a single email message.

        If 'from_addr' is empty the adapter uses its configured default.
        """
        ...

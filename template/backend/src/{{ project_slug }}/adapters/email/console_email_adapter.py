"""Console email adapter — logs emails to stdout for development."""

from __future__ import annotations

import structlog

from {{ project_slug }}.config.constants import DEFAULT_FROM_ADDRESS

__all__ = ["ConsoleEmailAdapter"]

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)


class ConsoleEmailAdapter:
    """Log email messages to the console instead of sending them.

    Use this adapter during local development and testing.
    """

    __slots__ = ()

    async def send(
        self,
        *,
        to: str,
        subject: str,
        body: str,
        from_addr: str = DEFAULT_FROM_ADDRESS,
    ) -> None:
        """Print the email to the console logger.

        Args:
            to (str): Recipient email address.
            subject (str): Email subject line.
            body (str): Email body content.
            from_addr (str): Sender email address.
        """
        logger.info(
            "EMAIL (console)\n  From: %s\n  To: %s\n  Subject: %s\n  Body:\n%s",
            from_addr,
            to,
            subject,
            body,
        )

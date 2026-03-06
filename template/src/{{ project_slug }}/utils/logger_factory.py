"""Structured logging factory using structlog."""

from __future__ import annotations

import logging
import sys

import structlog


def _get_shared_processors() -> list[structlog.types.Processor]:
    """Build shared structlog processors.

    Returns:
        Shared processor chain.
    """
    return [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]


def _get_renderer(*, json_output: bool) -> structlog.types.Processor:
    """Build renderer based on output mode.

    Args:
        json_output: Use JSON log renderer.

    Returns:
        Renderer processor.
    """
    if json_output:
        return structlog.processors.JSONRenderer()
    return structlog.dev.ConsoleRenderer()


def _configure_structlog(
    *,
    shared_processors: list[structlog.types.Processor],
) -> None:
    """Configure structlog integration.

    Args:
        shared_processors: Shared processor chain.
    """

    structlog.configure(
        processors=[
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )


def _build_handler(
    *,
    renderer: structlog.types.Processor,
) -> logging.Handler:
    """Build stream handler with processor formatter.

    Args:
        renderer: Renderer processor.

    Returns:
        Configured log handler.
    """

    formatter = structlog.stdlib.ProcessorFormatter(
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    return handler


def configure_logging(*, log_level: str = "INFO", json_output: bool = False) -> None:
    """Configure structured logging for the application.

    Args:
        log_level: Minimum log level (DEBUG, INFO, WARNING, ERROR).
        json_output: Use JSON renderer for machine-parseable logs.
    """
    shared_processors = _get_shared_processors()
    renderer = _get_renderer(json_output=json_output)
    _configure_structlog(shared_processors=shared_processors)
    handler = _build_handler(renderer=renderer)

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(getattr(logging, log_level.upper()))

"""Checkpoint adapters for durable LangGraph workflow execution."""

import structlog

logger: structlog.stdlib.BoundLogger = structlog.get_logger(__name__)
def create_memory_checkpointer() -> object:
    """Create an in-memory checkpointer for development/testing.

    Returns:
        A 'MemorySaver' instance from 'langgraph.checkpoint.memory'.

    Raises:
        ImportError: If 'langgraph' is not installed.
    """
    from langgraph.checkpoint.memory import MemorySaver

    logger.info("Using in-memory checkpointer (not durable)")
    return MemorySaver()


def create_sqlite_checkpointer(
    *,
    db_path: str = ".langgraph_checkpoints.db",
) -> object:
    """Create a SQLite-backed checkpointer for durable local execution.

    Zero-infrastructure alternative to PostgreSQL -- suitable for
    local development and single-process deployments.

    Args:
        db_path (str): File path for the SQLite database.
            Defaults to '.langgraph_checkpoints.db' in the working directory.

    Returns:
        A 'SqliteSaver' instance ready for use.

    Raises:
        ImportError: If 'langgraph' is not installed.
    """
    from langgraph.checkpoint.sqlite import SqliteSaver

    saver = SqliteSaver.from_conn_string(db_path)
    logger.info("SQLite checkpointer initialized: %s", db_path)
    return saver


async def create_postgres_checkpointer(
    *,
    connection_string: str,
) -> object:
    """Create a PostgreSQL-backed checkpointer for durable execution.

    Automatically runs the setup migration to create required tables.

    Args:
        connection_string (str): PostgreSQL connection string
            (e.g. 'postgresql+asyncpg://user:pass@host/db').
            The '+asyncpg' driver suffix is stripped for compatibility
            with 'psycopg' used internally by the checkpoint library.

    Returns:
        An 'AsyncPostgresSaver' instance ready for use.

    Raises:
        ImportError: If 'langgraph-checkpoint-postgres' is not installed.
    """
    from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

    # langgraph-checkpoint-postgres uses psycopg, not asyncpg
    conn_str = connection_string.replace("+asyncpg", "").replace("+psycopg", "")

    saver = AsyncPostgresSaver.from_conn_string(conn_str)
    await saver.setup()
    logger.info("PostgreSQL checkpointer initialized")
    return saver

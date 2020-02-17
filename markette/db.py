import asyncpg

from markette import settings

_pool = None


async def initialize():
    """Create a connection pool."""
    global _pool
    _pool = await asyncpg.create_pool(
        dsn=str(settings.DATABASE_DSN),
        min_size=7,
        max_size=7,
        timeout=5,
    )


async def shutdown():
    """Close the connection pool."""
    await _pool.close()


async def get_connection():
    """
    Get a connection from the pool.

    The connection (conn) will be released back
    to the pool by calling `conn.close()`.

    Returns:
        asyncpg.connection.Connection
    """
    return await _pool.acquire()

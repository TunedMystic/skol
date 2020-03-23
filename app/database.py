from contextlib import asynccontextmanager

import asyncpg

from app import settings

_pool = None


async def connect(dsn=None):
    global _pool
    _pool = await asyncpg.create_pool(
        dsn=settings.database_dsn(),
        min_size=7,
        max_size=7,
        timeout=5,
    )


async def close():
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


@asynccontextmanager
async def grab_connection():
    """
    Yield a connection from the pool.

    The connection (conn) will be released back
    to the pool after the context manager exits.

    Returns:
        asyncpg.connection.Connection
    """
    async with _pool.acquire() as conn:
        yield conn

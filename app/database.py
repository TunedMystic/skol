from contextlib import asynccontextmanager

import asyncpg

from app import settings

_pool = None


async def connect(dsn=None):
    """
    Create database pool.

    What should the size of the pool be?
    Ref: https://stackoverflow.com/questions/60233495
    """
    global _pool
    _pool = await asyncpg.create_pool(
        dsn=settings.database_dsn(),
        min_size=1,
        max_size=1,
        timeout=5,
    )


async def close():
    await _pool.close()


async def get_connection():
    """
    Get a connection from the pool.

    The connection (conn) will be released back
    to the pool by calling the returned function.

    Returns:
        asyncpg.connection.Connection, func
    """
    conn = await _pool.acquire()
    return conn, lambda: _pool.release(conn)


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

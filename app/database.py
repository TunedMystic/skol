from contextlib import asynccontextmanager

import asyncpg

from app import settings

_pool = None


async def connect(dsn=None):
    """Create a connection pool."""
    global _pool

    if not dsn:
        dsn = str(settings.DATABASE_DSN)

    _pool = await asyncpg.create_pool(
        dsn=dsn,
        min_size=7,
        max_size=7,
        timeout=5,
    )


async def close():
    """Close the connection pool."""
    await _pool.close()


async def initialize(dsn=None):
    """
    Initialize the database by performing the following:
        - Make db connection pool
        - Make tables
        - Run migrations
    """
    await connect(dsn)
    async with grab_connection() as conn:
        await conn.fetchrow('select 1 as message;')
        print('Database connection: ✅')


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

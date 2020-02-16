# import asyncpg
from databases import Database

from markette import settings

# _pool = None
database = None


async def connect():
    global database
    database = Database(settings.DATABASE_DSN)
    await database.connect()


async def disconnect():
    await database.disconnect()


# async def connect():
#     global _pool

#     if _pool and not _pool._closed:
#         print('DB is already connected')
#         return

#     print(f'setting up db {settings.DATABASE_DSN}')

#     _pool = await asyncpg.create_pool(settings.DATABASE_DSN)


# async def disconnect():
#     if _pool and _pool._closed:
#         print('DB is already disconnected')
#         return

#     _pool.close()


# async def conn():
#     conn = await _pool.acquire()
#     return conn

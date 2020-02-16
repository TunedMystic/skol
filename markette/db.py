from databases import Database

from markette import settings


database = None


async def connect():
    global database
    database = Database(settings.DATABASE_DSN)
    await database.connect()


async def disconnect():
    await database.disconnect()

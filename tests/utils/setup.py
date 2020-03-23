import asyncio
from pathlib import Path

import asyncpg

from app.main import settings


async def setup_database():
    # Make test database.
    conn = await asyncpg.connect(str(settings.DATABASE_DSN))
    await conn.execute('DROP DATABASE IF EXISTS test;')
    await conn.execute('CREATE DATABASE test;')
    await conn.execute('GRANT ALL PRIVILEGES ON DATABASE test to postgres;')
    await conn.close()
    print('Created test database')

    # Connect to test database, and load schema.
    conn = await asyncpg.connect(str(settings.TEST_DATABASE_DSN))

    # Read the schema file and execute it.
    # Skip if the schema file if not found, or the schema file is empty.
    try:
        schema = Path('sql/schema.sql').open().read()
        if not schema:
            raise FileNotFoundError()
    except FileNotFoundError:
        print('Schema not found')
        return

    await conn.execute(schema)
    await conn.close()
    print('Loaded db schema')


if __name__ == '__main__':
    asyncio.run(setup_database())

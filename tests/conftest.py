import asyncio
import logging

import asyncpg
import pytest
from migo import Migrator
from starlette.testclient import TestClient

from app import database, settings
from app.main import app

logger = logging.getLogger(__name__)

assert settings.TESTING, 'Must be a test environment'


@pytest.yield_fixture(scope='session')
def event_loop(request):
    """
    Create an instance of the default event loop for each test case.
    Ref: https://github.com/pytest-dev/pytest-asyncio/issues/75
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def db():
    """
    Create and return the test database.
    """

    # Create the test database.
    logger.info('Creating test database')
    conn = await asyncpg.connect(str(settings.DATABASE_DSN))
    await conn.execute('DROP DATABASE IF EXISTS test;')
    await conn.execute('CREATE DATABASE test;')
    await conn.execute('GRANT ALL PRIVILEGES ON DATABASE test to postgres;')
    await conn.close()

    # Migrate database.
    logger.info('Running migrations')
    m = Migrator(dsn=settings.TEST_DATABASE_DSN)
    await m.setup()
    await m.run_migrations()
    await m.close()

    # Make database connection and return.
    await database.connect()
    yield database
    await database.close()


@pytest.fixture(scope='function')
async def conn(db):
    """
    Return a connection from the database pool.
    """
    conn, done = await db.get_connection()
    tr = conn.transaction()
    await tr.start()
    yield conn
    await tr.rollback()
    await done()


@pytest.fixture(scope='session')
def client():
    """
    Return a test client for the app.

    Use TestClient as context manager to run startup and shutdown handlers.
    Ref: https://www.starlette.io/events/#running-event-handlers-in-tests

    def test__homepage(client):
        with client:
            response = client.get('/')
            assert response.status_code == 200
    """
    return TestClient(app=app)

import asyncio

import pytest
from migo import Migrator
from starlette.testclient import TestClient

from app import database, settings
from app.main import app

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
    await database.connect()

    async with database.grab_connection() as conn:
        user = settings.DATABASE_DSN.username
        name = 'test'
        await conn.execute(f'DROP DATABASE IF EXISTS {name};')
        await conn.execute(f'CREATE DATABASE {name};')
        await conn.execute(f'GRANT ALL PRIVILEGES ON DATABASE {name} to {user};')

    await database.close()

    # Init database.
    dsn = str(settings.TEST_DATABASE_DSN)
    await database.initialize(dsn)

    # Migrate database.
    m = Migrator(dsn)
    await m.setup()
    await m.run_migrations()

    yield database
    await database.close()


@pytest.fixture(scope='function')
async def conn(db):
    """
    Return a connection from the database pool.
    """
    conn = await db.get_connection()
    yield conn
    await conn.close()


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

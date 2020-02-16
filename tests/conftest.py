import asyncio
import os

import pytest
from starlette.testclient import TestClient

from markette import db as _db
from markette.app import app

assert os.getenv('ENV') == 'test', 'Must be a test environment'


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
def client():
    return TestClient(app)


@pytest.fixture(scope='session')
async def db():
    await _db.connect()
    yield _db.database

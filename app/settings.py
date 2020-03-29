import logging
import os

from starlette.config import Config
from starlette.datastructures import URL

config = Config(environ=os.environ)


# Paths / logging

PROJECT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(PROJECT_DIR)


# Environment

APP_ENV = config('APP_ENV', default='dev').lower()
TESTING = APP_ENV == 'test'
DEV = APP_ENV == 'dev'
PROD = APP_ENV == 'prod'


# Database

DATABASE_DSN = config('DATABASE_DSN', cast=URL)
TEST_DATABASE_DSN = DATABASE_DSN.replace(path='test')


# Logging

LOG_LEVEL = config('LOG_LEVEL', default='INFO')
logger = logging.getLogger()
logger.setLevel(logging.getLevelName(LOG_LEVEL))


# Helper functions

def database_dsn():
    if TESTING:
        return str(TEST_DATABASE_DSN)
    return str(DATABASE_DSN)

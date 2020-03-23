import os

from starlette.config import Config
from starlette.datastructures import URL

config = Config(environ=os.environ)

PROJECT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(PROJECT_DIR)

LOG_LEVEL = config('LOG_LEVEL', default='INFO')

ENV = config('ENV', default='dev')

TESTING = ENV == 'test'
DEV = ENV == 'dev'
PROD = ENV == 'prod'

DATABASE_DSN = config('DATABASE_DSN', cast=URL)
TEST_DATABASE_DSN = DATABASE_DSN.replace(path='test')


def database_dsn():
    if TESTING:
        return str(TEST_DATABASE_DSN)
    return str(DATABASE_DSN)

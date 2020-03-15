import os

from starlette.config import Config
from starlette.datastructures import URL

config = Config(environ=os.environ)

ENV = config('ENV', default='dev')

TESTING = ENV == 'test'
DEV = ENV == 'dev'
PROD = ENV == 'prod'

DATABASE_DSN = config('DATABASE_DSN', cast=URL)
TEST_DATABASE_DSN = DATABASE_DSN.replace(path='test')

LOG_LEVEL = config('LOG_LEVEL', default='INFO')

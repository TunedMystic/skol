import os

from starlette.config import Config
from starlette.datastructures import URL

config = Config(environ=os.environ)

# 'dev', 'stage', 'prod', 'test'
ENVIRONMENT = config('ENVIRONMENT', default='dev')

# 'postgresql://user:pass@host:port/db'
DATABASE_DSN = config('DATABASE_DSN', cast=URL, default='postgresql://postgres:postgres@localhost:5432/postgres')

if ENVIRONMENT == 'test':
    DATABASE_DSN = DATABASE_DSN.replace(path='test')

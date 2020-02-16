import os

from starlette.config import Config
from starlette.datastructures import URL

config = Config(environ=os.environ)

ENV = config('ENV', default='dev')

DATABASE_DSN = config('DATABASE_DSN', cast=URL)

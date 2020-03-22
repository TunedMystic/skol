import logging
from contextlib import contextmanager

from psycopg2.extras import DictCursor
from psycopg2.pool import SimpleConnectionPool as Pool

from app import settings

logger = logging.getLogger(__name__)

_pool = None


def connect():
    global _pool
    _pool = Pool(minconn=1,
                 maxconn=10,
                 cursor_factory=DictCursor,
                 dsn=settings.database_dsn())


def close():
    _pool.closeall()


@contextmanager
def cursor():
    """
    Create a quick cursor.
    Ref: https://github.com/psycopg/psycopg2/pull/367#issuecomment-241582921
    """
    try:
        conn = _pool.getconn()
        with conn:
            with conn.cursor() as cursor:
                yield cursor
    except Exception as e:
        logging.error(f'[quick_cursor] {str(e)}')
        raise e
    finally:
        _pool.putconn(conn)


def get_cursor():
    conn = _pool.getconn()
    conn.autocommit = True
    cursor = conn.cursor(cursor_factory=DictCursor)

    def close():
        conn.close()
        _pool.putconn(conn)

    return cursor, close

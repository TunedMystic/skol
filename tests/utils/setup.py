from pathlib import Path

import psycopg2

from app.main import settings


def setup_database():
    # Make test database.
    conn = psycopg2.connect(str(settings.DATABASE_DSN))
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute('DROP DATABASE IF EXISTS test;')
    cursor.execute('CREATE DATABASE test;')
    cursor.execute('GRANT ALL PRIVILEGES ON DATABASE test to postgres;')
    conn.close()
    print('Created test database')

    # Connect to test database, and load schema.
    conn = psycopg2.connect(str(settings.TEST_DATABASE_DSN))
    conn.autocommit = True

    # Read the schema file and execute it.
    # Skip if the schema file if not found, or the schema file is empty.
    try:
        schema = Path('sql/schema.sql').open().read()
        if not schema:
            raise FileNotFoundError()
    except FileNotFoundError:
        print('Schema not found')
        return

    cursor = conn.cursor()
    cursor.execute(schema)
    conn.close()
    print('Loaded db schema')


if __name__ == '__main__':
    setup_database()

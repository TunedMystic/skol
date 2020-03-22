from unittest import TestCase

from starlette.testclient import TestClient

from app.main import app, database


class BaseTestCase(TestCase):
    def setUp(self):
        self.client = TestClient(app=app)

    def tearDown(self):
        database.connect()

        # Drop all table data.
        with database.cursor() as cursor:
            cursor.execute('''
                SELECT table_name as name
                FROM information_schema.tables
                WHERE table_schema='public';
            ''')
            tables = [row['name'] for row in cursor.fetchall()]

            # If there are no tables, then simply return.
            if not tables:
                return

            cursor.execute(f"TRUNCATE {', '.join(tables)}")

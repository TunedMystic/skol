from app import database
from tests.base import BaseTestCase


class TestSomething(BaseTestCase):
    def test__cursor__context_manager__success(self):
        database.connect()

        with database.cursor() as c:
            c.execute('select 1 as message')
            row = c.fetchone()

        database.close()

        self.assertEqual(dict(row), {'message': 1})
        self.assertTrue(database._pool.closed)

    def test__cursor__context_manager__fail(self):
        database.connect()

        with self.assertRaises(Exception) as e:
            with database.cursor() as c:
                c.execute('this should fail')

        self.assertTrue(str(e.exception).startswith('syntax error at or near "this"'))

    def test__get_cursor(self):
        database.connect()

        cursor, close = database.get_cursor()
        cursor.execute('select 1 as message')
        row = cursor.fetchone()
        close()

        self.assertEqual(dict(row), {'message': 1})
        self.assertTrue(cursor.closed)

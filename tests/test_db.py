import asyncio
import unittest


class DBTestCase(unittest.TestCase):
    async def check(self):
        return 'hi'

    def test_check(self):
        result = asyncio.run(self.check())
        self.assertEqual(result, 'hi')

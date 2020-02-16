import os
import unittest

from starlette.testclient import TestClient


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['ENVIRONMENT'] = 'test'
        from markette.app import app
        self.client = TestClient(app)

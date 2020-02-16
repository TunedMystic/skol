from starlette import status

from .base import BaseTestCase


class TestEndpoints(BaseTestCase):
    def test__homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('text/plain', response.headers['content-type'])

    def test__version(self):
        response = self.client.get('/version')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('application/json', response.headers['content-type'])

    def test__message(self):
        # TestClient as context manager, to run startup and shutdown handlers.
        # Ref: https://www.starlette.io/events/#running-event-handlers-in-tests
        with self.client:
            response = self.client.get('/message')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('application/json', response.headers['content-type'])

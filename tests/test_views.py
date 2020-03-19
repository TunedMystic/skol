from starlette import status
from starlette.testclient import TestClient

from app.main import app
from tests.base import BaseTestCase


class TestSomething(BaseTestCase):
    def setUp(self):
        self.client = TestClient(app=app)

    def test__thing(self):
        self.assertEqual(1 + 2, 3)

    def test__homepage(self):
        response = self.client.get('/')
        assert response.status_code == status.HTTP_200_OK
        assert 'text/plain' in response.headers['content-type']

    def test__version(self):
        response = self.client.get('/version')
        assert response.status_code == status.HTTP_200_OK
        assert 'application/json' in response.headers['content-type']

    def test__products__list(self):
        response = self.client.get('/products')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 5

    def test__products__create(self):
        response = self.client.post('/products')
        assert response.status_code == status.HTTP_201_CREATED

    def test__message(self):
        # TestClient as context manager, to run startup and shutdown handlers.
        # Ref: https://www.starlette.io/events/#running-event-handlers-in-tests
        with self.client:
            response = self.client.get('/message')
            assert response.status_code == status.HTTP_200_OK
            assert 'application/json' in response.headers['content-type']

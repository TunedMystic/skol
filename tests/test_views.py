from starlette import status


def test__homepage(client):
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert 'text/plain' in response.headers['content-type']


def test__version(client):
    response = client.get('/version')
    assert response.status_code == status.HTTP_200_OK
    assert 'application/json' in response.headers['content-type']


def test__products__list(client):
    response = client.get('/products')
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5


def test__products__create(client):
    response = client.post('/products')
    assert response.status_code == status.HTTP_201_CREATED


def test__message(client):
    # TestClient as context manager, to run startup and shutdown handlers.
    # Ref: https://www.starlette.io/events/#running-event-handlers-in-tests
    with client:
        response = client.get('/message')
        assert response.status_code == status.HTTP_200_OK
        assert 'application/json' in response.headers['content-type']

from fastapi.testclient import TestClient
from pyfolio.tests.helper import exclude_middleware
from pyfolio.main import app

client = TestClient(exclude_middleware(app, 'TrustedHostMiddleware'))


def test_read_root():
    response = client.get("/v1/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Pyfolio API V1!"}

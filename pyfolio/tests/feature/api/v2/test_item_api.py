from fastapi.testclient import TestClient
from pyfolio.tests.helper import exclude_middleware
from pyfolio.main import app

client = TestClient(exclude_middleware(app, 'TrustedHostMiddleware'))


def test_read_item_list():
    response = client.get("/v2/items")
    assert response.status_code == 200

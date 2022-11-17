from pytest_schema import schema, Or
from faker import Faker
from fastapi.testclient import TestClient
from pyfolio.tests.helper import exclude_middleware
from pyfolio.main import app

client = TestClient(exclude_middleware(app, 'TrustedHostMiddleware'))

fake = Faker()

menu_list_structure = {
    "message": Or(None, str),
    "data": {
        "total": int,
        "limit": int,
        "skip": int,
        "total_page": int,
        "next_page_link": Or(None, str),
        "items": [
            {
                "id": int,
                "title": str,
                "group": str,
                "url": str,
                "target": str,
                "is_active": bool,
                "created_at": Or(None, str),
                "updated_at": Or(None, str),
            }
        ]
    }
}

menu_detail_structure = {
    "message": Or(None, str),
    "data": {
        "id": int,
        "title": str,
        "group": str,
        "url": str,
        "target": str,
        "is_active": bool,
        "created_at": Or(None, str),
        "updated_at": Or(None, str),
    }
}


class TestMenuApi:

    def test_read_menu_list(self):
        response = client.get("/v1/menus")
        data = response.json()
        assert response.status_code == 200
        assert schema(menu_list_structure) == data

    def test_create_menu_without_duplicate(self):
        payload = {
            "title": fake.text(50) + fake.uuid4(),
            "group": 'top_menu',
            "url": '/',
            "target": '',
            "is_active": True,
        }
        response = client.post("/v1/menus", json=payload)
        response_data = response.json()
        assert response.status_code == 201
        assert response_data['data']['title'] == payload['title']
        assert schema(menu_detail_structure) == response.json()

    def test_create_menu_with_duplicated(self):
        payload = {
            "title": fake.text(50) + fake.uuid4(),
            "group": 'top_menu',
            "url": '/',
            "target": '',
            "is_active": True,
        }

        # Create menu the first times
        response = client.post("/v1/menus", json=payload)

        # Create menu the second times
        response = client.post("/v1/menus", json=payload)

        assert response.status_code == 400

    def test_update_menu(self):
        payload = {
            "title": fake.text(50) + fake.uuid4(),
            "group": 'top_menu',
            "url": '/',
            "target": '',
            "is_active": False,
        }

        # Create menu the first times
        response = client.post("/v1/menus", json=payload)
        created_obj = response.json()['data']

        # Update menu
        payload['is_active'] = True
        response = client.put(f"/v1/menus/{created_obj['id']}", json=payload)
        updated_obj = response.json()['data']

        assert response.status_code == 200
        assert updated_obj['is_active'] is True

    def test_delete_menu(self):
        payload = {
            "title": fake.text(50) + fake.uuid4(),
            "group": 'top_menu',
            "url": '/',
            "target": '',
            "is_active": False,
        }
        response = client.post("/v1/menus", json=payload)
        created_obj = response.json()['data']

        # Delete menu
        response = client.delete(f"/v1/menus/{created_obj['id']}")
        assert response.status_code == 200

        # Get menu
        response = client.get(f"/v1/menus/{created_obj['id']}")
        assert response.status_code == 404

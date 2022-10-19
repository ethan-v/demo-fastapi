from pytest_schema import schema, Or
from faker import Faker
from fastapi.testclient import TestClient
from vinor.builder.tests.helper import exclude_middleware
from vinor.builder import builder_api

client = TestClient(exclude_middleware(builder_api, 'TrustedHostMiddleware'))

fake = Faker()


schema_list_structure = {
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
                "name": str,
                "is_active": bool,
                "created_at": Or(None, str),
                "updated_at": Or(None, str),
            }
        ]
    }
}

schema_detail_structure = {
    "message": Or(None, str),
    "data": {
        "id": int,
        "name": str,
        "is_active": bool,
        "created_at": Or(None, str),
        "updated_at": Or(None, str),
    }
}


class TestSchemaApi:

    def test_read_schema_list(self):
        response = client.get("/schemas/")
        data = response.json()
        assert response.status_code == 200
        assert schema(schema_list_structure) == data

    def test_create_schema_without_duplicate(self):
        payload = {
            "name": fake.uuid4(),
            "is_active": True
        }
        response = client.post("/schemas/", json=payload)
        response_data = response.json()

        assert response.status_code == 201
        assert response_data['data']['is_active'] == payload['is_active']
        assert response_data['data']['name'] == payload['name']
        assert schema(schema_detail_structure) == response.json()

    def test_create_schema_with_duplicated(self):
        payload = {
            "name": fake.uuid4(),
            "is_active": True
        }

        # Create schema the first times
        response = client.post("/schemas/", json=payload)

        # Create schema the second times
        response = client.post("/schemas/", json=payload)

        assert response.status_code == 400
        assert response.json() == {"detail": "Name already exists"}

    def test_update_schema(self):
        payload = {
            "name": fake.uuid4(),
            "is_active": True
        }

        # Create schema the first times
        response = client.post("/schemas/", json=payload)
        created_obj = response.json()['data']

        # Update schema
        payload['name'] = fake.uuid4()
        response = client.put(f"/schemas/{created_obj['id']}", json=payload)
        updated_obj = response.json()['data']

        assert response.status_code == 200
        assert updated_obj['name'] == payload['name']

    def test_delete_schema(self):
        payload = {
            "name": fake.uuid4(),
            "is_active": True
        }
        response = client.post("/schemas/", json=payload)
        created_obj = response.json()['data']

        # Delete schema
        response = client.delete(f"/schemas/{created_obj['id']}")
        assert response.status_code == 200

        # Get schema
        response = client.get(f"/schemas/{created_obj['id']}")
        assert response.status_code == 404

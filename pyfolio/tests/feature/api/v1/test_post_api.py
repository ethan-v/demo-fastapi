from pytest_schema import schema, Or
from faker import Faker
from fastapi.testclient import TestClient
from pyfolio.tests.helper import exclude_middleware
from pyfolio.main import app

client = TestClient(exclude_middleware(app, 'TrustedHostMiddleware'))

fake = Faker()


post_list_structure = {
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
                "slug": Or(None, str),
                "image": Or(None, str),
                "content": Or(None, str),
                "category_id": int,
                "is_active": bool,
                "created_at": Or(None, str),
                "updated_at": Or(None, str),
            }
        ]
    }
}

post_detail_structure = {
    "message": Or(None, str),
    "data": {
        "id": int,
        "title": str,
        "slug": Or(None, str),
        "image": Or(None, str),
        "content": Or(None, str),
        "category_id": int,
        "is_active": bool,
        "created_at": Or(None, str),
        "updated_at": Or(None, str),
    }
}


class TestCardModelApi:

    def test_read_post_list(self):
        response = client.get("/v1/posts/")
        data = response.json()
        print(data)
        assert response.status_code == 200
        assert schema(post_list_structure) == data

    def test_create_post_without_duplicate(self):
        payload = {
            "title": fake.uuid4(),
            "slug": fake.uuid4(),
            "image": fake.text(),
            "content": fake.uuid4(),
            "category_id": fake.random_number(),
            "is_active": True
        }
        response = client.post("/v1/posts/", json=payload)
        response_data = response.json()

        assert response.status_code == 201
        assert response_data['data']['is_active'] == payload['is_active']
        assert response_data['data']['title'] == payload['title']
        assert schema(post_detail_structure) == response.json()

    def test_create_post_with_duplicated(self):
        payload = {
            "title": fake.uuid4(),
            "slug": fake.uuid4(),
            "image": fake.text(),
            "content": fake.text(),
            "category_id": fake.random_number(),
            "is_active": True
        }

        # Create car model the first times
        response = client.post("/v1/posts/", json=payload)

        # Create car model the second times
        response = client.post("/v1/posts/", json=payload)

        assert response.status_code == 400
        assert response.json() == {"detail": "Title already exists"}

    def test_update_post(self):
        payload = {
            "title": fake.uuid4(),
            "slug": fake.uuid4(),
            "image": fake.text(),
            "content": fake.text(),
            "category_id": fake.random_number(),
            "is_active": True
        }

        # Create car model the first times
        response = client.post("/v1/posts/", json=payload)
        created_obj = response.json()['data']

        # Update car model
        payload['content'] = 'my content'
        response = client.put(f"/v1/posts/{created_obj['id']}", json=payload)
        updated_obj = response.json()['data']

        assert response.status_code == 200
        assert updated_obj['content'] == 'my content'

    def test_delete_post(self):
        payload = {
            "title": fake.uuid4(),
            "slug": fake.uuid4(),
            "image": fake.text(),
            "content": fake.text(),
            "category_id": fake.random_number(),
            "is_active": True
        }
        response = client.post("/v1/posts/", json=payload)
        created_obj = response.json()['data']

        # Delete car model
        response = client.delete(f"/v1/posts/{created_obj['id']}")
        assert response.status_code == 200

        # Get car model
        response = client.get(f"/v1/posts/{created_obj['id']}")
        assert response.status_code == 404
import pytest
from pytest_schema import schema, Or
from faker import Faker
from fastapi.testclient import TestClient

from vinor.builder.field.builder_field_models import BuilderFieldBase
from vinor.builder.generator import convert_value_to_datatype
from vinor.builder.tests.helper import exclude_middleware
from vinor.builder import builder_api

client = TestClient(exclude_middleware(builder_api, 'TrustedHostMiddleware'))

fake = Faker()

resource_data_detail_structure = {
    "message": Or(None, str),
    "data": {
        "id": int,
        "first_name": str,
        "last_name": str,
        "email": Or(None, str),
        "avatar": Or(None, str),
        "website": Or(None, str),
        "is_active": True,
        "created_at": Or(None, str),
        "updated_at": Or(None, str),
    }
}

resource_data_list_structure = {
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
                "first_name": str,
                "last_name": str,
                "email": Or(None, str),
                "avatar": Or(None, str),
                "website": Or(None, str),
                "is_active": True,
                "created_at": Or(None, str),
                "updated_at": Or(None, str),
            }
        ]
    }
}


class TestBuilderResourceApi:
    RESOURCE_NAME: str = 'member'
    RESOURCE_RECORD_SINGLE = {
        "id": 1,
        "first_name": "Ethan",
        "last_name": "Vu",
        "email": "ethanvu.dev@gmail.com",
        "avatar": "https://avatars.githubusercontent.com/u/101924640",
        "website": "https://ethanvu.dev",
        "is_active": True,
        "created_at": "2022-10-10 08:00:00",
        "updated_at": "2022-10-10 22:00:00",
    }
    CREATED_RECORD: dict = {}

    def test_create_table_columns(self):
        # Setup resource before test CRUD resource api
        payload = {
            "name": self.RESOURCE_NAME,
            "is_active": True,
        }
        response = client.post("/schemas/", json=payload)
        response_data = response.json()
        assert response.status_code == 201
        assert response_data['data']['name'] == payload['name']

        # Setup resource columns
        for field_name, field_value in self.RESOURCE_RECORD_SINGLE.items():
            field = BuilderFieldBase(
                name=field_name,
                schema_name=self.RESOURCE_NAME,
                data_type=convert_value_to_datatype(field_value),
                default=None,
                relation_mapping=None,
                comment=None,
                is_required=True,
                in_request=True,
                in_request_name=None,
                in_response=True,
                in_response_name=None,
                callback_function=None,
                created_at=None,
                updated_at=None,
            )
            field_payload = field.dict()
            response_field = client.post("/fields/", json=field_payload)
            response_field_data = response_field.json()
            assert response_field_data["data"]["name"] == field_payload["name"]
            assert response_field_data["data"]["schema_name"] == field_payload["schema_name"]
            assert response_field.status_code == 201

    @pytest.fixture(scope="module", name='created_record')
    def test_create_resource_record(self):
        payload = {
            "first_name": fake.name(),
            "last_name": fake.name(),
            "email": fake.email(),
            "avatar": fake.image_url(),
            "website": fake.uri(),
            "is_active": True,
            "created_at": "2022-10-10 08:00:00",
            "updated_at": "2022-10-10 22:00:00",
        }
        response = client.post(f"/resource/{self.RESOURCE_NAME}", json=payload)
        response_data = response.json()

        assert response.status_code == 201
        for key, value in payload.items():
            assert response_data['data'][key] == payload[key]
        assert schema(resource_data_detail_structure) == response.json()

        yield response_data['data']

    def test_read_resource_records_list(self):
        response = client.get(f"/resource/{self.RESOURCE_NAME}/list")
        data = response.json()
        assert response.status_code == 200
        assert schema(resource_data_list_structure) == data

    def test_read_resource_record_detail(self, created_record):
        response = client.get(f"/resource/{self.RESOURCE_NAME}/detail/{created_record['id']}")
        data = response.json()
        assert response.status_code == 200
        assert schema(resource_data_detail_structure) == data

    def test_update_resource_record(self, created_record):
        payload = created_record
        payload['first_name'] = fake.name()

        response = client.put(f"/resource/{self.RESOURCE_NAME}/{created_record['id']}", json=payload)
        updated_obj = response.json()

        assert response.status_code == 200
        assert updated_obj['data']['first_name'] == payload['first_name']

    def test_delete_resource_record(self, created_record):
        response = client.delete(f"/resource/{self.RESOURCE_NAME}/{created_record['id']}")
        assert response.status_code == 200

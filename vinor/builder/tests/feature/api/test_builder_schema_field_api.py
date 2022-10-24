from pytest_schema import schema, Or
from faker import Faker
from fastapi.testclient import TestClient
from vinor.builder.tests.helper import exclude_middleware
from vinor.builder import builder_api

client = TestClient(exclude_middleware(builder_api, "TrustedHostMiddleware"))

fake = Faker()

schema_field_list_structure = {
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
                "schema_name": str,
                "data_type": str,
                "default": Or(str, None),
                "relation_mapping": Or(str, None),
                "comment": Or(str, None),
                "is_required": bool,
                "in_request": bool,
                "in_request_name": Or(str, None),
                "in_response": bool,
                "in_response_name": Or(str, None),
                "callback_function": Or(str, None),
                "created_at": Or(None, str),
                "updated_at": Or(None, str),
            }
        ]
    }
}

schema_field_detail_structure = {
    "message": Or(None, str),
    "data": {
        "id": int,
        "name": str,
        "schema_name": str,
        "data_type": str,
        "default": Or(str, None),
        "relation_mapping": Or(str, None),
        "comment": Or(str, None),
        "is_required": bool,
        "in_request": bool,
        "in_request_name": Or(str, None),
        "in_response": bool,
        "in_response_name": Or(str, None),
        "callback_function": Or(str, None),
        "created_at": Or(None, str),
        "updated_at": Or(None, str),
    }
}


class TestBuilderSchemaFieldApi:

    def test_create_schema_field(self):
        payload = {
            "name": "name",
            "schema_name": "tbl_members",
            "data_type": "str",
            "default": None,
            "relation_mapping": None,
            "comment": "Course name",
            "is_required": True,
            "in_request": True,
            "in_request_name": None,
            "in_response": True,
            "in_response_name": None,
            "callback_function": None,
        }
        response = client.post("/fields/", json=payload)
        response_data = response.json()

        assert response.status_code == 201
        assert response_data["data"]["name"] == payload["name"]
        assert response_data["data"]["schema_name"] == payload["schema_name"]
        assert schema(schema_field_detail_structure) == response.json()

    def test_read_schema_field_list(self):
        response = client.get("/fields/")
        data = response.json()
        assert response.status_code == 200
        assert schema(schema_field_list_structure) == data

    # def test_update_schema(self):
    #     payload = {
    #         "name": "name",
    #         "schema_name": "tbl_members",
    #         "data_type": "str",
    #         "default": None,
    #         "relation_mapping": None,
    #         "comment": "Course name",
    #         "is_required": True,
    #         "in_request": True,
    #         "in_request_name": None,
    #         "in_response": True,
    #         "in_response_name": None,
    #         "callback_function": None,
    #     }
    #
    #     # Create schema the first times
    #     response = client.post("/fields/", json=payload)
    #     created_obj = response.json()["data"]
    #
    #     # Update schema
    #     payload["name"] = fake.uuid4()
    #     response = client.put(f"/fields/{created_obj['id']}", json=payload)
    #     updated_obj = response.json()["data"]
    #
    #     assert response.status_code == 200
    #     assert updated_obj["name"] == payload["name"]
    #
    # def test_delete_schema(self):
    #     payload = {
    #         "name": "name",
    #         "schema_name": "tbl_members",
    #         "data_type": "str",
    #         "default": None,
    #         "relation_mapping": None,
    #         "comment": "Course name",
    #         "is_required": True,
    #         "in_request": True,
    #         "in_request_name": None,
    #         "in_response": True,
    #         "in_response_name": None,
    #         "callback_function": None,
    #     }
    #     response = client.post("/fields/", json=payload)
    #     created_obj = response.json()["data"]
    #
    #     # Delete schema
    #     response = client.delete(f"/fields/{created_obj['id']}")
    #     assert response.status_code == 200
    #
    #     # Get schema
    #     response = client.get(f"/fields/{created_obj['id']}")
    #     assert response.status_code == 404

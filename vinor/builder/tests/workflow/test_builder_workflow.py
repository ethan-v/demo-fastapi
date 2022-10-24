import pytest
from faker import Faker
from fastapi.testclient import TestClient

from vinor.builder import builder_api
from vinor.builder.generator import Generator
from vinor.builder.tests.helper import exclude_middleware

client = TestClient(exclude_middleware(builder_api, 'TrustedHostMiddleware'))

fake = Faker()

workflow_data = {
    "schema": None,
}

example_response_json = {
    "course": {
        "id": 1,
        "title": "Python for Back-end Engineer",
        "slug": "python-for-backend-engineer",
        "image": "https://www.python.org/static/img/python-logo.png",
        "description": "Python background job, script, asynchronous",
        "content": "Python background job, script, asynchronous",
        "price": 4.99,
        "course_category": 1,
    },
    "course_lecture": {
        "id": 1,
        "title": "Basic data type in Python",
        "slug": "basic-data-type-in-python",
    },
    "course_video": {
        "id": 1,
        "course_id": 1,
        "lecture_id": 1,
    }
}


def set_workflow_data(key: str, value: dict):
    workflow_data[key] = value


@pytest.fixture
def step1_create_schema():
    payload = {
        "name": "tbl_members",
        "active": True,
    }
    response = client.post("/schemas/", json=payload)
    response_data = response.json()

    assert response.status_code == 201
    assert response_data['data']['name'] == payload['name']

    set_workflow_data('schema', response_data)

    return 'Created schema: tbl_members'


@pytest.fixture
def step2_create_fields_for_that_schema():
    # payload = {
    #     "name": "name",
    #     "schema_name": workflow_data['schema_name'],
    #     "data_type": "str",
    #     "default": None,
    #     # "relation_mapping": None,
    #     # "comment": "Course name",
    #     # "is_required": True,
    #     # "in_request": True,
    #     # "in_request_name": None,
    #     # "in_response": True,
    #     # "in_response_name": None,
    #     # "callback_function": None,
    # }

    generator = Generator()
    generator.set_example_json_data(example_response_json)
    schemas = generator.generate()

    for schema in schemas:
        schema_payload = schema.dict()
        print(schema_payload)
        response_schema = client.post("/schemas/", json=schema_payload)
        response_data = response_schema.json()
        assert response_data["data"]["name"] == schema_payload["name"]
        assert response_schema.status_code == 201

        for field in schema.fields:
            field_payload = field.dict()
            response_field = client.post("/fields/", json=field_payload)
            response_field_data = response_field.json()
            assert response_field_data["data"]["name"] == field_payload["name"]
            assert response_field_data["data"]["schema_name"] == field_payload["schema_name"]
            assert response_field.status_code == 201

    return 'Created fields for schema: tbl_members'


@pytest.fixture
def step3_send_http_request_for_that_schema():
    return 'Sent http request for schema: tbl_members'


@pytest.fixture
def step4_get_http_response_for_that_schema():
    return 'Get response data for schema: tbl_members'


def test_basic_workflow(
        step1_create_schema,
        step2_create_fields_for_that_schema,
        step3_send_http_request_for_that_schema,
        step4_get_http_response_for_that_schema
):
    assert step1_create_schema == 'Created schema: tbl_members'
    assert step2_create_fields_for_that_schema == 'Created fields for schema: tbl_members'
    assert step3_send_http_request_for_that_schema == 'Sent http request for schema: tbl_members'
    assert step4_get_http_response_for_that_schema == 'Get response data for schema: tbl_members'

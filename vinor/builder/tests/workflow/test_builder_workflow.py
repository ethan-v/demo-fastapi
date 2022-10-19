import pytest


@pytest.fixture
def step1_create_schema():
    return 'Created schema: tbl_members'


@pytest.fixture
def step2_create_fields_for_that_schema():
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

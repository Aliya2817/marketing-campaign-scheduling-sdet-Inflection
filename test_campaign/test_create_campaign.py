import json
from datetime import datetime

import pytest
import requests
from faker import Faker

from config import settings


@pytest.fixture
def successful_campaign_payload():
    fake = Faker()
    return {"campaignName": f"Test Successful Campaign {fake.name()}", "emailTemplateId": "EM-001",
            "recipientListId": "RL-001", "scheduledTime": 1717610495}


@pytest.fixture
def invalid_campaign_id():
    fake = Faker()
    return fake.uuid4()


@pytest.fixture
def valid_campaign_name():
    fake = Faker()
    return f"Campaign {fake.name()}"


@pytest.fixture
def invalid_email_template_campaign_payload():
    fake = Faker()
    return {"campaignName": f"Test Successful Campaign {fake.name()}", "emailTemplateId": "EM-0001",
            "recipientListId": "RL-001", "scheduledTime": 1717610495}


@pytest.fixture
def invalid_recipient_list_campaign_payload():
    fake = Faker()
    return {"campaignName": f"Test Successful Campaign {fake.name()}", "emailTemplateId": "EM-001",
            "recipientListId": "RL-0001", "scheduledTime": 1717610495}


def create_campaign(payload):
    url = settings.CAMPAIGN_SERVICE_BASE_URL
    headers = {'accept': '*/*', 'Content-Type': 'application/json'}

    return requests.post(url, headers=headers, data=json.dumps(payload))


def test_invalid_recipient_list_create_campaign(invalid_recipient_list_campaign_payload):
    response = create_campaign(invalid_recipient_list_campaign_payload)

    # Validate the response status code
    assert response.status_code == 404

    response_data = response.json()

    # Validate the response structure
    assert 'errors' in response_data
    assert 'meta' in response_data

    errors = response_data['errors']
    meta = response_data['meta']

    # Validate meta content
    assert meta['status'] == 'FAILURE'

    # Validate error code
    assert len(errors) > 0
    assert errors[0]['errorCode'] == 'CAM-E-003'


def test_invalid_email_template_create_campaign(invalid_email_template_campaign_payload):
    response = create_campaign(invalid_email_template_campaign_payload)

    # Validate the response status code
    assert response.status_code == 404

    response_data = response.json()

    # Validate the response structure
    assert 'errors' in response_data
    assert 'meta' in response_data

    errors = response_data['errors']
    meta = response_data['meta']

    # Validate meta content
    assert meta['status'] == 'FAILURE'

    # Validate error code
    assert len(errors) > 0
    assert errors[0]['errorCode'] == 'CAM-E-002'


def test_duplicate_create_campaign_test(successful_campaign_payload):
    # Creating campaign twice to make it duplicate
    create_campaign(successful_campaign_payload)
    response = create_campaign(successful_campaign_payload)

    # Validate the response status code
    assert response.status_code == 409

    response_data = response.json()

    # Validate the response structure
    assert 'errors' in response_data
    assert 'meta' in response_data

    errors = response_data['errors']
    meta = response_data['meta']

    # Validate meta content
    assert meta['status'] == 'FAILURE'

    # Validate error code
    assert len(errors) > 0
    assert errors[0]['errorCode'] == 'CAM-E-004'


def test_successful_create_campaign(successful_campaign_payload):
    response = create_campaign(successful_campaign_payload)

    # Validate the response status code
    assert response.status_code == 201

    response_data = response.json()

    # Validate the response structure
    assert 'data' in response_data
    assert 'meta' in response_data

    data = response_data['data']
    meta = response_data['meta']

    # Validate the data content
    assert data['campaignName'] == successful_campaign_payload['campaignName']
    assert data['emailTemplateId'] == successful_campaign_payload['emailTemplateId']
    assert data['recipientListId'] == successful_campaign_payload['recipientListId']
    assert data['scheduledTime'] == successful_campaign_payload['scheduledTime']

    # Validate meta content
    assert meta['status'] == 'SUCCESS'

    # Validate the timestamp format in meta
    try:
        datetime.fromisoformat(meta['timestamp'].replace('Z', '+00:00'))
    except ValueError:
        assert False, "Timestamp format is invalid"


def test_update_campaign_with_invalid_campaign_id(invalid_campaign_id, valid_campaign_name):
    url = f"{settings.CAMPAIGN_SERVICE_BASE_URL}/{invalid_campaign_id}/name"
    payload = json.dumps({"campaignName": valid_campaign_name})
    headers = {'accept': '*/*', 'Content-Type': 'application/json'}
    response = requests.request("PATCH", url, headers=headers, data=payload)

    # Validate the response status code
    assert response.status_code == 404

    response_data = response.json()

    # Validate the response structure
    assert 'errors' in response_data
    assert 'meta' in response_data

    errors = response_data['errors']
    meta = response_data['meta']

    # Validate the error code
    assert len(errors) > 0
    assert errors[0]['errorCode'] == 'CAM-E-001'

    # Validate meta content
    assert meta['status'] == 'FAILURE'


def test_successful_update_campaign(successful_campaign_payload, valid_campaign_name):
    response = create_campaign(successful_campaign_payload)
    campaign_id = response.json()['data']['id']

    url = f"{settings.CAMPAIGN_SERVICE_BASE_URL}/{campaign_id}/name"
    payload = json.dumps({"campaignName": valid_campaign_name})
    headers = {'accept': '*/*', 'Content-Type': 'application/json'}

    response = requests.request("PATCH", url, headers=headers, data=payload)

    # Validate the response status code
    assert response.status_code == 200

    response_data = response.json()

    # Validate the response structure
    assert 'data' in response_data
    assert 'meta' in response_data

    data = response_data['data']
    meta = response_data['meta']

    # Validate the data content
    assert data['campaignName'] == valid_campaign_name

    # Validate meta content
    assert meta['status'] == 'SUCCESS'


def test_successful_fetch_campaign(successful_campaign_payload):
    # First creating a campaign to fetch the same
    response = create_campaign(successful_campaign_payload)
    campaign_id = response.json()['data']['id']

    url = f"{settings.CAMPAIGN_SERVICE_BASE_URL}/{campaign_id}"
    headers = {'accept': '*/*', 'Content-Type': 'application/json'}
    response = requests.request("GET", url, headers=headers)

    # Validate the response status code
    assert response.status_code == 200

    response_data = response.json()

    # Validate the response structure
    assert 'data' in response_data
    assert 'meta' in response_data

    data = response_data['data']
    meta = response_data['meta']

    # Validate the data content
    assert data['campaignName'] == successful_campaign_payload['campaignName']
    assert data['emailTemplateId'] == successful_campaign_payload['emailTemplateId']
    assert data['recipientListId'] == successful_campaign_payload['recipientListId']
    assert data['scheduledTime'] == successful_campaign_payload['scheduledTime']

    # Validate meta content
    assert meta['status'] == 'SUCCESS'

    # Validate the timestamp format in meta
    try:
        datetime.fromisoformat(meta['timestamp'].replace('Z', '+00:00'))
    except ValueError:
        assert False, "Timestamp format is invalid"


def test_fetch_campaign_with_invalid_campaign_id(invalid_campaign_id, valid_campaign_name):
    url = f"{settings.CAMPAIGN_SERVICE_BASE_URL}/{invalid_campaign_id}"
    headers = {'accept': '*/*', 'Content-Type': 'application/json'}
    response = requests.request("GET", url, headers=headers)

    # Validate the response status code
    assert response.status_code == 404

    response_data = response.json()

    # Validate the response structure
    assert 'errors' in response_data
    assert 'meta' in response_data

    errors = response_data['errors']
    meta = response_data['meta']

    # Validate the error code
    assert len(errors) > 0
    assert errors[0]['errorCode'] == 'CAM-E-001'

    # Validate meta content
    assert meta['status'] == 'FAILURE'

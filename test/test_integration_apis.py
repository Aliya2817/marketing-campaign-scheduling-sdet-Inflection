import pytest
import requests

from faker import Faker

from config.settings import *


@pytest.fixture
def valid_campaign_name():
    fake = Faker()
    return f"Campaign {fake.name()}"


def test_integration_apis(valid_campaign_name):
    # URLs for the APIs
    campaigns_url = CAMPAIGN_SERVICE_BASE_URL
    templates_url = EMAIL_TEMPLATE_SERVICE_BASE_URL
    recipients_url = f'{RECIPIENT_SERVICE_BASE_URL}/lists'

    # Headers for requests
    headers = {'accept': '*/*', 'Content-Type': 'application/json'}

    # Fetch email templates
    templates_response = requests.get(templates_url, headers={'accept': '*/*'})
    assert templates_response.status_code == 200
    templates_data = templates_response.json()
    assert 'data' in templates_data and 'meta' in templates_data

    # Fetch recipient lists
    recipients_response = requests.get(recipients_url, headers={'accept': '*/*'})
    assert recipients_response.status_code == 200
    recipients_data = recipients_response.json()
    assert 'data' in recipients_data and 'meta' in recipients_data

    # Extract template and recipient list ids for the campaign creation
    email_template_id = templates_data['data'][0]['id']
    recipient_list_id = recipients_data['data'][0]['id']

    # Campaign payload
    campaign_payload = {"campaignName": valid_campaign_name, "emailTemplateId": email_template_id,
                        "recipientListId": recipient_list_id, "scheduledTime": 1717610495}

    # Create a campaign
    campaign_response = requests.post(campaigns_url, headers=headers, data=json.dumps(campaign_payload))
    assert campaign_response.status_code == 201
    campaign_response_data = campaign_response.json()
    assert 'data' in campaign_response_data and 'meta' in campaign_response_data

    campaign_data = campaign_response_data['data']
    campaign_meta = campaign_response_data['meta']

    # Validate campaign creation response
    assert campaign_data['campaignName'] == campaign_payload['campaignName']
    assert campaign_data['emailTemplateId'] == campaign_payload['emailTemplateId']
    assert campaign_data['recipientListId'] == campaign_payload['recipientListId']
    assert campaign_data['scheduledTime'] == campaign_payload['scheduledTime']
    assert campaign_meta['status'] == 'SUCCESS'

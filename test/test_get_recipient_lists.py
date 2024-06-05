import re

import requests
from datetime import datetime
from config.settings import RECIPIENT_SERVICE_BASE_URL


def test_get_recipient_lists():
    url = f"{RECIPIENT_SERVICE_BASE_URL}/lists"
    headers = {'accept': '*/*'}

    # Send GET request to the API endpoint
    response = requests.get(url, headers=headers)

    # Validate the response status code
    assert response.status_code == 200

    response_data = response.json()

    # Validate the response structure
    assert 'data' in response_data
    assert 'meta' in response_data

    data = response_data['data']
    meta = response_data['meta']

    # Validate the data content
    assert isinstance(data, list)
    assert len(data) > 0, "atleast ast one recipient list must be there"

    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    for item in data:
        assert 'id' in item
        assert 'name' in item
        assert 'recipients' in item
        assert len(item['recipients']) > 0, "atleast ast one recipient must be there"

        for recipient in item['recipients']:
            assert 'id' in recipient
            assert "email" in recipient
            assert re.match(email_regex, recipient['email']), f"Invalid email format: {recipient['email']}"

    # Validate meta content
    assert meta['status'] == 'SUCCESS'

    # Validate the timestamp format in meta
    try:
        datetime.fromisoformat(meta['timestamp'].replace('Z', '+00:00'))
    except ValueError:
        assert False, "Timestamp format is invalid"

import requests
from datetime import datetime
from config.settings import EMAIL_TEMPLATE_SERVICE_BASE_URL


def test_get_email_templates():
    url = EMAIL_TEMPLATE_SERVICE_BASE_URL
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
    assert len(data) > 0, "atleast ast one email template must be there"

    for item in data:
        assert 'id' in item
        assert 'name' in item
        assert 'data' in item

    # Validate meta content
    assert meta['status'] == 'SUCCESS'

    # Validate the timestamp format in meta
    try:
        datetime.fromisoformat(meta['timestamp'].replace('Z', '+00:00'))
    except ValueError:
        assert False, "Timestamp format is invalid"


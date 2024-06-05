# Parsing env
import json

config_path = 'config/config.json'

with open(config_path) as f:
    data = json.load(f)

CAMPAIGN_SERVICE_BASE_URL = data['CAMPAIGN_SERVICE_BASE_URL']
EMAIL_TEMPLATE_SERVICE_BASE_URL = data['EMAIL_TEMPLATE_SERVICE_BASE_URL']
RECIPIENT_SERVICE_BASE_URL = data['RECIPIENT_SERVICE_BASE_URL']

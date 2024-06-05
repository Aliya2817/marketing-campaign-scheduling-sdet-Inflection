from test.test_create_campaign import *
from test.test_get_email_templates import *
from test.test_get_recipient_lists import *

if __name__ == '__main__':
    import pytest
    pytest.main(['--disable-warnings'])

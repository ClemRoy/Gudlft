import pytest
from tests.conftest import client

def test_root(client):
    """
    Given: A user access the site
    When: he access the index url
    Then: we receive a status code 200 
    """
    response = client.get('/')
    assert response.status_code == 200
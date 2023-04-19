import pytest
from tests.conftest import client

def test_root(client):
    response = client.get('/')
    assert response.status_code == 200
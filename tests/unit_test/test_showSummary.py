import pytest
from tests.conftest import client

def test_showSummary_known_email_response_code(client):
    """
    Given: A user access show summary
    When: he input a known email
    Then: we receive a status_code 200
    """
    email = "john@simplylift.co"
    response = client.post('/showSummary',data={"email": email})
    assert response.status_code == 200

def test_showSummary_unknown_email(client):
    """
    Given: A user access show summary
    When: he input an unknown email
    Then: we receive an error message
    """
    email = "johndoe@simplylift.co"
    response = client.post('/showSummary',data={"email": email})
    assert b"There is no account using this email" in response.data


def test_showSummary_template_render(client):
    """
    Given: A user access show summary
    When: he input an unknown email
    Then: the welcome template is rendered
    """
    email = "john@simplylift.co"
    response = client.post('/showSummary',data={"email": email})
    assert b"Welcome, john@simplylift.co" in response.data
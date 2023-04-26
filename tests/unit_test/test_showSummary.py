import pytest
from tests.conftest import client,competitions_with_availability

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
    Then: we are redirected to the index page with an error message
    """
    email = "johndoe@simplylift.co"
    response = client.post('/showSummary',data={"email": email})
    assert response.status_code != 500
    assert response.status_code == 200
    assert b"Welcome to the GUDLFT Registration Portal!" in response.data
    assert b"There is no account using this email" in response.data


def test_showSummary_template_render(client,competitions_with_availability,monkeypatch):
    """
    Given: A user access show summary
    When: he input a known email
    Then: the welcome template is rendered
    """
    monkeypatch.setattr('server.competitions', competitions_with_availability)
    email = "john@simplylift.co"
    response = client.post('/showSummary',data={"email": email})
    assert b"Welcome, john@simplylift.co" in response.data
import pytest
from tests.conftest import client

def test_showSummary_known_email_response_code(client):
    email = "john@simplylift.co"
    response = client.post('/showSummary',data={"email": email})
    assert response.status_code == 200

def test_showSummary_unknown_email(client):
    email = "johndoe@simplylift.co"
    response = client.post('/showSummary',data={"email": email})
    assert response.status_code == 404


def test_showSummary_template_render(client):
    email = "john@simplylift.co"
    response = client.post('/showSummary',data={"email": email})
    assert b"Welcome, john@simplylift.co" in response.data
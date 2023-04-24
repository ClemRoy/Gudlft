import pytest
from tests.conftest import client,clubs

def test_index(client):
    """
    Given: A user access the site
    When: he access the index url
    Then: we receive a status code 200 
    """
    response = client.get('/')
    assert response.status_code == 200

def test_board_display(client,clubs,monkeypatch):
    """
    Given: A user access the site
    When: he access the index url
    Then: a list of clubs and their points is displayed
    """
    monkeypatch.setattr('server.clubs', clubs)
    response = client.get('/')
    for club in clubs:
        expected_text = f"Club: {club['name']} </br>\n            Number of points: {club['points']}"
        assert expected_text.encode('utf-8') in response.data

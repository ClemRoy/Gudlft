import pytest
from server import app, loadClubs, loadCompetitions, showSummary, book, purchasePlaces
from tests.conftest import client


def test_full_integration(client, monkeypatch):
    """
    Given: Want to book places
    When: he follow procedures
    Then: the places are correctly booked"""
    competitions = loadCompetitions()
    clubs = loadClubs()
    # test the correct extraction of data
    assert len(clubs) == 3
    assert len(competitions) == 4
    # test the correct display of points on the index
    response = client.get('/')
    for club in clubs:
        expected_text = f"Club: {club['name']} </br>\n            Number of points: {club['points']}"
        assert expected_text.encode('utf-8') in response.data

    monkeypatch.setattr('server.competitions', competitions)
    monkeypatch.setattr('server.clubs', clubs)
    email = "john@simplylift.co"
    response = client.post('/showSummary', data={"email": email})

    # testing if the user is properly identified
    assert b"Welcome, john@simplylift.co" in response.data
    # testing if the data has been correctly updated during showsummary
    assert competitions[0]["available"] == False
    response = client.get("book/Future%20comp/Simply%20Lift")
    # testing if the user is correctly redircted
    assert b"""<form action="/purchasePlaces" method="post">""" in response.data
    assert b"""<input type="hidden" name="club" value="Simply Lift">""" in response.data
    assert b"""<input type="hidden" name="competition" value="Future comp">""" in response.data
    response = client.post(
        '/purchasePlaces', data={
            "competition": competitions[2]['name'],
            "club": clubs[0]['name'],
            "places": 5})
    # testing if the booking was successful
    assert competitions[2]['numberOfPlaces'] == 15
    assert b"Great-booking complete!" in response.data
    assert b'Points available: 8' in response.data
    # testing you're redirected to the index "/" when you logout
    response = client.get('/logout')
    assert b'You should be redirected automatically' in response.data
import pytest
from server import purchasePlaces
from tests.conftest import client, club, competition



def test_purchasePlaces_valid_points_number(client, club, competition, monkeypatch):

    monkeypatch.setattr('server.competitions', competition)
    monkeypatch.setattr('server.clubs', club)

    response = client.post(
        '/purchasePlaces', data={
            "competition": competition[0]['name'],
            "club": club[0]['name'],
            "places": 5})
    
    assert response.status_code == 200
    assert b'Number of Places: 20' in response.data
    assert b"Great-booking complete!" in response.data
    assert b'Points available: 8' in response.data
    assert competition[0]['numberOfPlaces'] == 20
    assert club[0]['points'] == 8


def test_purchasePlaces_too_many_points(client, club, competition, monkeypatch):

    monkeypatch.setattr('server.competitions', competition)
    monkeypatch.setattr('server.clubs', club)

    response = client.post(
        '/purchasePlaces', data={
            "competition": competition[0]['name'],
            "club": club[0]['name'],
            "places": 20})
    print( club[0]['points'])
    assert response.status_code == 200
    assert b'Error: Inssufficient points' in response.data
    assert int(competition[0]['numberOfPlaces']) == 25
    assert int(club[0]['points']) == 13
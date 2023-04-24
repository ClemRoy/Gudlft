import pytest
from server import purchasePlaces
from tests.conftest import client, clubs, competitions


def test_purchasePlaces_valid_points_number_render(client, clubs, competitions, monkeypatch):
    """
    Given: A user try to retrieve 5 places for a competition
    When: he book 5 places
    Then: we receive a 200 status code,a confirmation message is
    displayed"""
    monkeypatch.setattr('server.competitions', competitions)
    monkeypatch.setattr('server.clubs', clubs)

    response = client.post(
        '/purchasePlaces', data={
            "competition": competitions[0]['name'],
            "club": clubs[0]['name'],
            "places": 5})

    assert response.status_code == 200
    assert b'Number of Places: 20' in response.data
    assert b"Great-booking complete!" in response.data
    assert b'Points available: 8' in response.data


def test_purchasePlaces_valid_points_number_deduction(client, clubs, competitions, monkeypatch):
    """
    Given: A user try to retrieve 5 places for a competition
    When: he book 5 places
    Then: the number of places available for the competition
    decrease from 25 to 20 and the number of point available from 13 to 8"""
    monkeypatch.setattr('server.competitions', competitions)
    monkeypatch.setattr('server.clubs', clubs)

    response = client.post(
        '/purchasePlaces', data={
            "competition": competitions[0]['name'],
            "club": clubs[0]['name'],
            "places": 5})


    assert competitions[0]['numberOfPlaces'] == 20
    assert clubs[0]['points'] == 8

def test_purchasePlaces_negative_input(client, clubs, competitions, monkeypatch):
    """
    Given: A user try to retrieve -15 places for a competition
    When: he book -15 places
    Then: the user receive a message error and the values 
    of numberofplace and points don't change"""
    monkeypatch.setattr('server.competitions', competitions)
    monkeypatch.setattr('server.clubs', clubs)

    response = client.post(
        '/purchasePlaces', data={
            "competition": competitions[0]['name'],
            "club": clubs[0]['name'],
            "places": -15})

    assert b'Error: You cannot redeem a negative number of places' in response.data
    assert int(competitions[0]['numberOfPlaces']) == 25
    assert int(clubs[0]['points']) == 13


def test_purchasePlaces_customer_use_too_many_points(client, clubs, competitions, monkeypatch):
    """
    Given: A user try to retrieve 8 places for a competition while he only has 4 points
    When: he book 8 places
    Then: we receive a 200 status code,an error message is
    displayed and the amount of places and points are not modified
    """
    monkeypatch.setattr('server.competitions', competitions)
    monkeypatch.setattr('server.clubs', clubs)

    response = client.post(
        '/purchasePlaces', data={
            "competition": competitions[0]['name'],
            "club": clubs[1]['name'],
            "places": 8})
    assert response.status_code == 200
    assert b'Error: Inssufficient points' in response.data
    assert int(competitions[0]['numberOfPlaces']) == 25
    assert int(clubs[1]['points']) == 4


def test_purchasePlaces_customer_book_too_many_places(client, clubs, competitions, monkeypatch):
    """
    Given: A user try to retrieve 13 places for a competition while he only has 4 points
    When: he book 8 places
    Then: we receive a 200 status code,an error message is
    displayed and the amount of places and points are not modified
    """
    monkeypatch.setattr('server.competitions', competitions)
    monkeypatch.setattr('server.clubs', clubs)

    response = client.post(
        '/purchasePlaces', data={
            "competition": competitions[0]['name'],
            "club": clubs[0]['name'],
            "places": 13})
    assert response.status_code == 200
    assert b'Error: You cannot redeem more than 12 places' in response.data
    assert int(competitions[0]['numberOfPlaces']) == 25
    assert int(clubs[0]['points']) == 13

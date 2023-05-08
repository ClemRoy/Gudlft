import pytest
from server import app,showSummary, book
from tests.conftest import client, clubs, competitions, competitions_with_availability


def test_book_competition_without_availability(client, clubs, competitions, monkeypatch):
    """
    Given: a user try to access a competition 
    When: he directly enter the url without going through showsummary
    Then: he should be redirected to the index with an error message
    """
    monkeypatch.setattr('server.competitions', competitions)
    monkeypatch.setattr('server.clubs', clubs)
    response = client.get("book/Future%20comp/Simply%20Lift")
    assert response.status_code != 500
    assert b"Please follow the links and do not attempt to directly enter an url" in response.data


def test_book_valid_competition(client, clubs, competitions_with_availability, monkeypatch):
    """
    Given: A user access the booking feature for a competition
    When: a competition is in the future
    Then: he should be redirected to the correct booking template
    """
    monkeypatch.setattr('server.competitions', competitions_with_availability)
    monkeypatch.setattr('server.clubs', clubs)
    response = client.get("book/Future%20comp/Simply%20Lift")
    assert b"""<h2>Future comp</h2>""" in response.data
    assert b"""<form action="/purchasePlaces" method="post">""" in response.data
    assert b"""<input type="hidden" name="club" value="Simply Lift">""" in response.data
    assert b"""<input type="hidden" name="competition" value="Future comp">""" in response.data



def test_book_invalid_competition(client, clubs, competitions_with_availability, monkeypatch):
    """
    Given: A user access the booking feature for a competition
    When: a competition is in the future
    Then: he should be redirected to the correct booking template 
    """
    monkeypatch.setattr('server.competitions', competitions_with_availability)
    monkeypatch.setattr('server.clubs', clubs)
    response = client.get("book/Spring%20Festival/Simply%20Lift")
    assert b"You were redirected here because you tried to book place for a competition that already happened" in response.data

def test_book_unknown_club(client, clubs, competitions_with_availability, monkeypatch):
    """
    Given: a user try to access a competition with an unknown club in the url
    When: he directly enter the wrong club name in the url
    Then: he should be redirected to the index with an error message
    """
    monkeypatch.setattr('server.competitions', competitions_with_availability)
    monkeypatch.setattr('server.clubs', clubs)
    response = client.get("book/Future%20comp/SimplXXXX")
    assert b"Please follow the links and do not attempt to directly enter an url" in response.data

def test_book_unknown_competition(client, clubs, competitions_with_availability, monkeypatch):
    """
    Given: a user try to access a competition with an unknown competition in the url
    When: he directly enter the wrong club name in the url
    Then: he should be redirected to the index with an error message
    """
    monkeypatch.setattr('server.competitions', competitions_with_availability)
    monkeypatch.setattr('server.clubs', clubs)
    response = client.get("book/SpAAAAAival/Simply%20Lift")
    assert b"Please follow the links and do not attempt to directly enter an url" in response.data
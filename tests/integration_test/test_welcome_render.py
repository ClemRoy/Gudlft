import pytest
from server import app,showSummary, book
from tests.conftest import client, clubs, competitions, competitions_with_availability, competitions_with_availability_for_update_test

def test_welcome_interface_proper_rendering(client,clubs, competitions,competitions_with_availability, monkeypatch):
    """
    Given: A user access show summary
    When: the user input a correct email
    Then:The check availability function is
    called and the welcome page is rendered accordingly
    to the availability 
    """
    monkeypatch.setattr('server.competitions', competitions)
    monkeypatch.setattr('server.clubs', clubs)
    email = "john@simplylift.co"
    response = client.post('/showSummary', data={"email": email})
    unexpected_text = b'''<a href="/book/Spring%20Festival/Simply%20Lift"'''
    expected_text_1 = b"""Spring Festival<br />
            Date: 2020-03-27 10:00:00</br>
            Number of Places: 25
            
            <p>You cannot book place for past competition</p>"""
    
    expected_text_2 = b"""Future comp<br />
            Date: 2026-10-22 13:30:00</br>
            Number of Places: 20
            
                
                <a href="/book/Future%20comp/Simply%20Lift">Book Places</a>"""

    expected_text_3 = b"""Future comp2<br />
            Date: 2026-10-22 13:30:00</br>
            Number of Places: 0
            
                
                <p>There is no more place available</p>"""
    
    for comp in range(0,len(competitions)):
        assert competitions[comp] == competitions_with_availability[comp]

    assert expected_text_1 in response.data
    assert expected_text_2 in response.data
    assert expected_text_3 in response.data
    assert unexpected_text not in response.data

def test_welcome_proper_update_ater_booking(client,clubs,competitions_with_availability_for_update_test,monkeypatch):
    """
    Given: A user try to retrieve the last 6 places for a competition
    When: he proceed with the booking
    Then: the number of places available for the competition
    decrease from 6 to 0 and the competition is no longer displayed as available in the welcome render"""
    monkeypatch.setattr('server.competitions', competitions_with_availability_for_update_test)
    monkeypatch.setattr('server.clubs', clubs)

    response = client.post(
        '/purchasePlaces', data={
            "competition": competitions_with_availability_for_update_test[3]['name'],
            "club": clubs[0]['name'],
            "places": 6})

    expected_test_1 = b"Great-booking complete!"
    expected_text_2 = b"""Future comp2<br />
            Date: 2026-10-22 13:30:00</br>
            Number of Places: 0
            
                
                <p>There is no more place available</p>"""  
      
    assert competitions_with_availability_for_update_test[3]['numberOfPlaces'] == 0
    assert clubs[0]['points'] == 7
    assert expected_test_1 in response.data
    assert expected_text_2
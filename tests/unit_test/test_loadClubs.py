import pytest
from server import loadClubs

def test_loadClubs():
    """
    Given:the app is launched
    When: the clubs data is extracted from the Json file
    Then: the clubs are properly extracted"""
    extracted_clubs = loadClubs()
    assert len(extracted_clubs) == 3
    assert extracted_clubs[0]['name'] == "Simply Lift"
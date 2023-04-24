import pytest
from server import loadClubs
from tests.conftest import clubs

def test_loadClubs(clubs):
    """
    Given:the app is launched
    When: the clubs data is extracted from the Json file
    Then: the clubs are properly extracted"""
    extracted_clubs = loadClubs()
    for x in range(0,len(extracted_clubs)):
        assert extracted_clubs[x] == clubs[x]
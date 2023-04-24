import pytest
from server import loadCompetitions
from tests.conftest import competitions

def test_loadCompetitions(competitions):
    """
    Given:the app is launched
    When: the competition data is extracted from the Json file
    Then: the competitions are properly extracted"""
    extracted_competition = loadCompetitions()
    for x in range(0,len(extracted_competition)):
        assert extracted_competition[x] == competitions[x]
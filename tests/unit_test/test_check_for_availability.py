import pytest
from server import check_for_availability
from tests.conftest import competitions,competitions_with_availability

def test_check_for_availability(competitions,competitions_with_availability):
    """
    Given:the showSummary function is called
    When: competitions are checked for availability
    Then: the key is added to their dictionnary"""
    for x in range(0,len(competitions)):
        comp_with_avail = check_for_availability(competitions[x])
        assert comp_with_avail == competitions_with_availability[x]
import pytest
from server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def clubs():
    return [
        {
            "name": "Simply Lift",
            "email": "john@simplylift.co",
            "points": "13"
        },
        {
            "name": "Iron Temple",
            "email": "admin@irontemple.com",
            "points": "4"
        },
        {"name": "She Lifts",
         "email": "kate@shelifts.co.uk",
         "points": "12"
         }
    ]


@pytest.fixture
def competitions():
    return [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        },
        {
            "name": "Future comp",
            "date": "2026-10-22 13:30:00",
            "numberOfPlaces": "20"
        },
        {
            "name": "Future comp2",
            "date": "2026-10-22 13:30:00",
            "numberOfPlaces": "0"
        }
    ]


@pytest.fixture
def competitions_with_availability():
    return [
        {
            "name": "Spring Festival",
            "date": "2020-03-27 10:00:00",
            "numberOfPlaces": "25",
            "available": False
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13",
            "available": False
        },
        {
            "name": "Future comp",
            "date": "2026-10-22 13:30:00",
            "numberOfPlaces": "20",
            "available": True
        },
        {
            "name": "Future comp2",
            "date": "2026-10-22 13:30:00",
            "numberOfPlaces": "0",
            "available": True
        }
    ]

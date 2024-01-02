import pytest
from unittest.mock import patch
from change_details import change_details

## Fixtures for change_details
@pytest.fixture
def test_entry():
    return {
        "username": "test",
        "password": "test",
        "address": "Dag Hammarskälds Väg",
        "phone": "07099999999",
        "email": "test@gmail.com",
        "credit": {
            "number": "0365027409470925",
            "expiry": "11/25",
            "cvv": "999",
        },
    }


## Tests for change_details
def test_change_details_input_not_Y(test_entry):
    with patch("builtins.input", side_effect=["N"]):
        assert change_details(test_entry) == None

def test_change_details_address(test_entry):
    with patch("builtins.input", side_effect=["Y", "a", "Raketvägen"]):
        assert change_details(test_entry) == {
            "username": "test",
            "password": "test",
            "address": "Raketvägen",
            "phone": "07099999999",
            "email": "test@gmail.com",
            "credit": {
                "number": "0365027409470925",
                "expiry": "11/25",
                "cvv": "999",
            },
        }

def test_change_details_credit_card(test_entry):
    with patch("builtins.input", side_effect=["Y", "c", "9999999999999999", "99/99", "999"]):
        assert change_details(test_entry) == {
            "username": "test",
            "password": "test",
            "address": "Dag Hammarskälds Väg",
            "phone": "07099999999",
            "email": "test@gmail.com",
            "credit": {
                "number": "9999999999999999",
                "expiry": "99/99",
                "cvv": "999",
            },
        }


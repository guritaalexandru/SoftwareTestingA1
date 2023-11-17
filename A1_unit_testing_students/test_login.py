# write some tests with pytest for the login function in login.py
from unittest.mock import patch

import pytest
from login import login, check_password


def test_login_existing_user_correct_password():
    inputs = ["Ramanathan", "Notaproblem23*"]
    with patch('builtins.input', side_effect=inputs):
        assert login() == {"username": "Ramanathan", "wallet": 100}


def test_login_existing_user_incorrect_password():
    inputs = ["Ramanathan", "Notaproblem23*!"]
    with patch('builtins.input', side_effect=inputs):
        assert login() == None


# Test for password validation
def test_check_password():
    assert check_password("Password1!") == True
    assert check_password("noSpecialChar1") == False
    assert check_password("No1!") == False

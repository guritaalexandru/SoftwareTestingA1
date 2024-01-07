# write some tests with pytest for the login function in login.py
from unittest.mock import patch

import pytest
from login import login, check_password

valid_test_inputs = ["Ramanathan", "Notaproblem23*"]
invalid_test_inputs = ["Ramanathan", "Notaproblem23*!"]

new_user_N_inputs = ["NewUser", "", "N"]
new_user_X_inputs = ["NewUser", "", "X"]

new_user_valid_password = ["NewUser", "", "Y", "ValidPassword1!"]
new_user_invalid_password = ["NewUser", "", "Y", "invalidpassword"]


@pytest.fixture(scope="function")
def write_to_file_stub(mocker):
    return mocker.patch('login.write_to_file', return_value=None)


@pytest.fixture(scope="function")
def check_password_stub_incorrect(mocker):
    return mocker.patch('login.check_password', return_value=False)


@pytest.fixture(scope="function")
def check_password_stub_correct(mocker):
    return mocker.patch('login.check_password', return_value=True)


def test_login_existing_user_correct_password():
    with patch('builtins.input', side_effect=valid_test_inputs):
        assert login() == {"username": valid_test_inputs[0], "wallet": 100}


def test_login_existing_user_incorrect_password():
    with patch('builtins.input', side_effect=invalid_test_inputs):
        assert login() is None


def test_login_new_user_no_register():
    with patch('builtins.input', side_effect=new_user_N_inputs):
        assert login() is None


def test_login_new_user_X_register():
    with patch('builtins.input', side_effect=new_user_X_inputs):
        assert login() is None


def test_login_new_user_register_valid_password(write_to_file_stub, check_password_stub_correct):
    with patch('builtins.input', side_effect=new_user_valid_password):
        assert login() == {"username": new_user_valid_password[0], "wallet": 100}
        write_to_file_stub.assert_called_once()
        check_password_stub_correct.assert_called_once_with(new_user_valid_password[3])


def test_login_new_user_register_invalid_password(check_password_stub_incorrect):
    with patch('builtins.input', side_effect=new_user_invalid_password):
        assert login() is None
        check_password_stub_incorrect.assert_called_once_with(new_user_invalid_password[3])


def test_check_password_no_capital():
    assert check_password("password1!") is False


def test_check_password_no_numeral():
    assert check_password("Password!") is False


def test_check_password_too_short():
    assert check_password("Pass1!") is False


def test_check_password_no_special_char():
    assert check_password("Password1") is False


def test_check_password_valid():
    assert check_password("Password1!") is True

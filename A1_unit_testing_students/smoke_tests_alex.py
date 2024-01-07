from unittest.mock import patch

import pytest
from login import login, check_password
from checkout_and_payment import checkoutAndPayment


@pytest.fixture
def mock_input(mocker):
    return mocker.patch('builtins.input')


@pytest.fixture
def mock_logout(mocker):
    return mocker.patch('checkout_and_payment.logout', return_value=True)


# Prevent the test from writing to the users.json file from login
@pytest.fixture(scope="function")
def write_to_file_stub(mocker):
    return mocker.patch('login.write_to_file', return_value=None)


# Prevents the test from writing to the users.json file from checkout_and_payment
@pytest.fixture(scope="function")
def write_to_file_checkout_stub(mocker):
    return mocker.patch('checkout_and_payment.update_users_json', return_value=None)


# Tests the successful checkout process after a valid login
def test_login_checkout(mock_input, mock_logout, write_to_file_checkout_stub, capsys):
    mock_input.side_effect = ["Ramanathan", "Notaproblem23*", '1', 'c', 'N', 'y', 'l']
    login_output = login()

    assert checkoutAndPayment(login_output) is None

    captured = capsys.readouterr()
    assert captured.out.count("Thank you for your purchase") == 1
    assert mock_logout.call_count == 1


#Tests the checkout process with a failed login attempt.
def test_failed_login_checkout(mock_input, mock_logout, capsys):
    mock_input.side_effect = ["Ramanathan", "Notaproblem23*!!!"]
    login_output = login()

    # Expect error
    assert login_output is None
    # Expect type error
    with pytest.raises(TypeError):
        checkoutAndPayment(login_output)


# Tests the checkout process for a newly registered user.
def test_register_checkout(write_to_file_stub, write_to_file_checkout_stub, mock_input, mock_logout, capsys):
    mock_input.side_effect = ["NewUser", "", "Y", "ValidPassword1!", '1', 'c', 'N', 'y', 'l']
    assert login() == {"username": "NewUser", "wallet": 100}

    login_output = {"username": "NewUser", "wallet": 100}
    assert checkoutAndPayment(login_output) is None

    captured = capsys.readouterr()
    assert captured.out.count("Thank you for your purchase") == 1
    assert mock_logout.call_count == 1


# Tests the registration process with invalid credentials.
def test_failed_register_checkout(mock_input, capsys):
    mock_input.side_effect = ["NewUser", "", "Y", "invalidpassword"]
    assert login() is None

    login_output = None
    captured = capsys.readouterr()
    assert captured.out.count("Password should have at least one capital letter") == 1

    # Expect type error
    with pytest.raises(TypeError):
        checkoutAndPayment(login_output)


# Tests the checkout process with an invalid product selection
def test_checkout_invalid_product_selection(mock_input, mock_logout, capsys):
    mock_input.side_effect = ["Ramanathan", "Notaproblem23*", '999', 'c', 'N', 'y', 'l']
    login_output = login()

    checkoutAndPayment(login_output)

    captured = capsys.readouterr()
    assert captured.out.count("Invalid input. Please try again.") == 1


# Tests the checkout process with multiple invalid product selections
def test_checkout_multiple_invalid_product_selection(mock_input, mock_logout, capsys):
    mock_input.side_effect = ["Ramanathan", "Notaproblem23*", '999', '998', '997', 'c', 'N', 'y', 'l']
    login_output = login()

    checkoutAndPayment(login_output)

    captured = capsys.readouterr()
    assert captured.out.count("Invalid input. Please try again.") == 3


# Tests the checkout process with a valid product selection
def test_checkout_with_multiple_items(mock_input, mock_logout, write_to_file_checkout_stub, capsys):
    mock_input.side_effect = ["Ramanathan", "Notaproblem23*", '1', '2', '2', '3', 'c', 'N', 'y', 'l']
    login_output = login()

    assert checkoutAndPayment(login_output) is None

    captured = capsys.readouterr()
    assert captured.out.count("Thank you for your purchase") == 1
    assert captured.out.count("added to your cart") == 4
    assert mock_logout.call_count == 1


# Tests the checkout process with multiple valid product selections and one invadid product selection
def test_checkout_mixed_invalid_product_selection(mock_input, mock_logout, write_to_file_checkout_stub, capsys):
    mock_input.side_effect = ["Ramanathan", "Notaproblem23*", '999', '1', '2', '2', 'c', 'N', 'y', 'l']
    login_output = login()

    assert checkoutAndPayment(login_output) is None

    captured = capsys.readouterr()
    assert captured.out.count("Invalid input. Please try again.") == 1
    assert captured.out.count("Thank you for your purchase") == 1
    assert captured.out.count("added to your cart") == 3


# Tests the checkout process with multiple valid product selections and multiple invadid product selections
def test_checkout_multiple_mixed_invalid_product_selection(mock_input, mock_logout, write_to_file_checkout_stub, capsys):
    mock_input.side_effect = ["Ramanathan", "Notaproblem23*", '999', '998', '1', '2', '2', 'c', 'N', 'y', 'l']
    login_output = login()

    assert checkoutAndPayment(login_output) is None

    captured = capsys.readouterr()
    assert captured.out.count("Invalid input. Please try again.") == 2
    assert captured.out.count("Thank you for your purchase") == 1
    assert captured.out.count("added to your cart") == 3


# Tests the checkout process when the balance is insufficient
def test_checkout_no_money(mock_input, mock_logout, write_to_file_checkout_stub, capsys):
    mock_input.side_effect = ["Ramanathan", "Notaproblem23*", '52', 'c', 'N', 'y', 'l']
    login_output = login()

    assert checkoutAndPayment(login_output) is None

    captured = capsys.readouterr()
    assert captured.out.count("You don't have enough money to complete the purchase.") == 1

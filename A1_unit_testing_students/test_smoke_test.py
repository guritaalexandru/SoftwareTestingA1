from io import StringIO
import json
import pytest
from unittest.mock import mock_open, patch
from checkout_and_payment import ShoppingCart, User, checkoutAndPayment, load_products_from_csv

from login import check_password, login

valid_json_users = """[
  {"username": "Ramanathan", "password": "Notaproblem23*", "wallet": 100, "cards": [{"name": "Card1", "balance": 1000}]}]"""

products= load_products_from_csv("products.csv")

@pytest.fixture
def filled_cart():
    cart = ShoppingCart()
    cart.add_item(products[0])
    cart.add_item(products[1])
    cart.add_item(products[2])
    cart.add_item(products[3])
    cart.add_item(products[4])
    cart.add_item(products[5])
    return cart

@pytest.fixture
def mock_open_users(mocker):
    json_file = StringIO(valid_json_users)
    return mocker.patch('checkout_and_payment.open', side_effect=mock_open(read_data=json_file.getvalue()))

@pytest.fixture
def mock_check_cart(mocker):
    """Fixture to mock cart checking functionality."""
    return mocker.patch('checkout_and_payment.check_cart', return_value=True)

@pytest.fixture
def mock_logout(mocker):
    """Fixture to mock logout functionality."""
    return mocker.patch('checkout_and_payment.logout', return_value=True)

@pytest.fixture
def user_1():
    return User("Test", 10, [{"name": "Card1", "balance": 1000}])

def test_smoke_check_password_valid():
    assert check_password("ValidPassword1!")

def test_smoke_check_password_no_capital():
    assert not check_password("password1!")

def test_smoke_check_password_no_numeral():
    assert not check_password("Password!")

def test_smoke_check_password_too_short():
    assert not check_password("Pass1!")

def test_smoke_check_password_no_special_char():
    assert not check_password("Password1")

def test_smoke_login_existing_user_correct_password(mock_open_users):
    with patch('builtins.input', side_effect=["Ramanathan", "Notaproblem23*"]):
        assert login() == {"username": "Ramanathan", "wallet": 100.0, "cards": [{"name": "Card1", "balance": 991.5}]}

def test_smoke_login_existing_user_incorrect_password(mock_open_users):
    with patch('builtins.input', side_effect=["Ramanathan", "IncorrectPassword"]):
        assert login() is None

def test_smoke_checkout_and_payment_with_items(mock_check_cart, mock_open_users):
    login_info = {"username": "Test", "password": "Notaproblem23*", "wallet": 10, "cards": [{"name": "Card1", "balance": 1000}]}
    with patch('builtins.input', side_effect=["1", "c", "y", "w", "l", "y"]):
        assert checkoutAndPayment(login_info) is None
        mock_check_cart.assert_called_once()

def test_smoke_checkout_and_payment_without_items(mock_open_users):
    login_info = {"username": "Ramanathan", "password": "Notaproblem23*", "wallet": 100.0, "cards": [{"name": "Card1", "balance": 991.5}]}
    with patch('builtins.input', side_effect=["l"]):
        assert checkoutAndPayment(login_info) is None

def test_smoke_checkout_and_payment_invalid_choice(mock_open_users):
    login_info = {"username": "Ramanathan", "password": "Notaproblem23*", "wallet": 100.0, "cards": [{"name": "Card1", "balance": 991.5}]}
    with patch('builtins.input', side_effect=["InvalidChoice", "l"]):
        assert checkoutAndPayment(login_info) is None
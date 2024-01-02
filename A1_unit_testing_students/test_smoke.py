import io
import pytest
from checkout_and_payment import Product, User, ShoppingCart, checkout, check_cart, products as productz, load_products_from_csv 
from unittest.mock import patch, mock_open, MagicMock
from logout import logout
from login import login, check_password
import csv
from products import display_csv_as_table, display_filtered_table, searchAndBuyProduct
import json
from checkout_and_payment import checkoutAndPayment, update_users_json

## Fixtures for the smoke tests
@pytest.fixture
def test_user_file():
    return {
        "username": "test",
        "password": "1234Test%",
        "address": "Dag Hammarskälds Väg",
        "phone": "07099999999",
        "email": "test@gmail.com",
        "credit": {
            "number": "0365027409470925",
            "expiry": "11/25",
            "cvv": "999",
        },
    }

@pytest.fixture
def test_user(test_user_file):
    user = User(test_user_file["username"], 0)
    return user

@pytest.fixture
def test_user_has_money(test_user_file):
    user = User(test_user_file["username"], 1000)
    return user

@pytest.fixture
def cart():
    cart = ShoppingCart()
    return cart

## 10 smoke tests for the whole system

# 1. Test user creation
def test_create_user():
    with patch("builtins.input", side_effect=["test", "1234Test%", "Y", "1234Test%", "Dag Hammarskälds Väg", "07099999999", "test@gmail.com", "0365027409470925", "11/25", "999"]):
        assert login() == {"username": "test", "wallet" : 0}

# 2. Test user login
def test_login():
    with patch("builtins.input", side_effect=["test", "1234Test%", "N"]):
        assert login() == {"username": "test", "wallet" : 0}

# 3. Test user login, create a cart log out
def test_login_create_cart_logout(test_user_file, cart):
    user = test_user_file
    with patch("builtins.input", side_effect=[user["username"], user["password"], "N"]):
        assert login() == {"username": "test", "wallet" : 0}
        assert cart.retrieve_item() == []

# 4. Test user login, create a cart and add an item to it
def test_login_create_cart_item(test_user_file, cart):
    user = test_user_file
    with patch("builtins.input", side_effect=[user["username"], user["password"], "N"]):
        assert login() == {"username": "test", "wallet" : 0}

        cart.add_item(productz[0])
        assert len(cart.retrieve_item()) == 1

# 5. Test user login, create a cart with an item and check that it is the right item.
def test_cart_item_check(test_user_file, cart):
    user = test_user_file
    with patch("builtins.input", side_effect=[user["username"], user["password"], "N"]):
        assert login() == {"username": "test", "wallet" : 0}

        cart.add_item(productz[0])
        assert cart.retrieve_item()[0].get_product() == productz[0].get_product()

# 6. Test to check that user cannot login with empty wallet, create a cart and buy an item.
def test_cart_item_check_no_money(test_user, test_user_file, cart):
    user = test_user
    user_file = test_user_file
    with patch("builtins.input", side_effect=[user_file["username"], user_file["password"], "N"]):
        assert login() == {"username": "test", "wallet" : 0}

        s_cart = cart
        s_cart.add_item(productz[0])
        assert len(s_cart.retrieve_item()) == 1
        assert s_cart.retrieve_item()[0].get_product() == productz[0].get_product()

        assert checkout(user, s_cart) == False

# 7. Test for user so that they can login with enough in wallet, create a cart and buy an item.
def test_cart_item_check_with_money(test_user_has_money, test_user_file, cart):
    user = test_user_has_money
    user_file = test_user_file
    with patch("builtins.input", side_effect=[user_file["username"], user_file["password"], "N"]):
        assert login() == {"username": "test", "wallet" : 0}

        s_cart = cart
        s_cart.add_item(productz[0])
        assert len(s_cart.retrieve_item()) == 1
        assert s_cart.retrieve_item()[0].get_product() == productz[0].get_product()

        assert checkout(user, s_cart) == True

# 8. Test for incorrect password, assert that the login function returns false and that the standard out gets captured and has the correct output.
def test_incorrect_password(test_user_file):
    user = test_user_file
    with patch('sys.stdout', new_callable=io.StringIO) as mocked_stdout:
        with patch("builtins.input", side_effect=[user["username"], "something", "N"]):
            assert login() == None
            assert mocked_stdout.getvalue() == ("Either username or password were incorrect\n")

# 9. Test for incorrect username, assert that the login function tries to make a new user and that the standard out gets captured and has the correct output.
def test_incorrect_username(test_user_file):
    user = test_user_file
    with patch('sys.stdout', new_callable=io.StringIO) as mocked_stdout:
        with patch("builtins.input", side_effect=["something", user["password"], "N"]):
            assert login() == None
            assert mocked_stdout.getvalue() == ("User does not exist. Would you like to register?\n")

# 10. Test for incorrect username and password, assert that the login function tries to make a new user and that the standard out gets captured and has the correct output.
def test_incorrect_username_and_password(test_user_file):
    user = test_user_file
    with patch('sys.stdout', new_callable=io.StringIO) as mocked_stdout:
        with patch("builtins.input", side_effect=["something", "something", "N"]):
            assert login() == None
            assert mocked_stdout.getvalue() == ("User does not exist. Would you like to register?\n")






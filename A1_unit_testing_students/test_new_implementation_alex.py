import io
import pytest
from checkout_and_payment import Product, User, ShoppingCart, checkout, check_cart
from unittest.mock import patch


@pytest.fixture
def user_1():
    return User("", 0.0)


@pytest.fixture
def cart_1(products):
    cart = ShoppingCart()
    cart.items = products
    return cart


@pytest.fixture
def products(csv_units, csv_name, csv_price):
    products = []
    for i in range(0, 7):
        products.append(Product(csv_name[i], csv_units[i], csv_price[i]))
    return products


@pytest.fixture
def csv_price():
    data = [
        10,
        15,
        8,
        5,
        12,
        1,
        2,
    ]
    return data


@pytest.fixture
def csv_units():
    data = [
        2,
        1,
        1.5,
        3,
        4,
        10,
        0.5,
    ]
    return data


@pytest.fixture
def csv_name():
    data = [
        "Apple",
        "Banana",
        "Orange",
        "Grapes",
        "Strawberry",
        "Watermelon",
        "Carrot",
    ]
    return data


def test_check_cart_input_no(user_1, cart_1):
    # Simulate input a negative input
    with patch('builtins.input', side_effect=['N', 'N']):
        # Assert that input is no
        assert (check_cart(user_1, cart_1) == False)


def test_check_cart_1(user_1, cart_1):
    with patch.object(cart_1, 'remove_item') as mock_remove_item, \
            patch('builtins.input', side_effect=['y', 'Apple', 'n', 'N']):
        result = check_cart(user_1, cart_1)

        # Assert that retrieve_item was called once
        mock_remove_item.assert_called_once()


def test_check_cart_2(user_1, cart_1):
    with patch.object(cart_1, 'remove_item') as mock_remove_item, \
            patch('builtins.input', side_effect=['y', 'Apple', 'Y', 'Banana', 'n', 'N']):
        result = check_cart(user_1, cart_1)

        # Assert that retrieve_item was called twice
        mock_remove_item.assert_called()

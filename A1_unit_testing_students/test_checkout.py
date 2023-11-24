import io
import pytest
from checkout_and_payment import (
    Product,
    User,
    ShoppingCart,
    checkout,
    check_cart,
    products,
)
from unittest.mock import patch


@pytest.fixture
def user_1():
    return User("Test", 10)


@pytest.fixture
def user_2():
    return User("Test_Rich", 2000)


@pytest.fixture
def user_3():
    return User("Test_Exakt", 1)


@pytest.fixture
def empty_cart():
    cart = ShoppingCart()
    cart.items = []
    return cart


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
def filled_cart_1_units():
    cart = ShoppingCart()
    cart.add_item(products[0])
    cart.add_item(products[1])
    cart.add_item(products[2])
    cart.add_item(products[3])
    cart.add_item(products[4])
    cart.add_item(products[5])
    for i in cart.retrieve_item():
        i.units = 1
    return cart


@pytest.fixture
def single_cart_1():
    cart = ShoppingCart()
    cart.add_item(products[0])
    return cart


@pytest.fixture
def single_cart_2():
    cart = ShoppingCart()
    cart.add_item(products[1])
    return cart


@pytest.fixture
def multi_cart():
    cart = ShoppingCart()
    cart.add_item(products[0])
    cart.add_item(products[1])
    cart.add_item(products[2])
    cart.add_item(products[4])
    return cart


def test_checkout_empty(user_1, empty_cart):
    with patch("sys.stdout", new_callable=io.StringIO) as mocked_stdout:
        checkout(user_1, empty_cart)
        assert (
            mocked_stdout.getvalue()
            == "\nYour basket is empty. Please add items before checking out.\n"
        )


def test_checkout_single(user_1, single_cart_1):
    with patch("sys.stdout", new_callable=io.StringIO) as mocked_stdout:
        checkout(user_1, single_cart_1)
        assert (
            mocked_stdout.getvalue()
            == "\n\nThank you for your purchase, Test! Your remaining balance is 8.0\n"
        )


def test_checkout_multiple(user_1, multi_cart):
    with patch("sys.stdout", new_callable=io.StringIO) as mocked_stdout:
        checkout(user_1, multi_cart)
        assert (
            mocked_stdout.getvalue()
            == "\n\nThank you for your purchase, Test! Your remaining balance is 1.5\n"
        )


def test_checkout_cart_clear(user_2, filled_cart):
    checkout(user_2, filled_cart)
    assert filled_cart.items == []


def test_checkout_insufficient_funds(user_1, filled_cart):
    with patch("sys.stdout", new_callable=io.StringIO) as mocked_stdout:
        checkout(user_1, filled_cart)
        assert (
            mocked_stdout.getvalue()
            == "\n\nYou don't have enough money to complete the purchase.\nPlease try again!\n"
        )


def test_checkout_sufficient_funds(user_2, filled_cart):
    with patch("sys.stdout", new_callable=io.StringIO) as mocked_stdout:
        checkout(user_2, filled_cart)
        assert (
            mocked_stdout.getvalue()
            == "\n\nThank you for your purchase, Test_Rich! Your remaining balance is 1988.0\n"
        )


def test_checkout_product_zero_units_single(user_1, single_cart_1):
    checkout(user_1, single_cart_1)
    for item in single_cart_1.items:
        assert item.units > 0


def test_checkout_product_zero_units_multi(user_1, multi_cart):
    checkout(user_1, multi_cart)
    for item in multi_cart.items:
        assert item.units > 0


def test_checkout_just_enough_money(user_3, single_cart_2):
    with patch("sys.stdout", new_callable=io.StringIO) as mocked_stdout:
        checkout(user_3, single_cart_2)
        assert (
            mocked_stdout.getvalue()
            == "\n\nThank you for your purchase, Test_Exakt! Your remaining balance is 0.0\n"
        )


def test_checkout_wallet_update(user_2, filled_cart):
    initial_wallet = user_2.wallet
    total_price = filled_cart.get_total_price()
    checkout(user_2, filled_cart)
    assert user_2.wallet == initial_wallet - total_price

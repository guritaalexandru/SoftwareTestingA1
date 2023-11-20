import pytest
from unittest.mock import patch, PropertyMock

from logout import logout


class Cart:
    def __init__(self):
        self.items = [1, 2, 3]

    def retrieve_item(self):
        pass

    def clear_items(self):
        pass


def test_logout_empty_cart():
    cart_instance = Cart()

    with patch.object(cart_instance, 'items') as mock_items:
        # Set the length of cart.items to simulate an empty cart
        mock_items.__len__.return_value = 0
        assert logout(cart_instance) is True


def test_logout_non_empty_cart_no_confirmation():
    cart_instance = Cart()

    with patch.object(cart_instance, 'retrieve_item') as mock_retrieve_item, \
            patch('builtins.input', side_effect=['N']):
        result = logout(cart_instance)

        # Assert that retrieve_item was called once
        mock_retrieve_item.assert_called_once()
        assert result is False


def test_logout_non_empty_cart_with_confirmation():
    cart_instance = Cart()

    with patch.object(cart_instance, 'retrieve_item') as mock_retrieve_item, \
            patch.object(cart_instance, 'clear_items') as mock_clear_items, \
            patch('builtins.input', side_effect=['Y']):
        result = logout(cart_instance)

        # Assert that retrieve_item was called once
        mock_retrieve_item.assert_called_once()
        mock_clear_items.assert_called_once()
        assert result is True


# test for int, float, string, list inputs

def test_logout_string_input():
    try:
        logout("not_a_cart_instance")
        assert False, "Expected an exception for incorrect input type"
    except AttributeError:
        # The function should raise a AttributeError for incorrect input type
        assert True  # The function raised the expected exception


def test_logout_int_input():
    try:
        logout(1)
        assert False, "Expected an exception for incorrect input type"
    except AttributeError:
        # The function should raise a AttributeError for incorrect input type
        assert True  # The function raised the expected exception


def test_logout_float_input():
    try:
        logout(1.0)
        assert False, "Expected an exception for incorrect input type"
    except AttributeError:
        # The function should raise a AttributeError for incorrect input type
        assert True  # The function raised the expected exception


def test_logout_list_input():
    try:
        logout([1, 2, 3])
        assert False, "Expected an exception for incorrect input type"
    except AttributeError:
        # The function should raise a AttributeError for incorrect input type
        assert True  # The function raised the expected exception


def test_logout_empty_input():
    try:
        logout()
        assert False, "Expected an exception for incorrect input type"
    except TypeError:
        # The function should raise a TypeError for incorrect input type
        assert True  # The function raised the expected exception

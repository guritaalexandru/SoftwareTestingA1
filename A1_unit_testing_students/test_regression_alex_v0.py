import pytest

from test_logout import test_logout_empty_cart, test_logout_non_empty_cart_no_confirmation, \
    test_logout_non_empty_cart_with_confirmation, test_logout_string_input, test_logout_int_input

from test_login import test_login_existing_user_correct_password, test_login_existing_user_incorrect_password, \
    test_login_new_user_no_register, test_login_new_user_X_register, test_login_new_user_register_valid_password, \
    write_to_file_stub, check_password_stub_correct

from test_check_cart import test_check_cart_input_no, test_check_cart_input_yes_wrong_case, \
    test_check_cart_input_ascii, test_check_cart_checkout_called, test_check_cart_checkout_returns_none, \
    user_1, cart_1, products_fixture, csv_units, csv_name, csv_price

from test_checkout import test_checkout_empty, test_checkout_single, test_checkout_multiple, test_checkout_cart_clear, \
    test_checkout_insufficient_funds, user_1 as checkout_user_1, empty_cart, single_cart_1, multi_cart, user_2, \
    filled_cart

def test_regression_login(write_to_file_stub, check_password_stub_correct):
    test_login_existing_user_correct_password()
    test_login_existing_user_incorrect_password()
    test_login_new_user_no_register()
    test_login_new_user_X_register()
    test_login_new_user_register_valid_password(write_to_file_stub, check_password_stub_correct)


def test_regression_logout():
    test_logout_empty_cart()
    test_logout_non_empty_cart_no_confirmation()
    test_logout_non_empty_cart_with_confirmation()
    test_logout_string_input()
    test_logout_int_input()


def test_regression_check_cart(user_1, cart_1, products_fixture, csv_units, csv_name, csv_price):
    test_check_cart_input_no(user_1, cart_1)
    test_check_cart_input_yes_wrong_case(user_1, cart_1)
    test_check_cart_input_ascii(user_1, cart_1)
    test_check_cart_checkout_called(user_1, cart_1)
    test_check_cart_checkout_returns_none(user_1, cart_1)


def test_regression_checkout(checkout_user_1, empty_cart, single_cart_1, multi_cart, user_2, filled_cart):
    test_checkout_empty(checkout_user_1, empty_cart)
    test_checkout_single(checkout_user_1, single_cart_1)
    # test_checkout_multiple(checkout_user_1, multi_cart)
    # test_checkout_cart_clear(user_2, filled_cart)
    test_checkout_insufficient_funds(checkout_user_1, filled_cart)

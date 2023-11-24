import io
import pytest
from checkout_and_payment import Product, User, ShoppingCart, checkout, check_cart
from unittest.mock import patch


@pytest.fixture
def cart_1(products):
    cart = ShoppingCart()
    cart.items = products
    return cart

@pytest.fixture
def cart_2():
    cart = ShoppingCart()
    cart.clear_items()
    return cart




@pytest.fixture
def user_1():
    return User("", 0.0)


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
    with patch('builtins.input', return_value='N'):
        # Assert that input is no
        assert(check_cart(user_1, cart_1) == False)

def test_check_cart_input_yes_wrong_case(user_1, cart_1):
    # Simulate a positive input, with an incorrect case to check that it still works
    with patch('builtins.input', return_value='Y'):
        # Assert that the input was yes
        assert(check_cart(user_1, cart_1) == False)

def test_check_cart_input_ascii(user_1, cart_1):
    # Test the function for all ascii inputs except for the one that are Yes
    for i in range(0, 256, 1) : 
        if chr(i) == 'y' or 'Y':
            continue

        with patch('builtins.input', return_value=chr(i)):
            # Assert that none passes as yes 
            assert(check_cart(user_1, cart_1) == False)

def test_check_cart_checkout_called(user_1, cart_1):
    # Test to ensure that the helper function checkout was called
    with patch('checkout_and_payment.checkout') as mocked:
        mocked.return_value = None

        with patch('builtins.input', return_value='Y'):
            check_cart(user_1, cart_1)
            
            # Assert that it was called once
            mocked.assert_called_once()

def test_check_cart_checkout_returns_boolean(user_1, cart_1):
    # Test that the boolean returned from checkout is returned from check_cart
    with patch('checkout_and_payment.checkout') as mocked:
        mocked.return_value = False

        with patch('builtins.input', return_value='Y'):
            result = check_cart(user_1, cart_1)
    
            mocked.assert_called_once()
            
            # Assert that the boolean is returned
            assert(result == False)

def test_check_cart_empty_cart(user_1, cart_2):
    # Test with an empty cart
    with patch('sys.stdout', new_callable=io.StringIO) as mocked_stdout:
    
        with patch('builtins.input', return_value='Y'):
            result = check_cart(user_1, cart_2)
        
            # Assert the return value 
            assert(result == False)

        # Assert that an empty cart has been identified
        assert mocked_stdout.getvalue() == "\nYour basket is empty. Please add items before checking out.\n"

def test_check_cart_insufficient_funds(user_1, cart_1):
    # Test the fucntion with not enough funds in the wallet
    user_1.wallet = 10

    with patch('sys.stdout', new_callable=io.StringIO) as mocked_stdout:
    
        with patch('builtins.input', return_value='Y'):
            result = check_cart(user_1, cart_1)
        
            # Assert the return value 
            assert(result == False)

        # Assert that insufficient funds have been identified
        assert mocked_stdout.getvalue().splitlines()[-2] == "You don't have enough money to complete the purchase."
        assert mocked_stdout.getvalue().splitlines()[-1] == "Please try again!"


def test_check_cart_invalid_input(user_1, cart_1):
    # Test the function with invalid input strings
    invalid_inputs = ["abcd", "", " ", "4321"]
    for input in invalid_inputs:
        with patch('builtins.input', return_value=input):
            # Assert that the inputs were invalid
            assert(check_cart(user_1, cart_1) == False)


def test_check_cart_contents(user_1, cart_1):
    # Test the function to check that the items remain in the cart if no is chosen
    with patch('sys.stdout', new_callable=io.StringIO) as mocked_stdout:
        with patch('builtins.input', return_value='n'):
            check_cart(user_1, cart_1)
        stdout = mocked_stdout.getvalue()
        for i in cart_1.items:
            # Assert that the items remain in the cart
            assert(i.name in stdout)

def test_check_cart_case_sensitivity(user_1, cart_1):
    # Test the function with invalid input and for upper and lower cases
    invalid_inputs = ["Ya", "ya"]
    for input in invalid_inputs:
        with patch('builtins.input', return_value=input):
            result = check_cart(user_1, cart_1)
            # Assert that the inputs were identified as invalid
            assert(result == False)

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
    # Test the load function for optimal csv data
    with patch('builtins.input', return_value='N'):
        assert(check_cart(user_1, cart_1) == False)

def test_check_cart_input_yes_wrong_case(user_1, cart_1):
    # Test the load function for optimal csv data
    with patch('builtins.input', return_value='Y'):
        assert(check_cart(user_1, cart_1) != False)

def test_check_cart_input_ascii(user_1, cart_1):
    # Test the load function for optimal csv data
    for i in range(0, 256, 1) : 
        if chr(i) == 'y' or 'Y':
            continue

        with patch('builtins.input', return_value=chr(i)):
            assert(check_cart(user_1, cart_1) != False)

def test_check_cart_checkout_called(user_1, cart_1):
    with patch('checkout_and_payment.checkout') as mocked:
        mocked.return_value = None

        with patch('builtins.input', return_value='Y'):
            check_cart(user_1, cart_1)
    
            mocked.assert_called_once()

def test_check_cart_checkout_returns_none(user_1, cart_1):
    with patch('checkout_and_payment.checkout') as mocked:
        mocked.return_value = None

        with patch('builtins.input', return_value='Y'):
            result = check_cart(user_1, cart_1)
    
            mocked.assert_called_once()

            assert(result == None)

def test_check_cart_empty_cart(user_1, cart_2):

    with patch('sys.stdout', new_callable=io.StringIO) as mocked_stdout:
    
        with patch('builtins.input', return_value='Y'):
            result = check_cart(user_1, cart_2)
        
    
            assert(result == None)




        assert mocked_stdout.getvalue() == "\nYour basket is empty. Please add items before checking out.\n"

def test_check_cart_insufficient_funds(user_1, cart_1):

    user_1.wallet = 10

    with patch('sys.stdout', new_callable=io.StringIO) as mocked_stdout:
    
        with patch('builtins.input', return_value='Y'):
            result = check_cart(user_1, cart_1)
        
    
            assert(result == None)




        assert mocked_stdout.getvalue().splitlines()[-2] == "You don't have enough money to complete the purchase."
        assert mocked_stdout.getvalue().splitlines()[-1] == "Please try again!"


def test_check_cart_invalid_input(user_1, cart_1):
    invalid_inputs = ["abc", "", "123", " ", "!"]
    for input in invalid_inputs:
        with patch('builtins.input', return_value=input):
            assert check_cart(user_1, cart_1) == False, f"Failed for input: {input}"


def test_check_cart_contents(user_1, cart_1):
    with patch('sys.stdout', new_callable=io.StringIO) as mocked_stdout:
        with patch('builtins.input', return_value='N'):
            check_cart(user_1, cart_1)
        output = mocked_stdout.getvalue()
        for item in cart_1.items:
            assert item.name in output, f"Item {item.name} not found in cart output"

def test_check_cart_case_sensitivity(user_1, cart_1):
    invalid_inputs = ["yes", "YES"]
    for input in invalid_inputs:
        with patch('builtins.input', return_value=input):
            result = check_cart(user_1, cart_1)
            assert result == False, f"Failed for valid case-insensitive input: {input}"

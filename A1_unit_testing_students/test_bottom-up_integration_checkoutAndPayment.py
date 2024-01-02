import pytest
from io import StringIO
from unittest import mock
from unittest.mock import patch, mock_open, MagicMock

from checkout_and_payment import *
from logout import logout

data_products = [Product("1", 10, 5), Product("2", 20, 3)]

# checkout cluster
def test_successful_checkout():
    # Setup
    user = User("test_user", 100.0)
    cart = ShoppingCart()
    cart.add_item(Product("product1", 10, 2))
    cart.add_item(Product("product2", 20, 1))

    # Test
    with patch('checkout_and_payment.products', side_effect=data_products):
        assert checkout(user, cart) == True

def test_checkout_empty_cart():
    # Setup
    user = User("test_user", 100.0)
    cart = ShoppingCart()

    # Test
    with patch('checkout_and_payment.products', side_effect=data_products):
        assert checkout(user, cart) == False

# check_cart cluster
def test_valid_cart_contents():
    # Setup
    user = User("test_user", 100.0)
    cart = ShoppingCart()
    cart.add_item(Product("product1", 10, 2))
    cart.add_item(Product("product2", 20, 1))

    # Test
    with patch('checkout_and_payment.products', side_effect=data_products), \
         patch('builtins.input', return_value="y"):
        assert check_cart(user, cart) == True

def test_cart_insufficient_funds():
    # Setup
    user = User("test_user", 1.0)
    cart = ShoppingCart()
    cart.add_item(Product("product1", 10, 2))

    # Test
    with patch('checkout_and_payment.products', side_effect=data_products), \
         patch('builtins.input', return_value="y"):
        assert check_cart(user, cart) == False

def test_negative_answer():
    # Setup
    user = User("test_user", 100.0)
    cart = ShoppingCart()
    cart.add_item(Product("product1", 10, 2))

    # Test
    with patch('checkout_and_payment.products', side_effect=data_products), \
         patch('builtins.input', return_value="N"):
        assert check_cart(user, cart) == False

# logout cluster
def test_logout_empty_cart():
    # Setup
    cart = ShoppingCart()

    # Test
    with patch('builtins.input', return_value="Y"):
        assert logout(cart) == True

def test_logout_non_empty_cart():
    # Setup
    cart = ShoppingCart()
    cart.add_item(Product("1", 10, 2))

    # Tes
    with patch('builtins.input', return_value="Y"):
        assert logout(cart) == True

# update_users_json cluster
@pytest.fixture
def mock_open_users_file():
    users = [{"username": "user1", "wallet": 100}, {"username": "user2", "wallet": 200}]
    return mock_open(read_data=json.dumps(users))

def capture_write_calls(mock_file):
    content = []
    original_write = mock_file.write

    def side_effect_write(data):
        content.append(data)
        return original_write(data)

    mock_file.write = MagicMock(side_effect=side_effect_write)
    return content

def test_update_new_user(mock_open_users_file):
    with patch("builtins.open", mock_open_users_file) as mock_file:
        content = capture_write_calls(mock_file())
        update_users_json("new_user", 300)
        assert json.loads(''.join(content)) == [{"username": "user1", "wallet": 100}, {"username": "user2", "wallet": 200}, {"username": "new_user", "wallet": 300}]


# checkoutAndPayment cluster
def test_checkout_and_payment_success():
    # Setup
    login_info = {"username": "existing_username", "wallet": 100}

    # Test
    with patch('checkout_and_payment.products', side_effect=data_products), \
         patch('builtins.input', side_effect=["1", "c", "y", "l"]):
        assert checkoutAndPayment(login_info) == None

def test_payment_insufficient_funds():
    # Setup
    login_info = {"username": "existing_username", "wallet": 1}

    # Test
    with patch('checkout_and_payment.products', side_effect=data_products), \
         patch('builtins.input', side_effect=["1", "c", "y", "l"]):
        assert checkoutAndPayment(login_info) == None


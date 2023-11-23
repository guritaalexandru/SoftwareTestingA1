import json
import pytest
from unittest.mock import patch, mock_open, MagicMock
from checkout_and_payment import checkoutAndPayment, update_users_json, products

@pytest.fixture
def mock_open_users_file():
    users = [{"username": "user1", "wallet": 100}, {"username": "user2", "wallet": 200}]
    return mock_open(read_data=json.dumps(users))

@pytest.fixture
def mock_input(mocker):
    return mocker.patch('builtins.input')

@pytest.fixture
def mock_check_cart(mocker):
    return mocker.patch('checkout_and_payment.check_cart', return_value=True)

@pytest.fixture
def mock_logout(mocker):
    return mocker.patch('checkout_and_payment.logout', return_value=True)

@pytest.fixture
def mock_update_users_json(mocker):
    return mocker.patch('checkout_and_payment.update_users_json')

# Tests for update_users_json
def capture_write_calls(mock_file):
    content = []
    def side_effect_write(data):
        content.append(data)
        return original_write(data)
    original_write = mock_file.write
    mock_file.write = MagicMock(side_effect=side_effect_write)
    return content

def test_update_users_json_existing_user(mock_open_users_file):
    with patch("builtins.open", mock_open_users_file) as mock_file:
        content = capture_write_calls(mock_file())
        update_users_json("user1", 150)
        assert json.loads(''.join(content)) == [{"username": "user1", "wallet": 150}, {"username": "user2", "wallet": 200}]

def test_update_users_json_new_user(mock_open_users_file):
    with patch("builtins.open", mock_open_users_file) as mock_file:
        content = capture_write_calls(mock_file())
        update_users_json("new_user", 300)
        assert json.loads(''.join(content)) == [{"username": "user1", "wallet": 100}, {"username": "user2", "wallet": 200}, {"username": "new_user", "wallet": 300}]

def test_update_users_json_exceptions():
    with patch("builtins.open", mock_open(read_data="not valid json")):
        with pytest.raises(ValueError):
            update_users_json("user1", 150)
    with pytest.raises(FileNotFoundError):
        update_users_json("user1", 150, "nonexistent_file.json")

# Tests for checkoutAndPayment
@pytest.mark.parametrize("invalid_login_info", [
    "invalid_string", 12345, 4.56,
    {"username": "testuser"}, {"wallet": 100},
    {"user": "testuser", "wallet": 100}
])
def test_checkout_and_payment_invalid_login_info_type(invalid_login_info, mock_input, mock_check_cart, mock_logout, mock_update_users_json):
    with pytest.raises(TypeError):
        checkoutAndPayment(invalid_login_info)

@pytest.mark.parametrize("mock_input_value, expected_output", [
    (['l'], "You have been logged out."),
    (['c', 'l'], "You have been logged out."),
    (['1', 'c', 'l'], "Apple added to your cart."),
    (['73', 'l'], "\nInvalid input. Please try again."),
    (['apple', 'l'], "\nInvalid input. Please try again."),
    (['0.75', 'l'], "\nInvalid input. Please try again."),
    (['[]', 'l'], "\nInvalid input. Please try again.")
])
def test_checkout_and_payment_scenarios(mock_input_value, expected_output, mock_input, mock_check_cart, mock_logout, mock_update_users_json, capsys):
    mock_input.side_effect = mock_input_value
    checkoutAndPayment({"username": "testuser", "wallet": 100})
    captured = capsys.readouterr()
    assert expected_output in captured.out
    mock_logout.assert_called_once()

def test_checkout_and_payment_print_products(mock_input, mock_check_cart, mock_logout, mock_update_users_json, capsys):
    mock_input.side_effect = ['l']
    checkoutAndPayment({"username": "testuser", "wallet": 100})
    captured = capsys.readouterr()
    for product in products:
        assert f"{product.name} - ${product.price}" in captured.out
    mock_logout.assert_called_once()

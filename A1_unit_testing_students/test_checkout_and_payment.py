import json
import pytest
from unittest.mock import patch, mock_open, MagicMock
from checkout_and_payment import checkoutAndPayment, update_users_json, products

@pytest.fixture
def mock_open_users_file():
    """Fixture to mock opening of the users file with predefined user data."""
    users = [{"username": "user1", "wallet": 100}, {"username": "user2", "wallet": 200}]
    return mock_open(read_data=json.dumps(users))

@pytest.fixture
def mock_input(mocker):
    """Fixture to mock user input."""
    return mocker.patch('builtins.input')

@pytest.fixture
def mock_check_cart(mocker):
    """Fixture to mock cart checking functionality."""
    return mocker.patch('checkout_and_payment.check_cart', return_value=True)

@pytest.fixture
def mock_logout(mocker):
    """Fixture to mock logout functionality."""
    return mocker.patch('checkout_and_payment.logout', return_value=True)

@pytest.fixture
def mock_update_users_json(mocker):
    """Fixture to mock update_users_json function."""
    return mocker.patch('checkout_and_payment.update_users_json')

def capture_write_calls(mock_file):
    """Helper function to capture write calls to a mock file."""
    content = []
    original_write = mock_file.write

    def side_effect_write(data):
        content.append(data)
        return original_write(data)

    mock_file.write = MagicMock(side_effect=side_effect_write)
    return content

def test_update_users_json_existing_user(mock_open_users_file):
    """Test updating an existing user's wallet amount in the JSON."""
    with patch("builtins.open", mock_open_users_file) as mock_file:
        content = capture_write_calls(mock_file())
        update_users_json("user1", 150)
        assert json.loads(''.join(content)) == [{"username": "user1", "wallet": 150}, {"username": "user2", "wallet": 200}]

def test_update_users_json_new_user(mock_open_users_file):
    """Test adding a new user to the JSON."""
    with patch("builtins.open", mock_open_users_file) as mock_file:
        content = capture_write_calls(mock_file())
        update_users_json("new_user", 300)
        assert json.loads(''.join(content)) == [{"username": "user1", "wallet": 100}, {"username": "user2", "wallet": 200}, {"username": "new_user", "wallet": 300}]

def test_update_users_json_exceptions():
    """Test the behavior of update_users_json with invalid input or file."""
    with patch("builtins.open", mock_open(read_data="not valid json")), pytest.raises(ValueError):
        update_users_json("user1", 150)

    with pytest.raises(FileNotFoundError):
        update_users_json("user1", 150, "nonexistent_file.json")

@pytest.mark.parametrize("invalid_login_info", [
    "invalid_string", 12345, 4.56,
    {"username": "testuser"}, {"wallet": 100},
    {"user": "testuser", "wallet": 100}
])
def test_checkout_and_payment_invalid_login_info(invalid_login_info, mock_input, mock_check_cart, mock_logout, mock_update_users_json):
    """Test checkoutAndPayment with various invalid login info formats."""
    with pytest.raises(TypeError):
        checkoutAndPayment(invalid_login_info)

@pytest.mark.parametrize("mock_input_value, expected_output", [
    (['l'], "You have been logged out."),
    (['c', 'l'], "You have been logged out."),
    (['1', 'c', 'l'], "Apple added to your cart."),
    ([str(len(products) + 1), 'l'], "\nInvalid input. Please try again."),
    (['apple', 'l'], "\nInvalid input. Please try again."),
    (['0.75', 'l'], "\nInvalid input. Please try again."),
    (['[]', 'l'], "\nInvalid input. Please try again.")
])
def test_checkout_and_payment_scenarios(mock_input_value, expected_output, mock_input, mock_check_cart, mock_logout, mock_update_users_json, capsys):
    """Test various scenarios in checkoutAndPayment based on different user inputs."""
    mock_input.side_effect = mock_input_value
    checkoutAndPayment({"username": "testuser", "wallet": 100})
    captured = capsys.readouterr()
    assert expected_output in captured.out
    mock_logout.assert_called_once()

def test_checkout_and_payment_print_products(mock_input, mock_check_cart, mock_logout, mock_update_users_json, capsys):
    """Test that all products are printed correctly in the checkout process."""
    mock_input.side_effect = ['l']
    checkoutAndPayment({"username": "testuser", "wallet": 100})
    captured = capsys.readouterr()
    for product in products:
        assert f"{product.name} - ${product.price}" in captured.out
    mock_logout.assert_called_once()

def test_checkout_and_payment_session_management(mock_input, mock_check_cart, mock_logout, mock_update_users_json, capsys):
    """Test the management of user session in repeated calls of checkoutAndPayment."""
    mock_input.side_effect = ['1', 'l', '2', 'l']
    user_info = {"username": "testuser", "wallet": 100}

    # Test with two consecutive calls to simulate user session
    checkoutAndPayment(user_info)
    checkoutAndPayment(user_info)

    captured = capsys.readouterr()
    assert captured.out.count("You have been logged out.") == 2
    assert mock_logout.call_count == 2

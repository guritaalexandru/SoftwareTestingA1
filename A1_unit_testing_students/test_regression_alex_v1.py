import json
from unittest.mock import patch, mock_open, MagicMock
import io
from io import StringIO

import pytest
from login import login
from logout import logout
from products import display_csv_as_table
from checkout_and_payment import (
    checkout, ShoppingCart, User, products, Product, check_cart, checkoutAndPayment, update_users_json,
    load_products_from_csv
)

valid_test_inputs = ["Ramanathan", "Notaproblem23*"]
invalid_test_inputs = ["Ramanathan", "Notaproblem23*!"]

new_user_N_inputs = ["NewUser", "", "N"]
new_user_X_inputs = ["NewUser", "", "X"]

new_user_valid_password = ["NewUser", "", "Y", "ValidPassword1!"]

valid_csv_products = "Product,Price,Units\nProduct1,10,2\nProduct2,20,1\nProduct3,30,5\n"
expected_output = ("['Product', 'Price', 'Units']\n['Product1', '10', '2']\n['Product2', '20', '1']\n['Product3', "
                   "'30', '5']\n")
expected_filtered_output = "['Product', 'Price', 'Units']\n['Product1', '10', '2']\n"
invalid_filtered_output = "['Product', 'Price', 'Units']\n"


class Cart:
    def __init__(self):
        self.items = [1, 2, 3]

    def retrieve_item(self):
        pass

    def clear_items(self):
        pass


@pytest.fixture(scope="function")
def write_to_file_stub(mocker):
    return mocker.patch('login.write_to_file', return_value=None)


@pytest.fixture(scope="function")
def check_password_stub_correct(mocker):
    return mocker.patch('login.check_password', return_value=True)


@pytest.fixture(scope="function")
def user_1():
    return User("Test", 10)


@pytest.fixture(scope="function")
def user_2():
    return User("Test_Rich", 2000)


@pytest.fixture(scope="function")
def user_3():
    return User("Test_Exakt", 1)


@pytest.fixture(scope="function")
def empty_cart():
    cart = ShoppingCart()
    cart.items = []
    return cart


@pytest.fixture(scope="function")
def filled_cart():
    cart = ShoppingCart()
    cart.add_item(products[0])
    cart.add_item(products[1])
    cart.add_item(products[2])
    cart.add_item(products[3])
    cart.add_item(products[4])
    cart.add_item(products[5])
    return cart


@pytest.fixture(scope="function")
def single_cart_1():
    cart = ShoppingCart()
    cart.add_item(products[0])
    return cart


@pytest.fixture(scope="function")
def multi_cart():
    cart = ShoppingCart()
    cart.add_item(products[0])
    cart.add_item(products[1])
    cart.add_item(products[2])
    cart.add_item(products[4])
    return cart


@pytest.fixture(scope="function")
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
def csv_price_load():
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


@pytest.fixture(scope="function")
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
def csv_units_load():
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

@pytest.fixture(scope="function")
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


@pytest.fixture(scope="function")
def products_fixture(csv_units, csv_name, csv_price):
    products = []
    for i in range(0, 7):
        products.append(Product(csv_name[i], csv_units[i], csv_price[i]))
    return products


@pytest.fixture(scope="function")
def cart_1(products_fixture):
    cart = ShoppingCart()
    cart.items = products
    return cart


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
def mock_update_users_json(mocker):
    """Fixture to mock update_users_json function."""
    return mocker.patch('checkout_and_payment.update_users_json')

@pytest.fixture
def mock_logout(mocker):
    """Fixture to mock logout functionality."""
    return mocker.patch('checkout_and_payment.logout', return_value=True)

@pytest.fixture
def csv_file_optimal_state(tmp_path):
    # Create a temporary CSV file
    test_file = tmp_path / "optimal.csv"
    test_file.write_text(
        """Product,Price,Units
Apple,2,10
Banana,1,15
Orange,1.5,8
Grapes,3,5 
Strawberry,4,12 
Watermelon,10,1 
Carrot,0.5,2"""
    )
    return test_file

@pytest.fixture
def csv_file_body_less_state(tmp_path):
    # Create a temporary CSV file
    test_file = tmp_path / "body_less.csv"
    test_file.write_text("Product,Price,Units")
    return test_file


@pytest.fixture
def csv_file_added_head_state(tmp_path):
    # Create a temporary CSV file
    test_file = tmp_path / "added_head.csv"
    test_file.write_text(
        """Product,Price,Units,Test
Apple,2,10
Banana,1,15
Orange,1.5,8
Grapes,3,5 
Strawberry,4,12 
Watermelon,10,1 
Carrot,0.5,2"""
    )
    return test_file


@pytest.fixture
def csv_file_added_column_state_1(tmp_path):
    # Create a temporary CSV file
    test_file = tmp_path / "added_column_1.csv"
    test_file.write_text(
        """Product,Price,Units, Test
Apple,2,10, Test
Banana,1,15 Test
Orange,1.5,8 Test
Grapes,3,5 Test
Strawberry,4,12 Test
Watermelon,10,1 Test
Carrot,0.5,2 Test"""
    )
    return test_file


@pytest.fixture
def csv_file_added_column_state_2(tmp_path):
    # Create a temporary CSV file
    test_file = tmp_path / "added_column_2.csv"
    test_file.write_text(
        """Product,Price,Test,Units
Apple,2,Test,10
Banana,1,Test,15
Orange,1.5,Test,8
Grapes,3,Test,5 
Strawberry,4,Test,12 
Watermelon,10,Test,1 
Carrot,0.5,Test,2"""
    )
    return test_file


@pytest.fixture
def csv_file_added_column_state_3(tmp_path):
    # Create a temporary CSV file
    test_file = tmp_path / "added_column_3.csv"
    test_file.write_text(
        """Test,Product,Price,Test,Units
Test,Apple,2,Test,10
Test,Banana,1,Test,15
Test,Orange,1.5,Test,8
Test,Grapes,3,Test,5 
Test,Strawberry,4,Test,12 
Test,Watermelon,10,Test,1 
Test,Carrot,0.5,Test,2"""
    )
    return test_file


@pytest.fixture
def csv_file_huge_state(tmp_path):
    # Create a temporary, huge CSV file
    test_file = tmp_path / "mega_size.csv"
    test_file.write_text("Product,Price,Units\n" + "Carrot,0.5,2\n" * 100000)
    return test_file


@pytest.fixture
def csv_file_non_existent_state(tmp_path):
    # Create a temporary, non_existent CSV file
    test_file = tmp_path / "missing_file.csv"
    return test_file


@pytest.fixture
def csv_file_head_less_state(tmp_path):
    # Create a temporary CSV file
    test_file = tmp_path / "head_less.csv"
    test_file.write_text(
        """Apple,2,10
Banana,1,15
Orange,1.5,8
Grapes,3,5 
Strawberry,4,12 
Watermelon,10,1 
Carrot,0.5,2"""
    )
    return test_file


# Test Login
def test_login_existing_user_correct_password():
    with patch('builtins.input', side_effect=valid_test_inputs):
        assert login() == {"username": valid_test_inputs[0], "wallet": 100}


def test_login_existing_user_incorrect_password():
    with patch('builtins.input', side_effect=invalid_test_inputs):
        assert login() is None


def test_login_new_user_no_register():
    with patch('builtins.input', side_effect=new_user_N_inputs):
        assert login() is None


def test_login_new_user_X_register():
    with patch('builtins.input', side_effect=new_user_X_inputs):
        assert login() is None


def test_login_new_user_register_valid_password(write_to_file_stub, check_password_stub_correct):
    with patch('builtins.input', side_effect=new_user_valid_password):
        assert login() == {"username": new_user_valid_password[0], "wallet": 0}
        write_to_file_stub.assert_called_once()
        check_password_stub_correct.assert_called_once_with(new_user_valid_password[3])


# Test Logout
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


# Test Products
# Unite test cases for display_csv_as_table
def test_display_csv_as_table(capsys):
    csv_file = StringIO(valid_csv_products)

    with patch('builtins.open', return_value=csv_file):
        display_csv_as_table('dummy_filename.csv')

    captured = capsys.readouterr()

    assert captured.out == expected_output


def test_display_csv_as_table_row_count(capsys):
    csv_file = StringIO(valid_csv_products)

    with patch('builtins.open', return_value=csv_file):
        display_csv_as_table('dummy_filename.csv')

    captured = capsys.readouterr()
    rows = captured.out.strip().split('\n')
    assert len(rows) == 4


def test_display_csv_as_table_column_count(capsys):
    csv_file = StringIO(valid_csv_products)

    with patch('builtins.open', return_value=csv_file):
        display_csv_as_table('dummy_filename.csv')

    captured = capsys.readouterr()
    rows = captured.out.strip().split('\n')

    # Check the column count in each row
    for line in rows[1:]:
        columns = line.split(',')
        assert len(columns) == 3


def test_display_csv_as_table_with_pdf_file():
    with patch('builtins.open', side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "unicode error")):
        with pytest.raises(UnicodeDecodeError):
            display_csv_as_table('example.pdf')


def test_display_csv_as_table_with_jpg_file():
    with patch('builtins.open', side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "unicode error")):
        with pytest.raises(UnicodeDecodeError):
            display_csv_as_table('example.jpg')


# Test Checkout
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


# Test Check Cart

def test_check_cart_input_no(user_1, cart_1):
    # Test the load function for optimal csv data
    with patch("builtins.input", return_value="N"):
        assert check_cart(user_1, cart_1) == False


def test_check_cart_input_yes_wrong_case(user_1, cart_1):
    # Test the load function for optimal csv data
    with patch("builtins.input", return_value="Y"):
        assert check_cart(user_1, cart_1) == False


def test_check_cart_input_ascii(user_1, cart_1):
    # Test the load function for optimal csv data
    for i in range(0, 256, 1):
        if chr(i) == "y" or "Y":
            continue

        with patch("builtins.input", return_value=chr(i)):
            assert check_cart(user_1, cart_1) != False


def test_check_cart_checkout_called(user_1, cart_1):
    with patch("checkout_and_payment.checkout") as mocked:
        mocked.return_value = None

        with patch("builtins.input", return_value="Y"):
            check_cart(user_1, cart_1)

            mocked.assert_called_once()


def test_check_cart_checkout_returns_none(user_1, cart_1):
    with patch("checkout_and_payment.checkout") as mocked:
        mocked.return_value = None

        with patch("builtins.input", return_value="Y"):
            result = check_cart(user_1, cart_1)

            mocked.assert_called_once()

            assert result == None


# Test Checkout and Payment
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
        assert json.loads(''.join(content)) == [{"username": "user1", "wallet": 150},
                                                {"username": "user2", "wallet": 200}]


def test_update_users_json_new_user(mock_open_users_file):
    """Test adding a new user to the JSON."""
    with patch("builtins.open", mock_open_users_file) as mock_file:
        content = capture_write_calls(mock_file())
        update_users_json("new_user", 300)
        assert json.loads(''.join(content)) == [{"username": "user1", "wallet": 100},
                                                {"username": "user2", "wallet": 200},
                                                {"username": "new_user", "wallet": 300}]


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
def test_checkout_and_payment_invalid_login_info(invalid_login_info, mock_input, mock_check_cart, mock_logout,
                                                 mock_update_users_json):
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
def test_checkout_and_payment_scenarios(mock_input_value, expected_output, mock_input, mock_check_cart, mock_logout,
                                        mock_update_users_json, capsys):
    """Test various scenarios in checkoutAndPayment based on different user inputs."""
    mock_input.side_effect = mock_input_value
    checkoutAndPayment({"username": "testuser", "wallet": 100})
    captured = capsys.readouterr()
    assert expected_output in captured.out
    mock_logout.assert_called_once()


# Test Load Products From CSV
def test_load_products_from_csv_optimal(
    csv_file_optimal_state, csv_name, csv_units_load, csv_price_load
):
    # Test the load function for optimal csv data
    loaded = load_products_from_csv(csv_file_optimal_state)
    for i, v in enumerate(loaded):
        assert v.name == csv_name[i]
        assert v.units == csv_units_load[i]
        assert v.price == csv_price_load[i]


def test_load_products_from_csv_body_less(csv_file_body_less_state):
    # Test the load function for body_less csv data
    loaded = load_products_from_csv(csv_file_body_less_state)
    assert loaded == []


def test_load_products_from_csv_head_less(csv_file_head_less_state):
    # Test the load function for head_less csv data
    with pytest.raises(KeyError):
        load_products_from_csv(csv_file_head_less_state)


def test_load_products_from_csv_edge(
    csv_file_optimal_state, csv_name, csv_units_load, csv_price_load
):
    # Test the load function for optimal csv data, checking edge cases.
    loaded = load_products_from_csv(csv_file_optimal_state)
    assert loaded[0].name == csv_name[0]
    assert loaded[0].units == csv_units_load[0]
    assert loaded[0].price == csv_price_load[0]
    assert loaded[len(loaded) - 1].units == csv_units_load[len(csv_units_load) - 1]
    assert loaded[len(loaded) - 1].price == csv_price_load[len(csv_units_load) - 1]
    assert loaded[len(loaded) - 1].name == csv_name[len(csv_units_load) - 1]


def test_load_products_from_csv_non_existent_file(csv_file_non_existent_state):
    # Test the load function for head_less csv data
    with pytest.raises(FileNotFoundError):
        load_products_from_csv(csv_file_non_existent_state)

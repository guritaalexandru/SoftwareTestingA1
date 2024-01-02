import io
import pytest
from checkout_and_payment import (
    Product,
    User,
    ShoppingCart,
    checkout,
    check_cart,
    products as productz,
    load_products_from_csv,
)
from unittest.mock import patch, mock_open, MagicMock
from logout import logout
from login import login, check_password
import csv
from products import display_csv_as_table, display_filtered_table, searchAndBuyProduct
import json
from checkout_and_payment import checkoutAndPayment, update_users_json
from change_details import change_details


## Fixtures for check_cart
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


## Fixtures for login
valid_test_inputs = ["Ramanathan", "Notaproblem23*"]
invalid_test_inputs = ["Ramanathan", "Notaproblem23*!"]

new_user_N_inputs = ["NewUser", "", "N"]
new_user_X_inputs = ["NewUser", "", "X"]

new_user_valid_password = ["NewUser", "", "Y", "ValidPassword1!"]
new_user_invalid_password = ["NewUser", "", "Y", "invalidpassword"]


@pytest.fixture
def write_to_file_stub(mocker):
    return mocker.patch("login.write_to_file", return_value=None)


@pytest.fixture
def check_password_stub_incorrect(mocker):
    return mocker.patch("login.check_password", return_value=False)


@pytest.fixture
def check_password_stub_correct(mocker):
    return mocker.patch("login.check_password", return_value=True)


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


## Fixtures for logout
class Cart:
    def __init__(self):
        self.items = [1, 2, 3]

    def retrieve_item(self):
        pass

    def clear_items(self):
        pass


## Fixtures for checkout
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
    cart.add_item(productz[0])
    cart.add_item(productz[1])
    cart.add_item(productz[2])
    cart.add_item(productz[3])
    cart.add_item(productz[4])
    cart.add_item(productz[5])
    return cart


@pytest.fixture
def filled_cart_1_units():
    cart = ShoppingCart()
    cart.add_item(productz[0])
    cart.add_item(productz[1])
    cart.add_item(productz[2])
    cart.add_item(productz[3])
    cart.add_item(productz[4])
    cart.add_item(productz[5])
    for i in cart.retrieve_item():
        i.units = 1
    return cart


@pytest.fixture
def single_cart_1():
    cart = ShoppingCart()
    cart.add_item(productz[0])
    return cart


@pytest.fixture
def single_cart_2():
    cart = ShoppingCart()
    cart.add_item(productz[1])
    return cart


@pytest.fixture
def multi_cart():
    cart = ShoppingCart()
    cart.add_item(productz[0])
    cart.add_item(productz[1])
    cart.add_item(productz[2])
    cart.add_item(productz[4])
    return cart


## Fixtures for products
valid_csv_products = (
    "Product,Price,Units\nProduct1,10,2\nProduct2,20,1\nProduct3,30,5\n"
)
expected_output = (
    "['Product', 'Price', 'Units']\n['Product1', '10', '2']\n['Product2', '20', '1']\n['Product3', "
    "'30', '5']\n"
)
expected_filtered_output = "['Product', 'Price', 'Units']\n['Product1', '10', '2']\n"
invalid_filtered_output = "['Product', 'Price', 'Units']\n"


@pytest.fixture
def temp_csv_file_stub():
    csv_file_path = "example.csv"

    with open(csv_file_path, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows([row.split(",") for row in valid_csv_products.split("\n")])

    return csv_file_path


valid_test_inputs = ["Ramanathan", "Notaproblem23*"]
valid_checkout_and_payment_inputs = ["1", "c", "y", "l"]
valid_json_users = """[
  {"username": "Ramanathan", "password": "Notaproblem23*", "wallet": 100}]"""


@pytest.fixture
def mock_login(mocker):
    return mocker.patch(
        "login.login", return_value={"username": "Ramanathan", "wallet": 100}
    )


@pytest.fixture
def mock_input_login(mocker):
    return mocker.patch("login.input", side_effect=valid_test_inputs)


@pytest.fixture
def check_password_stub_correct(mocker):
    return mocker.patch("login.check_password", return_value=True)


@pytest.fixture
def mock_display_csv_as_table(mocker):
    return mocker.patch("products.display_csv_as_table")


@pytest.fixture
def mock_display_filtered_table(mocker):
    return mocker.patch("products.display_filtered_table")


@pytest.fixture
def mock_checkout_and_payment(mocker):
    return mocker.patch("checkout_and_payment.checkoutAndPayment")


@pytest.fixture
def mock_input_checkout_and_payment(mocker):
    return mocker.patch(
        "checkout_and_payment.input", side_effect=valid_checkout_and_payment_inputs
    )


@pytest.fixture
def mock_input_all(mocker):
    return mocker.patch("products.input", side_effect=["all", "Y"])


@pytest.fixture
def mock_input_filtered(mocker):
    return mocker.patch("products.input", side_effect=["Product1", "Y"])


@pytest.fixture
def mock_open_users(mocker):
    json_file = io.StringIO(valid_json_users)
    return mocker.patch(
        "checkout_and_payment.open",
        side_effect=mock_open(read_data=json_file.getvalue()),
    )


## Fixtures for checkoutAndPayment
@pytest.fixture
def mock_open_users_file():
    """Fixture to mock opening of the users file with predefined user data."""
    users = [{"username": "user1", "wallet": 100}, {"username": "user2", "wallet": 200}]
    return mock_open(read_data=json.dumps(users))


@pytest.fixture
def mock_input(mocker):
    """Fixture to mock user input."""
    return mocker.patch("builtins.input")


@pytest.fixture
def mock_check_cart(mocker):
    """Fixture to mock cart checking functionality."""
    return mocker.patch("checkout_and_payment.check_cart", return_value=True)


@pytest.fixture
def mock_logout(mocker):
    """Fixture to mock logout functionality."""
    return mocker.patch("checkout_and_payment.logout", return_value=True)


@pytest.fixture
def mock_update_users_json(mocker):
    """Fixture to mock update_users_json function."""
    return mocker.patch("checkout_and_payment.update_users_json")


## Fixtures for load_products_from_csv
@pytest.fixture
def csv_file_optimal_state(tmp_path):
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
    test_file = tmp_path / "body_less.csv"
    test_file.write_text("Product,Price,Units")
    return test_file


@pytest.fixture
def csv_file_added_head_state(tmp_path):
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
    test_file = tmp_path / "added_column_1.csv"
    test_file.write_text(
        """Product,Price,Units, Test
Apple,2,10,Test
Banana,1,15,Test
Orange,1.5,8,Test
Grapes,3,5,Test
Strawberry,4,12,Test
Watermelon,10,1,Test
Carrot,0.5,2,Test"""
    )
    return test_file


@pytest.fixture
def csv_file_added_column_state_2(tmp_path):
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
    test_file = tmp_path / "mega_size.csv"
    test_file.write_text("Product,Price,Units\n" + "Carrot,0.5,2\n" * 100000)
    return test_file


@pytest.fixture
def csv_file_non_existent_state(tmp_path):
    test_file = tmp_path / "missing_file.csv"
    return test_file


@pytest.fixture
def csv_file_head_less_state(tmp_path):
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


@pytest.fixture
def csv_units():
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
def csv_price():
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


## Fixtures for change_details
@pytest.fixture
def test_entry():
    return {
        "username": "test",
        "password": "test",
        "address": "Dag Hammarskälds Väg",
        "phone": "07099999999",
        "email": "test@gmail.com",
        "credit": {
            "number": "0365027409470925",
            "expiry": "11/25",
            "cvv": "999",
        },
    }


## Tests for check_cart
def test_check_cart_empty_cart(user_1, cart_2):
    # Test with an empty cart
    with patch("sys.stdout", new_callable=io.StringIO) as mocked_stdout:
        with patch("builtins.input", return_value="Y"):
            result = check_cart(user_1, cart_2)

            # Assert the return value
            assert result == False

        # Assert that an empty cart has been identified
        assert (
            mocked_stdout.getvalue()
            == "\nYour basket is empty. Please add items before checking out.\n"
        )


def test_check_cart_insufficient_funds(user_1, cart_1):
    # Test the fucntion with not enough funds in the wallet
    user_1.wallet = 10

    with patch("sys.stdout", new_callable=io.StringIO) as mocked_stdout:
        with patch("builtins.input", return_value="Y"):
            result = check_cart(user_1, cart_1)

            # Assert the return value
            assert result == False

        # Assert that insufficient funds have been identified
        assert (
            mocked_stdout.getvalue().splitlines()[-2]
            == "You don't have enough money to complete the purchase."
        )
        assert mocked_stdout.getvalue().splitlines()[-1] == "Please try again!"


def test_check_cart_invalid_input(user_1, cart_1):
    # Test the function with invalid input strings
    invalid_inputs = ["abcd", "", " ", "4321"]
    for input in invalid_inputs:
        with patch("builtins.input", return_value=input):
            # Assert that the inputs were invalid
            assert check_cart(user_1, cart_1) == False


def test_check_cart_contents(user_1, cart_1):
    # Test the function to check that the items remain in the cart if no is chosen
    with patch("sys.stdout", new_callable=io.StringIO) as mocked_stdout:
        with patch("builtins.input", return_value="n"):
            check_cart(user_1, cart_1)
        stdout = mocked_stdout.getvalue()
        for i in cart_1.items:
            # Assert that the items remain in the cart
            assert i.name in stdout


def test_check_cart_case_sensitivity(user_1, cart_1):
    # Test the function with invalid input and for upper and lower cases
    invalid_inputs = ["Ya", "ya"]
    for input in invalid_inputs:
        with patch("builtins.input", return_value=input):
            result = check_cart(user_1, cart_1)
            # Assert that the inputs were identified as invalid
            assert result == False


## Tests for login
def test_check_password_no_capital():
    assert check_password("password1!") is False


def test_check_password_no_numeral():
    assert check_password("Password!") is False


def test_check_password_too_short():
    assert check_password("Pass1!") is False


def test_check_password_no_special_char():
    assert check_password("Password1") is False


def test_check_password_valid():
    assert check_password("Password1!") is True


## Tests for logout
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


## Tests for checkout
def test_checkout_sufficient_funds(user_2, filled_cart):
    # Test checkout with sufficient user funds
    with patch("sys.stdout", new_callable=io.StringIO) as mocked_stdout:
        checkout(user_2, filled_cart)
        # Assert that sufficient funds was identified in checkout
        assert (
            mocked_stdout.getvalue()
            == "\n\nThank you for your purchase, Test_Rich! Your remaining balance is 1978.5\n"
        )


def test_checkout_product_zero_units_single(user_1, single_cart_1):
    # Test checkout to see that no zero-unit product remains, they should have been removed
    checkout(user_1, single_cart_1)
    for i in single_cart_1.items:
        # Assert units are above zero
        assert i.units > 0


def test_checkout_product_zero_units_multi(user_1, multi_cart):
    # Test checkout for a bigger cart to see that no zero-unit product remains, they should have been removed
    checkout(user_1, multi_cart)
    for i in multi_cart.items:
        # Assert units are above zero
        assert i.units > 0


def test_checkout_just_enough_money(user_3, single_cart_2):
    # Test checkout for the case when the user has just enough money for the transaction
    with patch("sys.stdout", new_callable=io.StringIO) as mocked_stdout:
        checkout(user_3, single_cart_2)
        # Assert that 0.0 money remains in the wallet
        assert (
            mocked_stdout.getvalue()
            == "\n\nThank you for your purchase, Test_Exakt! Your remaining balance is 0.0\n"
        )


def test_checkout_wallet_update(user_2, filled_cart):
    # Test checkout to see that the cost of the transaction is removed from the wallet of the user.
    wallet = user_2.wallet
    price = filled_cart.get_total_price()
    checkout(user_2, filled_cart)
    cost = wallet - price
    # Assert that the remaining money in the wallet wallet is correct
    assert cost == user_2.wallet


## Tests for products
def test_display_csv_as_table_with_pdf_file():
    with patch(
        "builtins.open",
        side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "unicode error"),
    ):
        with pytest.raises(UnicodeDecodeError):
            display_csv_as_table("example.pdf")


def test_display_csv_as_table_with_jpg_file():
    with patch(
        "builtins.open",
        side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "unicode error"),
    ):
        with pytest.raises(UnicodeDecodeError):
            display_csv_as_table("example.jpg")


def test_display_csv_as_table_with_excel_file():
    with patch(
        "builtins.open",
        side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "unicode error"),
    ):
        with pytest.raises(UnicodeDecodeError):
            display_csv_as_table("example.excel")


def test_display_csv_as_table_non_existence_file():
    with pytest.raises(FileNotFoundError):
        display_csv_as_table("nonexistent_file.csv")


def test_display_csv_as_table_empty_file_name():
    with pytest.raises(FileNotFoundError):
        display_csv_as_table("")


def test_display_filtered_csv_as_table_none_search_parameter():
    with pytest.raises(TypeError):
        display_filtered_table(temp_csv_file_stub, None)


def test_display_filtered_csv_as_table_empty_parameter():
    with pytest.raises(TypeError):
        display_filtered_table()


def test_display_filtered_csv_as_table_list_search_parameter():
    with pytest.raises(TypeError):
        display_csv_as_table(temp_csv_file_stub, [1, 2, 3])


def test_display_filtered_csv_as_table_dictionary_search_parameter():
    with pytest.raises(TypeError):
        display_csv_as_table(temp_csv_file_stub, {"filename": "test.csv"})


def test_display_filtered_csv_as_table_int_search_parameter():
    with pytest.raises(TypeError):
        display_csv_as_table(temp_csv_file_stub, 10)


def test_display_filtered_csv_as_table_boolean_search_parameter():
    with pytest.raises(TypeError):
        display_csv_as_table(temp_csv_file_stub, True)


## Test for checkoutAndPayment
def capture_write_calls(mock_file):
    """Helper function to capture write calls to a mock file."""
    content = []
    original_write = mock_file.write

    def side_effect_write(data):
        content.append(data)
        return original_write(data)

    mock_file.write = MagicMock(side_effect=side_effect_write)
    return content


@pytest.mark.parametrize(
    "invalid_login_info",
    [
        "invalid_string",
        12345,
        4.56,
        {"username": "testuser"},
        {"wallet": 100},
        {"user": "testuser", "wallet": 100},
    ],
)
def test_checkout_and_payment_invalid_login_info(
    invalid_login_info, mock_input, mock_check_cart, mock_logout, mock_update_users_json
):
    """Test checkoutAndPayment with various invalid login info formats."""
    with pytest.raises(TypeError):
        checkoutAndPayment(invalid_login_info)


@pytest.mark.parametrize(
    "mock_input_value, expected_output",
    [
        (["l"], "You have been logged out."),
        (["c", "l"], "You have been logged out."),
        (["1", "c", "l"], "Apple added to your cart."),
        ([str(len(productz) + 1), "l"], "\nInvalid input. Please try again."),
        (["apple", "l"], "\nInvalid input. Please try again."),
        (["0.75", "l"], "\nInvalid input. Please try again."),
        (["[]", "l"], "\nInvalid input. Please try again."),
    ],
)
def test_checkout_and_payment_scenarios(
    mock_input_value,
    expected_output,
    mock_input,
    mock_check_cart,
    mock_logout,
    mock_update_users_json,
    capsys,
):
    """Test various scenarios in checkoutAndPayment based on different user inputs."""
    mock_input.side_effect = mock_input_value
    checkoutAndPayment({"username": "testuser", "wallet": 100})
    captured = capsys.readouterr()
    assert expected_output in captured.out
    mock_logout.assert_called_once()


def test_checkout_and_payment_print_products(
    mock_input, mock_check_cart, mock_logout, mock_update_users_json, capsys
):
    """Test that all products are printed correctly in the checkout process."""
    mock_input.side_effect = ["l"]
    checkoutAndPayment({"username": "testuser", "wallet": 100})
    captured = capsys.readouterr()
    for product in productz:
        assert f"{product.name} - ${product.price}" in captured.out
    mock_logout.assert_called_once()


def test_checkout_and_payment_session_management(
    mock_input, mock_check_cart, mock_logout, mock_update_users_json, capsys
):
    """Test the management of user session in repeated calls of checkoutAndPayment."""
    mock_input.side_effect = ["1", "l", "2", "l"]
    user_info = {"username": "testuser", "wallet": 100}

    # Test with two consecutive calls to simulate user session
    checkoutAndPayment(user_info)
    checkoutAndPayment(user_info)

    captured = capsys.readouterr()
    assert captured.out.count("You have been logged out.") == 2
    assert mock_logout.call_count == 2


## Tests for load_products_from_csv
def test_load_products_from_csv_huge_file(csv_file_huge_state):
    # Test the load function for huge ammount of csv data
    loaded = load_products_from_csv(csv_file_huge_state)
    for v in loaded:
        # Assert that the load function performs correctly for large ammounts of data
        assert v.name == "Carrot"
        assert v.units == 2
        assert v.price == 0.5


def test_load_products_from_csv_added_head(
    csv_file_added_head_state, csv_name, csv_units, csv_price
):
    # Test the load function for additional column head added to csv
    loaded = load_products_from_csv(csv_file_added_head_state)
    for i, v in enumerate(loaded):
        # Assert that the load function loads the data in the correct columns
        assert v.name == csv_name[i]
        assert v.units == csv_units[i]
        assert v.price == csv_price[i]


def test_load_products_from_csv_added_column_1(
    csv_file_added_column_state_1, csv_name, csv_units, csv_price
):
    # Test the load function for additional column added at the end to csv
    loaded = load_products_from_csv(csv_file_added_column_state_1)
    for i, v in enumerate(loaded):
        # Assert that the load function gets the right column data
        assert v.name == csv_name[i]
        assert v.units == csv_units[i]
        assert v.price == csv_price[i]


def test_load_products_from_csv_added_column_2(
    csv_file_added_column_state_2, csv_name, csv_units, csv_price
):
    # Test the load function for additional column head added in the middle to csv
    loaded = load_products_from_csv(csv_file_added_column_state_2)
    for i, v in enumerate(loaded):
        # Assert that the load function gets the right column data
        assert v.name == csv_name[i]
        assert v.units == csv_units[i]
        assert v.price == csv_price[i]


def test_load_products_from_csv_added_column_3(
    csv_file_added_column_state_3, csv_name, csv_units, csv_price
):
    # Test the load function for additional column head added in the beginning to csv
    loaded = load_products_from_csv(csv_file_added_column_state_3)
    for i, v in enumerate(loaded):
        # Assert that the load function gets the right column data
        assert v.name == csv_name[i]
        assert v.units == csv_units[i]
        assert v.price == csv_price[i]


## Tests for change_details


def test_change_details_input_not_Y(test_entry):
    with patch("builtins.input", side_effect=["N"]):
        assert change_details(test_entry) == None


def test_change_details_address(test_entry):
    with patch("builtins.input", side_effect=["Y", "a", "Raketvägen"]):
        assert change_details(test_entry) == {
            "username": "test",
            "password": "test",
            "address": "Raketvägen",
            "phone": "07099999999",
            "email": "test@gmail.com",
            "credit": {
                "number": "0365027409470925",
                "expiry": "11/25",
                "cvv": "999",
            },
        }


def test_change_details_credit_card(test_entry):
    with patch(
        "builtins.input", side_effect=["Y", "c", "9999999999999999", "99/99", "999"]
    ):
        assert change_details(test_entry) == {
            "username": "test",
            "password": "test",
            "address": "Dag Hammarskälds Väg",
            "phone": "07099999999",
            "email": "test@gmail.com",
            "credit": {
                "number": "9999999999999999",
                "expiry": "99/99",
                "cvv": "999",
            },
        }

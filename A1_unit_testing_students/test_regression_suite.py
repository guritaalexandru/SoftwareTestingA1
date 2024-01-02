import csv
from io import StringIO
import io
import json
from unittest.mock import MagicMock, mock_open, patch

import pytest
from checkout_and_payment import Product, ShoppingCart, User, check_cart, checkout, checkoutAndPayment, display_and_select_card, load_products_from_csv, update_users_json
from products import display_csv_as_table, display_filtered_table, searchAndBuyProduct
from logout import logout
from login import login, check_password

valid_test_inputs = ["Ramanathan", "Notaproblem23*"]
invalid_test_inputs = ["Ramanathan", "Notaproblem23*!"]

new_user_N_inputs = ["NewUser", "", "N"]
new_user_X_inputs = ["NewUser", "", "X"]

new_user_valid_password = ["NewUser", "", "Y", "ValidPassword1!"]
new_user_invalid_password = ["NewUser", "", "Y", "invalidpassword"]

valid_csv_products = "Product,Price,Units\nProduct1,10,2\nProduct2,20,1\nProduct3,30,5\n"
expected_output = ("['Product', 'Price', 'Units']\n['Product1', '10', '2']\n['Product2', '20', '1']\n['Product3', "
                   "'30', '5']\n")
expected_filtered_output = "['Product', 'Price', 'Units']\n['Product1', '10', '2']\n"
invalid_filtered_output = "['Product', 'Price', 'Units']\n"

products= load_products_from_csv("products.csv")
cart = ShoppingCart()

valid_test_inputs = ["Ramanathan", "Notaproblem23*"]
valid_checkout_and_payment_inputs = ["1", "c", "y", "w", "l"]
valid_json_users = """[
  {"username": "Ramanathan", "password": "Notaproblem23*", "wallet": 100, "cards": [{"name": "Card1", "balance": 1000}]}]"""

@pytest.fixture
def check_password_stub_correct(mocker):
    return mocker.patch('login.check_password', return_value=True)

@pytest.fixture
def write_to_file_stub(mocker):
    return mocker.patch('login.write_to_file', return_value=None)

@pytest.fixture
def check_password_stub_incorrect(mocker):
    return mocker.patch('login.check_password', return_value=False)

@pytest.fixture
def temp_csv_file_stub():
    csv_file_path = "example.csv"

    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows([row.split(',') for row in valid_csv_products.split('\n')])

    return csv_file_path


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

@pytest.fixture
def user_1():
    return User("Test", 10, [{"name": "Card1", "balance": 1000}])


@pytest.fixture
def user_2():
    return User("Test_Rich", 2000, [{"name": "Card1", "balance": 5000}])


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

@pytest.fixture
def products_(csv_units, csv_name, csv_price):
    products = []
    for i in range(0, 7):
        products.append(Product(csv_name[i], csv_units[i], csv_price[i]))
    return products

@pytest.fixture
def cart_1(products_):
    cart = ShoppingCart()
    cart.items = products
    return cart

@pytest.fixture
def cart_2():
    cart = ShoppingCart()
    cart.clear_items()
    return cart

@pytest.fixture
def mock_open_users_file():
    """Fixture to mock opening of the users file with predefined user data."""
    users = [{"username": "user1", "wallet": 100, "cards":[{"name": "Card1", "balance": 5000}]}, {"username": "user2", "wallet": 200, "cards":[{"name": "Card1", "balance": 5000}]}]
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

@pytest.fixture
def mock_login(mocker):
    return mocker.patch('login.login', return_value={"username": "Ramanathan", "wallet": 100})


@pytest.fixture
def mock_input_login(mocker):
    return mocker.patch('login.input', side_effect=valid_test_inputs)

@pytest.fixture
def check_password_stub_correct(mocker):
    return mocker.patch('login.check_password', return_value=True)


@pytest.fixture
def mock_display_csv_as_table(mocker):
    return mocker.patch('products.display_csv_as_table')


@pytest.fixture
def mock_display_filtered_table(mocker):
    return mocker.patch('products.display_filtered_table')


@pytest.fixture
def mock_checkout_and_payment(mocker):
    return mocker.patch('checkout_and_payment.checkoutAndPayment')


@pytest.fixture
def mock_input_checkout_and_payment(mocker):
    return mocker.patch('checkout_and_payment.input', side_effect=valid_checkout_and_payment_inputs)


@pytest.fixture
def mock_input_all(mocker):
    return mocker.patch('products.input', side_effect=['all', 'Y'])


@pytest.fixture
def mock_input_filtered(mocker):
    return mocker.patch('products.input', side_effect=['Product1', 'Y'])


@pytest.fixture
def mock_open_users(mocker):
    json_file = StringIO(valid_json_users)
    return mocker.patch('checkout_and_payment.open', side_effect=mock_open(read_data=json_file.getvalue()))

@pytest.fixture
def user_4():
    return User("Test_Exakt", 1000, [{"name": "Card1", "balance": 100}, {"name": "Card2", "balance": 200}])

@pytest.fixture
def user_5():
    return User("Test_Exakt", 1000, [{"name": "Card1", "balance": 30}, {"name": "Card2", "balance": 200}])

@pytest.fixture
def mock_input_payment_method(mocker):
    return mocker.patch('checkout_and_payment.input', side_effect=['w'])

@pytest.fixture
def mock_input_checkout_decision(mocker):
    return mocker.patch('checkout_and_payment.input', side_effect=['y'])

@pytest.fixture
def mock_display_and_select_card(mocker):
    return mocker.patch('checkout_and_payment.display_and_select_card', return_value=True)

@pytest.fixture
def mock_checkout(mocker):
    return mocker.patch('checkout_and_payment.checkout', return_value=False)

def capture_write_calls(mock_file):
    """Helper function to capture write calls to a mock file."""
    content = []
    original_write = mock_file.write

    def side_effect_write(data):
        content.append(data)
        return original_write(data)

    mock_file.write = MagicMock(side_effect=side_effect_write)
    return content

class Cart:
    def __init__(self):
        self.items = [1, 2, 3]

    def retrieve_item(self):
        pass

    def clear_items(self):
        pass

"""
Funtion: Login
Test No: 1
Scenario: Login should success for correct password.
"""
def test_login_existing_user_correct_password():
    with patch('builtins.input', side_effect=valid_test_inputs):
        assert login() == {"username": valid_test_inputs[0], "wallet": 100, "cards": [{"name": "Card1", "balance": 991.5}]}


"""
Funtion: Login
Test No: 2
Scenario: Login should fail for incorrect password.
"""
def test_login_existing_user_incorrect_password():
    with patch('builtins.input', side_effect=invalid_test_inputs):
        assert login() is None


"""
Funtion: Login
Test No: 3
Scenario: Login should fail for incorrect password.
"""
def test_login_new_user_no_register():
    with patch('builtins.input', side_effect=new_user_N_inputs):
        assert login() is None


"""
Funtion: Login
Test No: 4
Scenario: If user is a new user, user should be able to register to the system with a valid password.
"""
def test_login_new_user_register_valid_password(write_to_file_stub, check_password_stub_correct):
    with patch('builtins.input', side_effect=new_user_valid_password):
        assert login() == {"username": new_user_valid_password[0], "wallet": 0, "cards": []}
        write_to_file_stub.assert_called_once()
        check_password_stub_correct.assert_called_once_with(new_user_valid_password[3])

"""
Funtion: Login
Test No: 5
Scenario: If user is a new user, user should not be able to register to the system with an invalid password.
"""
def test_login_new_user_register_invalid_password(check_password_stub_incorrect):
    with patch('builtins.input', side_effect=new_user_invalid_password):
        assert login() is None
        check_password_stub_incorrect.assert_called_once_with(new_user_invalid_password[3])


"""
Funtion: Check password
Test No: 6
Scenario: Check if the password is having a Capital letter
"""
def test_check_password_no_capital():
    assert check_password("password1!") is False


"""
Funtion: Check password
Test No: 7
Scenario: Check if the password is numerical
"""
def test_check_password_no_numerical():
    assert check_password("Password!") is False


"""
Funtion: Check password
Test No: 8
Scenario: Check if the password is long enough
"""
def test_check_password_too_short():
    assert check_password("Pass1!") is False


"""
Funtion: Check password
Test No: 9
Scenario: Check if the password is not having a special char
"""
def test_check_password_no_special_char():
    assert check_password("Password1") is False


"""
Funtion: Check password
Test No: 10
Scenario: Check if the password is valid
"""
def test_check_password_valid():
    assert check_password("Password1!") is True


"""
Funtion: logout
Test No: 11
Scenario: Check logout success for empty cart
"""
def test_logout_empty_cart():
    cart_instance = Cart()

    with patch.object(cart_instance, 'items') as mock_items:
        # Set the length of cart.items to simulate an empty cart
        mock_items.__len__.return_value = 0
        assert logout(cart_instance) is True


"""
Funtion: logout
Test No: 12
Scenario: Check logout fail for non-empty cart with no confirmation
"""
def test_logout_non_empty_cart_no_confirmation():
    cart_instance = Cart()

    with patch.object(cart_instance, 'retrieve_item') as mock_retrieve_item, \
            patch('builtins.input', side_effect=['N']):
        result = logout(cart_instance)

        # Assert that retrieve_item was called once
        mock_retrieve_item.assert_called_once()
        assert result is False

"""
Funtion: logout
Test No: 13
Scenario: Check logout success for non-empty cart with confirmation
"""
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


"""
Funtion: logout
Test No: 14
Scenario: Check logout fail for string input
"""
def test_logout_string_input():
    try:
        logout("not_a_cart_instance")
        assert False, "Expected an exception for incorrect input type"
    except AttributeError:
        # The function should raise a AttributeError for incorrect input type
        assert True  # The function raised the expected exception


"""
Funtion: logout
Test No: 15
Scenario: Check logout fail for empty input
"""
def test_logout_empty_input():
    try:
        logout()
        assert False, "Expected an exception for incorrect input type"
    except TypeError:
        # The function should raise a TypeError for incorrect input type
        assert True  # The function raised the expected exception


"""
Funtion: display_csv_as_table
Test No: 16
Scenario: Check display_csv_as_table work for valid csv
"""
def test_display_csv_as_table(capsys):
    csv_file = StringIO(valid_csv_products)

    with patch('builtins.open', return_value=csv_file):
        display_csv_as_table('dummy_filename.csv')

    captured = capsys.readouterr()

    assert captured.out == expected_output


"""
Funtion: display_csv_as_table
Test No: 17
Scenario: Check display_csv_as_table give correct row count for valid csv
"""
def test_display_csv_as_table_row_count(capsys):
    csv_file = StringIO(valid_csv_products)

    with patch('builtins.open', return_value=csv_file):
        display_csv_as_table('dummy_filename.csv')

    captured = capsys.readouterr()
    rows = captured.out.strip().split('\n')
    assert len(rows) == 4


"""
Funtion: display_csv_as_table
Test No: 18
Scenario: Check display_csv_as_table give correct column count for valid csv
"""
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


"""
Funtion: display_csv_as_table
Test No: 19
Scenario: Check display_csv_as_table give error for non csv file
"""
def test_display_csv_as_table_with_pdf_file():
    with patch('builtins.open', side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "unicode error")):
        with pytest.raises(UnicodeDecodeError):
            display_csv_as_table('example.pdf')

"""
Funtion: display_csv_as_table
Test No: 20
Scenario: Check display_csv_as_table give error for None input
"""
def test_display_csv_as_table_none_input():
    with pytest.raises(TypeError):
        display_csv_as_table(None)


"""
Funtion: display_filtered_csv_as_table
Test No: 21
Scenario: Check display_csv_as_table give expected output
"""
def test_display_filtered_csv_as_table(capsys):
    csv_file = StringIO(valid_csv_products)

    with patch('builtins.open', return_value=csv_file):
        display_filtered_table('dummy_filename.csv', 'Product1')

    captured = capsys.readouterr()

    assert captured.out == expected_filtered_output


"""
Funtion: display_filtered_csv_as_table
Test No: 22
Scenario: Check display_csv_as_table give correct row count
"""
def test_display_filtered_csv_as_table_row_count(capsys):
    csv_file = StringIO(valid_csv_products)

    with patch('builtins.open', return_value=csv_file):
        display_filtered_table('dummy_filename.csv', 'Product1')

    captured = capsys.readouterr()
    rows = captured.out.strip().split('\n')
    assert len(rows) == 2


"""
Funtion: display_filtered_csv_as_table
Test No: 23
Scenario: Check display_csv_as_table give expected output by ignoring the case
"""
def test_display_filtered_csv_as_table_ignore_case(capsys):
    csv_file = StringIO(valid_csv_products)

    with patch('builtins.open', return_value=csv_file):
        display_filtered_table('dummy_filename.csv', 'product1')

    captured = capsys.readouterr()
    rows = captured.out.strip().split('\n')
    assert len(rows) == 2
    assert captured.out == expected_filtered_output


"""
Funtion: display_filtered_csv_as_table
Test No: 24
Scenario: Check display_csv_as_table give empty table if search for non-existing product
"""
def test_display_filtered_csv_as_table_invalid_search_parameter(capsys):
    csv_file = StringIO(valid_csv_products)

    with patch('builtins.open', return_value=csv_file):
        display_filtered_table('dummy_filename.csv', 'XYZ')

    captured = capsys.readouterr()
    rows = captured.out.strip().split('\n')
    assert len(rows) == 1
    assert captured.out == invalid_filtered_output


"""
Funtion: display_filtered_csv_as_table
Test No: 25
Scenario: Check display_csv_as_table give empty table if search for empty string
"""
def test_display_filtered_csv_as_table_empty_search_parameter(capsys):
    csv_file = StringIO(valid_csv_products)

    with patch('builtins.open', return_value=csv_file):
        display_filtered_table('dummy_filename.csv', '')

    captured = capsys.readouterr()
    rows = captured.out.strip().split('\n')
    assert len(rows) == 1
    assert captured.out == invalid_filtered_output

"""
Funtion: searchAndBuyProduct
Test No: 26
Scenario: Check searchAndBuyProduct correctly called display all products from csv for input all
"""
def test_search_and_buy_product_all(mock_login, check_password_stub_correct, mock_display_csv_as_table,
                                    mock_checkout_and_payment,
                                    mock_input_all, mock_input_login, mock_input_checkout_and_payment, mock_open_users):
    searchAndBuyProduct()
    mock_display_csv_as_table.assert_called_once()

"""
Funtion: searchAndBuyProduct
Test No: 27
Scenario: Check searchAndBuyProduct correctly called display all products from csv for search input
"""
def test_search_and_buy_products_filtered(mock_login, check_password_stub_correct,
                                          mock_checkout_and_payment, mock_display_filtered_table,
                                          mock_input_filtered, mock_input_login, mock_input_checkout_and_payment,
                                          mock_open_users):
    searchAndBuyProduct()
    mock_display_filtered_table.assert_called_once()

"""
Funtion: load_products_from_csv
Test No: 28
Scenario: Check load_products_from_csv load optimal csv data correctly
"""
def test_load_products_from_csv_optimal(
    csv_file_optimal_state, csv_name, csv_units, csv_price
):
    # Test the load function for optimal csv data
    loaded = load_products_from_csv(csv_file_optimal_state)
    for i, v in enumerate(loaded):
        # Assert that the loaded products have the correct values in the correct fields
        assert v.name == csv_name[i]
        assert v.units == csv_units[i]
        assert v.price == csv_price[i]


"""
Funtion: load_products_from_csv
Test No: 29
Scenario: Check load_products_from_csv load column names correctly
"""
def test_load_products_from_csv_body_less(csv_file_body_less_state):
    # Test the load function for csv data with only the column names
    loaded = load_products_from_csv(csv_file_body_less_state)
    # Assert that the loaded products is an empty list
    assert loaded == []


"""
Funtion: load_products_from_csv
Test No: 30
Scenario: Check load_products_from_csv load column names correctly
"""
def test_load_products_from_csv_head_less(csv_file_head_less_state):
    # Test the load function for csv data without the csv column names
    # Assure that the load function raises an error for this kind of input data
    with pytest.raises(KeyError):
        load_products_from_csv(csv_file_head_less_state)


"""
Funtion: load_products_from_csv
Test No: 31
Scenario: Check load_products_from_csv load column names correctly
"""
def test_load_products_from_csv_edge(
    csv_file_optimal_state, csv_name, csv_units, csv_price
):
    # Test the load function for optimal csv data, checking edge cases.
    loaded = load_products_from_csv(csv_file_optimal_state)
    # Assert that the load function performs correctly on these edge cases
    assert loaded[0].name == csv_name[0]
    assert loaded[0].units == csv_units[0]
    assert loaded[0].price == csv_price[0]
    assert loaded[len(loaded) - 1].units == csv_units[len(csv_units) - 1]
    assert loaded[len(loaded) - 1].price == csv_price[len(csv_units) - 1]
    assert loaded[len(loaded) - 1].name == csv_name[len(csv_units) - 1]


"""
Funtion: load_products_from_csv
Test No: 32
Scenario: Check load_products_from_csv give error if file is not exists
"""
def test_load_products_from_csv_non_existent_file(csv_file_non_existent_state):
    # Test the load function for head_less csv data
    # Assure that the load function raises an error when the input csv file is non-existant
    with pytest.raises(FileNotFoundError):
        load_products_from_csv(csv_file_non_existent_state)


"""
Funtion: checkout
Test No: 33
Scenario: Check checkout identified basket is empty
"""
def test_checkout_empty(user_1, empty_cart):
    # Test checkout with an empty cart
    with patch("sys.stdout", new_callable=io.StringIO) as mocked_stdout:
        checkout(user_1, empty_cart)
        # Assert that empty basket was identified
        assert (
            mocked_stdout.getvalue()
            == "\nYour basket is empty. Please add items before checking out.\n"
        )


"""
Funtion: checkout
Test No: 34
Scenario: Check checkout work with single item in cart
"""
def test_checkout_single(user_1, single_cart_1, mock_input_payment_method, mock_display_and_select_card):
    # Test checkout with a single item in the cart
    with patch("sys.stdout", new_callable=io.StringIO) as mocked_stdout:
        checkout(user_1, single_cart_1)
        # Assert that the one item was bought
        assert (
            mocked_stdout.getvalue()
            == "\n\nThank you for your purchase, Test! Your remaining balance is 8.0\n"
        )


"""
Funtion: checkout
Test No: 35
Scenario: Check checkout work with multiple items in cart
"""
def test_checkout_multiple(user_1, multi_cart, mock_input_payment_method, mock_display_and_select_card):
    # The checkout with multiple items in cart
    with patch("sys.stdout", new_callable=io.StringIO) as mocked_stdout:
        checkout(user_1, multi_cart)
        # Assert that multiple items were bought
        assert (
            mocked_stdout.getvalue()
            == "\n\nThank you for your purchase, Test! Your remaining balance is 1.5\n"
        )


"""
Funtion: checkout
Test No: 36
Scenario: Check checkout with insufficient user funds
"""
def test_checkout_insufficient_funds(user_1, filled_cart, mock_input_payment_method):
    # Test checkout with insufficient user funds
    with patch("sys.stdout", new_callable=io.StringIO) as mocked_stdout:
        checkout(user_1, filled_cart)
        # Assert that insufficient funds was identified in checkout
        assert (
            mocked_stdout.getvalue()
            == "\n\nYou don't have enough money to complete the purchase.\nPlease try again!\n"
        )

"""
Funtion: checkout
Test No: 37
Scenario: Check checkout with sufficient user funds
"""
def test_checkout_sufficient_funds(user_2, multi_cart, mock_input_payment_method):
    # Test checkout with sufficient user funds
    with patch("sys.stdout", new_callable=io.StringIO) as mocked_stdout:
        checkout(user_2, multi_cart)
        # Assert that sufficient funds was identified in checkout
        assert (
            mocked_stdout.getvalue()
            == "\n\nThank you for your purchase, Test_Rich! Your remaining balance is 1991.5\n"
        )


"""
Funtion: check_cart
Test No: 38
Scenario: Check check_cart with negative input
"""
def test_check_cart_input_no(user_1, cart_1):
    # Simulate input a negative input
    with patch('builtins.input', return_value='N'):
        # Assert that input is no
        assert(check_cart(user_1, cart_1) == False)


"""
Funtion: check_cart
Test No: 39
Scenario: Check check_cart with yes input
"""
def test_check_cart_input_yes_wrong_case(user_1, cart_1):
    # Simulate a positive input, with an incorrect case to check that it still works
    with patch('builtins.input', return_value='Y'):
        # Assert that the input was yes
        assert(check_cart(user_1, cart_1) == False)


"""
Funtion: check_cart
Test No: 40
Scenario: Check check_cart empty cart
"""
def test_check_cart_empty_cart(user_1, cart_2):
    # Test with an empty cart
    with patch('sys.stdout', new_callable=io.StringIO) as mocked_stdout:
    
        with patch('builtins.input', return_value='Y'):
            result = check_cart(user_1, cart_2)
        
            # Assert the return value 
            assert(result == False)

        # Assert that an empty cart has been identified
        assert mocked_stdout.getvalue() == "\nYour basket is empty. Please add items before checking out.\n"


"""
Funtion: check_cart
Test No: 41
Scenario: Check check_cart insufficient funds
"""
def test_check_cart_insufficient_funds(user_1, cart_1):
    # Test the fucntion with not enough funds in the wallet
    user_1.wallet = 0

    with patch('sys.stdout', new_callable=io.StringIO) as mocked_stdout:
    
        with patch('builtins.input', side_effect=['y', 'w']):
            result = check_cart(user_1, cart_1)
        
            # Assert the return value 
            assert(result == False)

        # Assert that insufficient funds have been identified
        assert mocked_stdout.getvalue().splitlines()[-2] == "You don't have enough money to complete the purchase."
        assert mocked_stdout.getvalue().splitlines()[-1] == "Please try again!"


"""
Funtion: check_cart
Test No: 42
Scenario: Check check_cart invalid input
"""
def test_check_cart_invalid_input(user_1, cart_1):
    # Test the function with invalid input strings
    invalid_inputs = ["abcd", "", " ", "4321"]
    for input in invalid_inputs:
        with patch('builtins.input', return_value=input):
            # Assert that the inputs were invalid
            assert(check_cart(user_1, cart_1) == False)

"""
Funtion: update_users_json
Test No: 43
Scenario: Check update_users_json updates existing user details correctly
"""
def test_update_users_json_existing_user(mock_open_users_file):
    """Test updating an existing user's wallet amount in the JSON."""
    with patch("builtins.open", mock_open_users_file) as mock_file:
        content = capture_write_calls(mock_file())
        update_users_json("user1", 150, [{"name": "Card1", "balance": 5000}])
        assert json.loads(''.join(content)) == [{"username": "user1", "wallet": 150, "cards":[{"name": "Card1", "balance": 5000}]}, {"username": "user2", "wallet": 200, "cards":[{"name": "Card1", "balance": 5000}]}]


"""
Funtion: update_users_json
Test No: 44
Scenario: Check update_users_json updates new user details correctly
"""
def test_update_users_json_new_user(mock_open_users_file):
    """Test adding a new user to the JSON."""
    with patch("builtins.open", mock_open_users_file) as mock_file:
        content = capture_write_calls(mock_file())
        update_users_json("new_user", 300, [{"name": "Card1", "balance": 7000}])
        assert json.loads(''.join(content)) == [{"username": "user1", "wallet": 100, "cards":[{"name": "Card1", "balance": 5000}]}, {"username": "user2", "wallet": 200, "cards":[{"name": "Card1", "balance": 5000}]}, {"username": "new_user", "wallet": 300, "cards":[{"name": "Card1", "balance": 7000}]}]


"""
Funtion: update_users_json
Test No: 45
Scenario: Check update_users_json give error for invalid file
"""
def test_update_users_json_exceptions():
    """Test the behavior of update_users_json with invalid input or file."""
    with patch("builtins.open", mock_open(read_data="not valid json")), pytest.raises(ValueError):
        update_users_json("user1", 150, [{"name": "Card1", "balance": 5000}])

    with pytest.raises(FileNotFoundError):
        update_users_json("user1", 150, [{"name": "Card1", "balance": 5000}], "nonexistent_file.json")

"""
Funtion: checkoutAndPayment
Test No: 46
Scenario: Check checkoutAndPayment give error for invalid login info
"""
@pytest.mark.parametrize("invalid_login_info", [
    "invalid_string", 12345, 4.56,
    {"username": "testuser"}, {"wallet": 100},
    {"user": "testuser", "wallet": 100}
])
def test_checkout_and_payment_invalid_login_info(invalid_login_info, mock_input, mock_check_cart, mock_logout, mock_update_users_json):
    """Test checkoutAndPayment with various invalid login info formats."""
    with pytest.raises(TypeError):
        checkoutAndPayment(invalid_login_info)

"""
Funtion: checkoutAndPayment
Test No: 47
Scenario: Check checkoutAndPayment for different inputs
"""
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
    checkoutAndPayment({"username": "testuser", "wallet": 100, "cards": [{"name": "Card1", "balance": 100}]})
    captured = capsys.readouterr()
    assert expected_output in captured.out
    mock_logout.assert_called_once()

"""
Funtion: checkoutAndPayment
Test No: 48
Scenario: Check checkoutAndPayment print product list correctly
"""
def test_checkout_and_payment_print_products(mock_input, mock_check_cart, mock_logout, mock_update_users_json, capsys):
    """Test that all products are printed correctly in the checkout process."""
    mock_input.side_effect = ['l']
    checkoutAndPayment({"username": "testuser", "wallet": 100, "cards": [{"name": "Card1", "balance": 100}]})
    captured = capsys.readouterr()
    for product in products:
        assert f"{product.name} - ${product.price}" in captured.out
    mock_logout.assert_called_once()


"""
Funtion: checkoutAndPayment
Test No: 49
Scenario: Check checkoutAndPayment works with multiple sessions
"""
def test_checkout_and_payment_session_management(mock_input, mock_check_cart, mock_logout, mock_update_users_json, capsys):
    """Test the management of user session in repeated calls of checkoutAndPayment."""
    mock_input.side_effect = ['1', 'l', '2', 'l']
    user_info = {"username": "testuser", "wallet": 100, "cards": [{"name": "Card1", "balance": 100}]}

    # Test with two consecutive calls to simulate user session
    checkoutAndPayment(user_info)
    checkoutAndPayment(user_info)

    captured = capsys.readouterr()
    assert captured.out.count("You have been logged out.") == 2
    assert mock_logout.call_count == 2


"""New test cases for payment method card feature"""
def test_display_and_select_card_success(user_4, mocker):
    mocker.patch("builtins.input", side_effect=["1"])
    assert display_and_select_card(user_4, 50) is True


def test_display_and_select_card_cancel(user_4, mocker):
    mocker.patch("builtins.input", side_effect=["c"])
    assert display_and_select_card(user_4, 50) is False
    assert user_4.cards == [{"name": "Card1", "balance": 100}, {"name": "Card2", "balance": 200}]

def test_display_and_select_card_insufficient_balance(user_5, mocker):
    mocker.patch("builtins.input", side_effect=["1"])
    assert display_and_select_card(user_5, 50) is False
    assert user_5.cards == [{"name": "Card1", "balance": 30}, {"name": "Card2", "balance": 200}]

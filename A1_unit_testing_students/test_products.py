from unittest import mock

import pytest
import csv
from io import StringIO
from unittest.mock import patch
from products import display_csv_as_table, display_filtered_table, searchAndBuyProduct

valid_csv_products = "Product,Price,Units\nProduct1,10,2\nProduct2,20,1\nProduct3,30,5\n"
expected_output = ("['Product', 'Price', 'Units']\n['Product1', '10', '2']\n['Product2', '20', '1']\n['Product3', "
                   "'30', '5']\n")
expected_filtered_output = "['Product', 'Price', 'Units']\n['Product1', '10', '2']\n"
invalid_filtered_output = "['Product', 'Price', 'Units']\n"


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


def test_display_csv_as_table_with_excel_file():
    with patch('builtins.open', side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "unicode error")):
        with pytest.raises(UnicodeDecodeError):
            display_csv_as_table('example.excel')


def test_display_csv_as_table_non_existence_file():
    with pytest.raises(FileNotFoundError):
        display_csv_as_table('nonexistent_file.csv')


def test_display_csv_as_table_empty_file_name():
    with pytest.raises(FileNotFoundError):
        display_csv_as_table('')


# test for int, float, list, empty inputs

def test_display_csv_as_table_none_input():
    with pytest.raises(TypeError):
        display_csv_as_table(None)


def test_display_csv_as_table_list_input():
    with pytest.raises(TypeError):
        display_csv_as_table([1, 2, 3])


def test_display_csv_as_table_dictionary_input():
    with pytest.raises(TypeError):
        display_csv_as_table({'filename': 'test.csv'})


# Unit test cases for display_filtered_table

@pytest.fixture
def temp_csv_file_stub():
    csv_file_path = "example.csv"

    with open(csv_file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerows([row.split(',') for row in valid_csv_products.split('\n')])

    return csv_file_path


def test_display_filtered_csv_as_table(capsys):
    csv_file = StringIO(valid_csv_products)

    with patch('builtins.open', return_value=csv_file):
        display_filtered_table('dummy_filename.csv', 'Product1')

    captured = capsys.readouterr()

    assert captured.out == expected_filtered_output


def test_display_filtered_csv_as_table_row_count(capsys):
    csv_file = StringIO(valid_csv_products)

    with patch('builtins.open', return_value=csv_file):
        display_filtered_table('dummy_filename.csv', 'Product1')

    captured = capsys.readouterr()
    rows = captured.out.strip().split('\n')
    assert len(rows) == 2


def test_display_filtered_csv_as_table_ignore_case(capsys):
    csv_file = StringIO(valid_csv_products)

    with patch('builtins.open', return_value=csv_file):
        display_filtered_table('dummy_filename.csv', 'product1')

    captured = capsys.readouterr()
    rows = captured.out.strip().split('\n')
    assert len(rows) == 2
    assert captured.out == expected_filtered_output


def test_display_filtered_csv_as_table_invalid_search_parameter(capsys):
    csv_file = StringIO(valid_csv_products)

    with patch('builtins.open', return_value=csv_file):
        display_filtered_table('dummy_filename.csv', 'XYZ')

    captured = capsys.readouterr()
    rows = captured.out.strip().split('\n')
    assert len(rows) == 1
    assert captured.out == invalid_filtered_output


def test_display_filtered_csv_as_table_empty_search_parameter(capsys):
    csv_file = StringIO(valid_csv_products)

    with patch('builtins.open', return_value=csv_file):
        display_filtered_table('dummy_filename.csv', '')

    captured = capsys.readouterr()
    rows = captured.out.strip().split('\n')
    assert len(rows) == 1
    assert captured.out == invalid_filtered_output


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
        display_csv_as_table(temp_csv_file_stub, {'filename': 'test.csv'})


def test_display_filtered_csv_as_table_int_search_parameter():
    with pytest.raises(TypeError):
        display_csv_as_table(temp_csv_file_stub, 10)


def test_display_filtered_csv_as_table_boolean_search_parameter():
    with pytest.raises(TypeError):
        display_csv_as_table(temp_csv_file_stub, True)


# Unit test cases for searchAndBuyProduct
valid_test_inputs = ["Ramanathan", "Notaproblem23*"]
valid_checkout_and_payment_inputs = ["1", "c", "y", "l"]


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


def test_search_and_buy_product_all(mock_login, check_password_stub_correct, mock_display_csv_as_table,
                                    mock_checkout_and_payment,
                                    mock_input_all, mock_input_login, mock_input_checkout_and_payment):
    searchAndBuyProduct()
    mock_display_csv_as_table.assert_called_once()


def test_search_and_buy_products_filtered(mock_login, check_password_stub_correct,
                                          mock_checkout_and_payment, mock_display_filtered_table,
                                          mock_input_filtered, mock_input_login, mock_input_checkout_and_payment):
    searchAndBuyProduct()
    mock_display_filtered_table.assert_called_once()

import pytest
from io import StringIO
from unittest import mock
from unittest.mock import patch, mock_open

import main

# Integration test first level
def stub_searchAndBuyProduct():
    return None

def test_main():
    with mock.patch('main.searchAndBuyProduct', side_effect=stub_searchAndBuyProduct) as mock_searchAndBuyProduct:
        main.run_program()

        # Assertions to verify that the stubs were called
        mock_searchAndBuyProduct.assert_called_once()



# Integration test second level
data_test_searchAndBuyProduct = {
    "valid_login_info": {"username": "existing_username", "wallet": 100},
    "valid_inputs": ["all", "N", "1", "Y"]
}

def stub_login():
    return data_test_searchAndBuyProduct['valid_login_info']

def stub_display_csv_as_table(csv_filename):
    print("Displaying all products")

def stub_display_filtered_table(csv_filename, search):
    print(f"Displaying products filtered by: {search}")

def stub_checkoutAndPayment(login_info):
    print("Checkout and Payment process initiated")

def test_searchAndBuyProduct():
    with patch('products.login', side_effect=stub_login) as mock_login, \
         patch('products.display_csv_as_table', side_effect=stub_display_csv_as_table) as mock_display_csv_as_table, \
         patch('products.display_filtered_table', side_effect=stub_display_filtered_table) as mock_display_filtered_table, \
         patch('products.checkoutAndPayment', side_effect=stub_checkoutAndPayment) as mock_checkoutAndPayment, \
         patch('builtins.input', side_effect=data_test_searchAndBuyProduct['valid_inputs']):
            main.searchAndBuyProduct()

            # Assertions to verify that the stubs were called
            mock_login.assert_called_once()
            mock_display_csv_as_table.assert_called_once_with("products.csv")
            mock_display_filtered_table.assert_called_once_with("products.csv", "1")
            mock_checkoutAndPayment.assert_called_once_with(data_test_searchAndBuyProduct['valid_login_info'])



# Integration test third level
data_test_login_existing_user_valid_password = {
    "valid_login_info": {"username": "existing_username", "wallet": 100},
    "valid_inputs": ["existing_username", "valid_password", "all", "N", "1", "Y"],
    "valid_json_users": """[{"username": "existing_username", "password": "valid_password", "wallet": 100}]"""
}

def test_login_existing_user_valid_password():
    with patch('products.display_csv_as_table', side_effect=stub_display_csv_as_table) as mock_display_csv_as_table, \
         patch('products.display_filtered_table', side_effect=stub_display_filtered_table) as mock_display_filtered_table, \
         patch('products.checkoutAndPayment', side_effect=stub_checkoutAndPayment) as mock_checkoutAndPayment, \
         patch('builtins.open', mock_open(read_data=data_test_login_existing_user_valid_password['valid_json_users'])), \
         patch('builtins.input', side_effect=data_test_login_existing_user_valid_password['valid_inputs']):
            main.searchAndBuyProduct()

            # Assertions to verify that the stubs were called
            mock_display_csv_as_table.assert_called_once_with("products.csv")
            mock_display_filtered_table.assert_called_once_with("products.csv", "1")
            mock_checkoutAndPayment.assert_called_once_with(data_test_login_existing_user_valid_password['valid_login_info'])



data_test_login_new_user = {
    "valid_login_info": {"username": "new_username", "wallet": 0},
    "valid_inputs": ["new_username", "unused_password", "Y", "valid_password", "all", "N", "1", "Y"],
    "valid_json_users": """[{"username": "existing_username", "password": "valid_password", "wallet": 100}]""",
}

def stub_check_password(password):
    return True

def stub_write_to_file(data):
    print("Writing new user to file")

def test_login_new_user():
    with patch('login.check_password', side_effect=stub_check_password) as mock_check_password, \
         patch('login.write_to_file', side_effect=stub_write_to_file) as mock_write_to_file, \
         patch('products.display_csv_as_table', side_effect=stub_display_csv_as_table) as mock_display_csv_as_table, \
         patch('products.display_filtered_table', side_effect=stub_display_filtered_table) as mock_display_filtered_table, \
         patch('products.checkoutAndPayment', side_effect=stub_checkoutAndPayment) as mock_checkoutAndPayment, \
         patch('builtins.open', mock_open(read_data=data_test_login_new_user['valid_json_users'])), \
         patch('builtins.input', side_effect=data_test_login_new_user['valid_inputs']):
            main.searchAndBuyProduct()

            # Assertions to verify that the stubs were called
            mock_check_password.assert_called_once_with("valid_password")
            mock_write_to_file.assert_called_once()
            mock_display_csv_as_table.assert_called_once_with("products.csv")
            mock_display_filtered_table.assert_called_once_with("products.csv", "1")
            mock_checkoutAndPayment.assert_called_once_with(data_test_login_new_user['valid_login_info'])

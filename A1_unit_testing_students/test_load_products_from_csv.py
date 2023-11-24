import pytest
from checkout_and_payment import load_products_from_csv, checkout, check_cart
from unittest.mock import patch


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


def test_load_products_from_csv_optimal(
    csv_file_optimal_state, csv_name, csv_units, csv_price
):
    # Test the load function for optimal csv data
    loaded = load_products_from_csv(csv_file_optimal_state)
    for i, v in enumerate(loaded):
        assert v.name == csv_name[i]
        assert v.units == csv_units[i]
        assert v.price == csv_price[i]


def test_load_products_from_csv_body_less(csv_file_body_less_state):
    # Test the load function for body_less csv data
    loaded = load_products_from_csv(csv_file_body_less_state)
    assert loaded == []


def test_load_products_from_csv_head_less(csv_file_head_less_state):
    # Test the load function for head_less csv data
    with pytest.raises(KeyError):
        load_products_from_csv(csv_file_head_less_state)


def test_load_products_from_csv_edge(
    csv_file_optimal_state, csv_name, csv_units, csv_price
):
    # Test the load function for optimal csv data, checking edge cases.
    loaded = load_products_from_csv(csv_file_optimal_state)
    assert loaded[0].name == csv_name[0]
    assert loaded[0].units == csv_units[0]
    assert loaded[0].price == csv_price[0]
    assert loaded[len(loaded) - 1].units == csv_units[len(csv_units) - 1]
    assert loaded[len(loaded) - 1].price == csv_price[len(csv_units) - 1]
    assert loaded[len(loaded) - 1].name == csv_name[len(csv_units) - 1]


def test_load_products_from_csv_non_existent_file(csv_file_non_existent_state):
    # Test the load function for head_less csv data
    with pytest.raises(FileNotFoundError):
        load_products_from_csv(csv_file_non_existent_state)


def test_load_products_from_csv_huge_file(csv_file_huge_state):
    # Test the load function for huge csv data
    loaded = load_products_from_csv(csv_file_huge_state)
    for v in loaded:
        assert v.name == "Carrot"
        assert v.units == 2
        assert v.price == 0.5


def test_load_products_from_csv_added_head_file(
    csv_file_added_head_state, csv_name, csv_units, csv_price
):
    # Test the load function for additional column head added to csv
    loaded = load_products_from_csv(csv_file_added_head_state)
    for i, v in enumerate(loaded):
        assert v.name == csv_name[i]
        assert v.units == csv_units[i]
        assert v.price == csv_price[i]


def test_load_products_from_csv_added_column_file_1(csv_file_added_column_state_1):
    # Test the load function for additional column added at the end to csv
    with pytest.raises(ValueError):
        load_products_from_csv(csv_file_added_column_state_1)


def test_load_products_from_csv_added_column_file_2(
    csv_file_added_column_state_2, csv_name, csv_units, csv_price
):
    # Test the load function for additional column head added in the middle to csv
    loaded = load_products_from_csv(csv_file_added_column_state_2)
    for i, v in enumerate(loaded):
        assert v.name == csv_name[i]
        assert v.units == csv_units[i]
        assert v.price == csv_price[i]


def test_load_products_from_csv_added_column_file_3(
    csv_file_added_column_state_3, csv_name, csv_units, csv_price
):
    # Test the load function for additional column head added in the beginning to csv
    loaded = load_products_from_csv(csv_file_added_column_state_3)
    for i, v in enumerate(loaded):
        assert v.name == csv_name[i]
        assert v.units == csv_units[i]
        assert v.price == csv_price[i]

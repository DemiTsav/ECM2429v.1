import pytest
from datetime import datetime
from asset_management.field_validations import FieldValidations

@pytest.fixture
def field_validations():
    return FieldValidations()

def test_validate_year_valid(field_validations):
    assert field_validations.validate_year(2020) == True

def test_validate_year_invalid(field_validations):
    assert field_validations.validate_year(1800) == False
    assert field_validations.validate_year("invalid") == False

def test_validate_date_valid(field_validations):
    assert field_validations.validate_date("25-12-22") == True

def test_validate_date_invalid(field_validations):
    assert field_validations.validate_date("31-13-22") == False
    assert field_validations.validate_date("2022-12-25") == False

def test_validations_empty_field(field_validations):
    # Simulate empty field
    mock_entries = {
        "Make": lambda: "",
        "Model": lambda: "Toyota"
    }
    errors = field_validations.validations(mock_entries, 2020, "25-12-22", "31-12-22", "Tax Paid")
    assert "Make cannot be empty." in errors

def test_validations_valid_field(field_validations):
    # Simulate valid field
    mock_entries = {
        "Make": lambda: "Toyota",
        "Model": lambda: "Corolla"
    }
    errors = field_validations.validations(mock_entries, 2020, "25-12-22", "31-12-22", "Tax Paid")
    assert errors == []

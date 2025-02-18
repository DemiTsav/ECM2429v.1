import pytest
from tkinter import Tk, Entry
from asset_management.field_validations import FieldValidations

@pytest.fixture
def mock_entries():
    # Mock the tkinter entry widgets
    root = Tk()
    entry1 = Entry(root)
    entry2 = Entry(root)
    entry3 = Entry(root)
    
    entry1.insert(0, "Toyota")  # Valid input
    entry2.insert(0, "AVD34R")  # Valid input for Registration
    entry3.insert(0, "Camry")   # Valid input for Model (used for valid tests)
    
    return {
        "Make": entry1,
        "Registration": entry2,
        "Model": entry3,
        "Fuel Type": entry1,
        "Vehicle Type": entry1
    }

# Test the validations method for non-empty fields and valid characters
def test_validations_valid(mock_entries):
    validations = FieldValidations()
    
    # Inputs
    entries = mock_entries
    year = 2020
    service_date = "15-05-2025"
    tax_due_date = "15-06-2025"
    tax_status = "Tax Paid"
    
    errors = validations.validations(entries, year, service_date, tax_due_date, tax_status)
    
    assert errors is None  # No errors for valid input

# Test the validations method for empty fields
def test_validations_empty_field(mock_entries):
    validations = FieldValidations()
    
    # Making Registration field empty
    mock_entries["Registration"].delete(0, "end")
    
    entries = mock_entries
    year = 2020
    service_date = "15-05-2025"
    tax_due_date = "15-06-2025"
    tax_status = "Tax Paid"
    
    errors = validations.validations(entries, year, service_date, tax_due_date, tax_status)
    
    assert "Registration cannot be empty." in errors

# Test the validations method for invalid character input
def test_validations_invalid_character(mock_entries):
    validations = FieldValidations()
    
    # Making Model field invalid (should only contain alphabetic characters)
    mock_entries["Model"].delete(0, "end")
    mock_entries["Model"].insert(0, "@@@")  # Invalid value for Model
    
    entries = mock_entries
    year = 2020
    service_date = "15-05-2025"
    tax_due_date = "15-06-2025"
    tax_status = "Tax Paid"
    
    errors = validations.validations(entries, year, service_date, tax_due_date, tax_status)
    print(errors)
    assert "Value for Model must use characters a-z" in errors

# Test the year validation (valid year)
def test_validate_year_valid():
    validations = FieldValidations()
    assert validations.validate_year(2020) is True

# Test the year validation (invalid year)
def test_validate_year_invalid():
    validations = FieldValidations()
    assert validations.validate_year(1899) is False

# Test the date validation (valid date)
def test_validate_date_valid():
    validations = FieldValidations()
    assert validations.validate_date("15-05-2025") is True

# Test the date validation (invalid date format)
def test_validate_date_invalid_format():
    validations = FieldValidations()
    assert validations.validate_date("2025-05-15") is False

# Test the date validation (valid date but year <= 2000)
def test_validate_date_invalid_year():
    validations = FieldValidations()
    assert validations.validate_date("15-05-1999") is False

# Test the update_validations method with a valid update
def test_update_validations_valid():
    validations = FieldValidations()
    updates = {
        "Service Date": "15-05-2025",
        "Tax Due Date": "15-06-2025"
    }
    errors = validations.update_validations(updates)
    assert errors == []  # No errors for valid dates

# Test the update_validations method with invalid date updates
def test_update_validations_invalid():
    validations = FieldValidations()
    updates = {
        "Service Date": "15-05-1999",  # Invalid date year
        "Tax Due Date": "2025-06-15"   # Invalid format
    }
    errors = validations.update_validations(updates)
    assert "Date fields must be in dd-mm-yyyy format!" in errors

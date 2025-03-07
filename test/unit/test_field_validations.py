import pytest
from datetime import datetime
from asset_management.backend.field_validations import FieldValidations


@pytest.fixture
def field_validations():
    """Fixture to create an instance of FieldValidations."""
    return FieldValidations()


@pytest.fixture
def mock_entries(mocker):
    """Mock entry fields with valid values."""
    return {
        "Make": mocker.Mock(get=mocker.Mock(return_value="Toyota")),
        "Registration": mocker.Mock(get=mocker.Mock(return_value="ABC123")),
        "Model": mocker.Mock(get=mocker.Mock(return_value="Corolla")),
        "Fuel Type": mocker.Mock(get=mocker.Mock(return_value="Petrol")),
        "Vehicle Type": mocker.Mock(get=mocker.Mock(return_value="Sedan"))
    }


@pytest.mark.parametrize("year, expected", [("2020", True), ("1899", False),
                                            (str(datetime.now().year + 1),
                                             False), ("abcd", False)])
def test_validate_year(field_validations, year, expected):
    """Test the validate_year function."""
    assert field_validations.validate_year(year) == expected


@pytest.mark.parametrize("date_str, expected", [
    ("01-01-2025", True),
    ("31-12-1999", False),
    ("2025-01-01", False),
    ("32-01-2025", False),
    ("abc-def-ghij", False)
])
def test_validate_date(field_validations, date_str, expected):
    """Test the validate_date function."""
    assert field_validations.validate_date(date_str) == expected


@pytest.mark.parametrize("value, expected",
                         [("Toyota", True),
                          ("Car123", True),
                          ("Car_123", False),
                          ("Car@!", False)])
def test_validate_character_input(field_validations, value, expected):
    """Test the validate_character_input function."""
    assert field_validations.validate_character_input(value) == expected


def test_validations_success(field_validations, mock_entries):
    """Test the validations function with valid inputs."""
    errors = field_validations.validations(
        mock_entries, year="2020", service_date="01-01-2025",
        tax_due_date="01-06-2025", tax_status="Valid"
    )
    assert errors is None


def test_validations_failure(field_validations, mock_entries):
    """Test the validations function with invalid inputs."""
    mock_entries["Make"].get.return_value = ""
    errors = field_validations.validations(
        mock_entries, year="1899", service_date="2025-01-01",
        tax_due_date="32-13-2025", tax_status=None
    )
    assert len(errors) > 0
    assert "Make cannot be empty." in errors
    assert "Year must be a valid number between 1900 and the current year" \
           in errors
    assert "Service Date must be in dd-mm-yyyy format." in errors
    assert "Tax Due Date must be in dd-mm-yyyy format." in errors
    assert "Tax Status must be selected." in errors


def test_update_validations(field_validations):
    """Test update_validations function with valid and invalid dates."""
    valid_updates = {"Service Date": "01-01-2025",
                     "Tax Due Date": "15-06-2025", "Tax Status": "Tax Paid"}
    invalid_updates = {"Service Date": "2025/01/01",
                       "Tax Due Date": "invalid-date",
                       "Tax Status": "InvalidStatus"}

    assert field_validations.update_validations(valid_updates) is None
    errors = field_validations.update_validations(invalid_updates)
    assert "Service date field must be in dd-mm-yyyy format!" in errors
    assert "Tax due date field must be in dd-mm-yyyy format!" in errors
    assert "Tax Status must be one of the following: Tax Paid, Tax Due, " \
           "SORN, Exempt." in errors


def test_update_validations_tax_due_date(field_validations):
    """Test update_validations function with valid & invalid tax due dates."""
    valid_updates = {"Service Date": "01-01-2025",
                     "Tax Due Date": "N/A", "Tax Status": "SORN"}
    invalid_updates = {"Service Date": "01-01-2025",
                       "Tax Due Date": "15-06-2025", "Tax Status": "SORN"}

    assert field_validations.update_validations(valid_updates) is None
    errors = field_validations.update_validations(invalid_updates)
    assert "Tax Due Date must be 'N/A' when Tax Status is SORN or " \
           "Exempt." in errors


def test_update_validations_tax_status(field_validations):
    """Test update_validations function with valid and invalid tax statuses."""
    invalid_tax_date_updates = {"Service Date": "01-01-2025",
                                "Tax Due Date": "15-06-2025",
                                "Tax Status": "Exempt"}
    invalid_updates = {"Service Date": "01-01-2025",
                       "Tax Due Date": "15-06-2025",
                       "Tax Status": "InvalidStatus"}

    tax_due_date_error = field_validations.update_validations(
        invalid_tax_date_updates)
    assert "Tax Due Date must be 'N/A'" in tax_due_date_error[0]
    tax_status_errors = field_validations.update_validations(invalid_updates)
    assert "Tax Status must be one of the following" in tax_status_errors[0]

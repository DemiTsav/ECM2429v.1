import pytest
from unittest.mock import MagicMock
from asset_management.asset_management_page import AssetManagementPage
from vehicle_management_task.database import VehicleDatabase
import tkinter as tk


@pytest.fixture
def mock_db():
    """Fixture to mock the VehicleDatabase."""
    mock_db = MagicMock(spec=VehicleDatabase)
    return mock_db


def test_show_all_vehicles(mock_db):
    """Test to verify that all vehicles are displayed correctly in the table."""
    app = AssetManagementPage(parent=tk.Tk(), db=mock_db)

    # Mock the return value to ensure vehicle ID is a string (consistency in type)
    mock_db.get_all_vehicles.return_value = [
        ("1", "Toyota", "Camry", "2020", "Sedan", "Gas", "2020-05-01", "2022-05-01", "Tax Paid")
    ]

    app.show_all_vehicles()

    # Check that the table has been populated with the correct values
    children = app.vehicle_table.get_children()
    assert len(children) == 1  # One vehicle
    assert app.vehicle_table.item(children[0])['values'] == (
        "1", "Toyota", "Camry", "2020", "Sedan", "Gas", "2020-05-01", "2022-05-01", "Tax Paid"
    )

def test_process_add_vehicle(self):
    # Create a mock for the db object
    mock_db = MagicMock()
    app = AssetManagementPage(self.parent, mock_db)

    # Setup mock behavior
    mock_db.add_vehicle.return_value = None  # Mock the response to avoid actual DB interaction

    # Simulate adding a vehicle
    app.show_add_vehicle_form()
    app._process_add_vehicle({
        'Make': 'Toyota',
        'Model': 'Camry',
        'Year': '2020',
        'Vehicle Type': 'Sedan',
        'Fuel Type': 'Gas',
        'Service Date': '2020-05-01',
        'Tax Due Date': '2022-05-01',
    }, 'Tax Paid')

    # Check that add_vehicle was called once
    mock_db.add_vehicle.assert_called_once_with('Toyota', 'Camry', 2020, 'Sedan', 'Gas', '2020-05-01', '2022-05-01', 'Tax Paid')

def test_show_update_vehicle_form(mock_db):
    """Test to ensure the vehicle update form is displayed correctly."""
    app = AssetManagementPage(parent=tk.Tk(), db=mock_db)

    # Mock vehicle data to simulate retrieving a vehicle for update
    mock_db.get_vehicle.return_value = {
        "ID": "1",
        "Make": "Toyota",
        "Model": "Camry",
        "Year": "2020",
        "Vehicle Type": "Sedan",
        "Fuel Type": "Gas",
        "Service Date": "2020-05-01",
        "Tax Due Date": "2022-05-01",
        "Tax Status": "Tax Paid"
    }

    # Show the update vehicle form
    app.show_update_vehicle_form()

    # Check that update_entries is initialized correctly
    assert hasattr(app, 'update_entries')
    assert isinstance(app.update_entries, dict)  # Should be a dictionary

    # Check that the UI has been populated with the correct vehicle data
    assert app.update_entries["Make"].get() == "Toyota"
    assert app.update_entries["Model"].get() == "Camry"


def test_show_add_vehicle_form(mock_db):
    """Test to check that the Add Vehicle form is displayed correctly."""
    app = AssetManagementPage(parent=tk.Tk(), db=mock_db)

    # Show the add vehicle form
    app.show_add_vehicle_form()

    # Check that the dynamic content is cleared and a new form is created
    assert len(app.dynamic_content_frame.winfo_children()) > 0  # Should contain form elements

    # Ensure the form fields are properly initialized
    assert isinstance(app.entries, dict)
    assert 'Make' in app.entries
    assert 'Model' in app.entries


def test_delete_vehicle_prompt(mock_db):
    """Test to ensure that the delete vehicle prompt is displayed correctly."""
    app = AssetManagementPage(parent=tk.Tk(), db=mock_db)

    # Mocking vehicle data for testing
    mock_db.get_all_vehicles.return_value = [
        ("1", "Toyota", "Camry", "2020", "Sedan", "Gas", "2020-05-01", "2022-05-01", "Tax Paid")
    ]

    # Show delete vehicle prompt
    app.delete_vehicle_prompt()

    # Ensure the dynamic content is cleared and delete buttons are created
    assert len(app.dynamic_content_frame.winfo_children()) > 0
    assert any("Delete" in button.cget("text") for button in app.dynamic_content_frame.winfo_children())


def test_confirm_deletion(mock_db):
    """Test the confirmation of vehicle deletion."""
    app = AssetManagementPage(parent=tk.Tk(), db=mock_db)

    # Mock the selection of a vehicle to delete
    app.vehicle_table.selection = MagicMock(return_value=["1"])

    # Simulate user confirming deletion
    app.confirm_deletion()

    # Check that the delete method was called with the correct vehicle ID
    mock_db.delete_vehicle.assert_called_once_with("1")

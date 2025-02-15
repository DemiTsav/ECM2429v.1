import pytest
from unittest.mock import MagicMock
from asset_management.asset_management_page import AssetManagementPage
from vehicle_management_task.database import VehicleDatabase
import tkinter as tk
from tkinter import ttk


@pytest.fixture
def mock_db():
    """Fixture to mock the VehicleDatabase."""
    mock_db = MagicMock(spec=VehicleDatabase)
    # Simulate a single vehicle in the database
    mock_db.get_all_vehicles.return_value = [
        (1, "Honda", "Civic", 2021, "Car", "Petrol", "2025-01-01", "2025-06-01", "Tax Paid")
    ]
    return mock_db


@pytest.fixture
def asset_management_page(mock_db):
    """Fixture to create the AssetManagementPage instance."""
    root = tk.Tk()
    page = AssetManagementPage(root, mock_db)
    return page


def test_show_all_vehicles(asset_management_page, mock_db):
    """Test that all vehicles are shown correctly."""
    # Simulate adding a vehicle
    asset_management_page.show_all_vehicles()
    children = asset_management_page.vehicle_table.get_children()
    
    # Check that there is only 1 vehicle shown
    assert len(children) == 1  # Ensure one vehicle is present
    assert children[0] == ("1", "Honda", "Civic", 2021, "Car", "Petrol", "2025-01-01", "2025-06-01", "Tax Paid")


def test_process_add_vehicle(asset_management_page, mock_db):
    """Test that a new vehicle is added successfully."""
    # Mock the tk.Entry widgets
    make_entry = MagicMock(spec=tk.Entry)
    model_entry = MagicMock(spec=tk.Entry)
    year_entry = MagicMock(spec=tk.Entry)
    
    make_entry.get.return_value = "Honda"
    model_entry.get.return_value = "Civic"
    year_entry.get.return_value = "2021"
    
    entries = {
        "Make": make_entry,
        "Model": model_entry,
        "Year": year_entry
    }
    
    # Simulate adding a new vehicle
    asset_management_page.process_add_vehicle(entries, "Tax Paid")
    
    # Check that the add_vehicle method was called with correct parameters
    mock_db.add_vehicle.assert_called_once_with(
        "Honda", "Civic", "2021", "Car", "Petrol", "2025-01-01", "2025-06-01", "Tax Paid"
    )


def test_show_update_vehicle_form_no_selection(asset_management_page):
    """Test the behavior when no vehicle is selected to update."""
    # Simulate no vehicle selected
    asset_management_page.vehicle_table.selection = []
    
    # Check if the form doesn't display for no selection
    asset_management_page.show_update_vehicle_form()
    
    # Assert that the update form was not called (no selection)
    assert not asset_management_page.update_form_is_shown()


def test_delete_vehicle_prompt_no_selection(asset_management_page):
    """Test the behavior when no vehicle is selected for deletion."""
    # Simulate no vehicle selected
    asset_management_page.vehicle_table.selection = []
    
    # Check if the delete prompt doesn't show for no selection
    asset_management_page.delete_vehicle_prompt()
    
    # Assert that the delete confirmation was not triggered
    assert not asset_management_page.delete_vehicle_called()


def test_show_search_form():
    """Test the search form (mocking Tkinter)."""
    try:
        root = tk.Tk()
        search_form = AssetManagementPage(root, MagicMock(spec=VehicleDatabase))
        search_form.show_search_form()
    except Exception as e:
        pytest.fail(f"Failed to display search form due to: {e}")

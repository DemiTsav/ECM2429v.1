import pytest
import tkinter as tk
from tkinter import ttk
from asset_management.ui_components import UIComponents

# Mock classes for vehicle_process and vehicle_table
class MockVehicleProcess:
    pass  # Implement any necessary methods or attributes here

class MockVehicleTable:
    def __init__(self):
        self.selected_item = None
        self.children = []

    def selection(self):
        # Simulate returning selected items
        return [self.selected_item] if self.selected_item else []

    def get_children(self):
        # Simulate getting all children (rows in the table)
        return self.children

    def delete(self, item_id):
        # Simulate deletion of a row
        if item_id in self.children:
            self.children.remove(item_id)

    def insert(self, parent, index, values):
        # Simulate inserting a new row
        self.children.append(values)

    def item(self, item_id, option=None):
        # Simulate getting an item (used in confirm_deletion)
        return {"values": self.children[0]} if self.children else {}

class MockEntries:
    def __init__(self):
        self.entries = {}

    def add_entry(self, field, entry_widget):
        self.entries[field] = {"entry": entry_widget}

# Fixtures
@pytest.fixture
def mock_db(monkeypatch):
    """Fixture to mock the database operations."""

    # Mock the get_vehicle method
    def mock_get_vehicle(vehicle_id):
        return ("1", "ABC123", "Toyota", "Camry", 2020, "Sedan", "Petrol", "15-05-2025", "15-06-2025", "Tax Paid")
    
    # Mock the update_vehicle method
    def mock_update_vehicle(vehicle_id, data):
        return None

    # Mock the delete_vehicle method
    def mock_delete_vehicle(vehicle_id):
        return None

    # Mock the query_vehicles method
    def mock_query_vehicles():
        return [("1", "ABC123", "Toyota", "Camry", 2020, "Sedan", "Petrol", "15-05-2025", "15-06-2025", "Tax Paid")]

    # Patch the methods directly on the db object
    monkeypatch.setattr("vehicle_management_task.database.VehicleDatabase.get_vehicle", mock_get_vehicle)
    monkeypatch.setattr("vehicle_management_task.database.VehicleDatabase.update_vehicle", mock_update_vehicle)
    monkeypatch.setattr("vehicle_management_task.database.VehicleDatabase.delete_vehicle", mock_delete_vehicle)
    monkeypatch.setattr("vehicle_management_task.database.VehicleDatabase.query_vehicles", mock_query_vehicles)
    
    return mock_get_vehicle


@pytest.fixture
def mock_ui_components(mock_db, monkeypatch):
    """Fixture to mock the UIComponents class."""
    
    # Mock tkinter components to avoid actual GUI rendering
    monkeypatch.setattr(tk, "Frame", lambda *args, **kwargs: tk.Frame())  # Mock Frame
    monkeypatch.setattr(ttk, "Treeview", lambda *args, **kwargs: ttk.Treeview())  # Mock Treeview

    # Create mock vehicle_process and vehicle_table for UIComponents
    mock_vehicle_process = MockVehicleProcess()
    mock_vehicle_table = MockVehicleTable()
    mock_entries = MockEntries()

    # Create a mocked UIComponents instance with the required arguments
    ui_components = UIComponents(mock_db, mock_vehicle_process, mock_vehicle_table)
    ui_components.entries = mock_entries.entries  # Mock the entries attribute

    return ui_components


def test_create_button(mock_ui_components):
    """Test create_button method."""
    parent_frame = tk.Frame()
    text = "Test Button"
    command = lambda: None
    padx = 10

    # Call create_button to generate a button
    button = mock_ui_components.create_button(parent_frame, text, command, padx)

    # Assert the button was created correctly
    assert isinstance(button, tk.Button)


def test_create_dropdown(mock_ui_components):
    """Test create_dropdown method."""
    parent_frame = tk.Frame()
    field = "Fuel Type"
    values = ["Petrol", "Diesel", "Electric"]
    default_value = "Petrol"

    # Call create_dropdown to generate a dropdown
    dropdown = mock_ui_components.create_dropdown(parent_frame, field, values, default_value)

    # Assert the dropdown was created and the default value is set
    assert isinstance(dropdown, ttk.Combobox)
    dropdown.set.assert_called_once_with(default_value)


def test_create_checkbox(mock_ui_components):
    """Test create_checkbox method."""
    field = "Insurance Paid"
    default_value = True

    # Call create_checkbox to generate a checkbox
    var, checkbox = mock_ui_components.create_checkbox(field, default_value)

    # Assert the checkbox and variable were created
    assert isinstance(var, tk.BooleanVar)
    assert isinstance(checkbox, tk.Checkbutton)


def test_create_text_entry(mock_ui_components):
    """Test create_text_entry method."""
    field = "Vehicle Make"
    default_value = "Toyota"
    state = "normal"

    # Call create_text_entry to generate a text entry field
    entry = mock_ui_components.create_text_entry(field, default_value, state)

    # Assert the entry field was created and initialized with the default value
    assert isinstance(entry, tk.Entry)
    entry.insert.assert_called_once_with(0, default_value)
    entry.config.assert_called_once_with(state=state)


def test_enable_delete_button(mock_ui_components):
    """Test enable_delete_button method."""
    delete_button = tk.Button()
    vehicle_table = mock_ui_components.vehicle_table
    vehicle_table.selected_item = "1"

    # Call enable_delete_button to check if delete button gets enabled
    selected_items = mock_ui_components.enable_delete_button(delete_button)

    delete_button.config.assert_called_once_with(state="normal")
    assert selected_items == ["1"]


def test_update_vehicle_table(mock_ui_components):
    """Test update_vehicle_table method."""
    vehicles = [("1", "ABC123", "Toyota", "Camry", 2020, "Sedan", "Petrol", "15-05-2025", "15-06-2025", "Tax Paid")]

    # Call update_vehicle_table to check if the table is updated
    mock_ui_components.update_vehicle_table(vehicles)

    # Assert that the table was cleared and updated with new data
    mock_ui_components.vehicle_table.delete.assert_called()
    mock_ui_components.vehicle_table.insert.assert_called_with("", tk.END, values=vehicles[0])


def test_clear_form_fields(mock_ui_components):
    """Test clear_form_fields method."""
    mock_ui_components.clear_form_fields()

    # Assert that form fields are cleared
    for entry in mock_ui_components.entries.values():
        entry['entry'].delete.assert_called_once_with(0, tk.END)


def test_confirm_deletion(mock_ui_components, mock_db):
    """Test confirm_deletion method."""
    delete_button = tk.Button()
    vehicle_table = mock_ui_components.vehicle_table
    vehicle_table.selected_item = "1"
    vehicle_table.children = [("1", "ABC123", "Toyota", "Camry", 2020)]

    # Call confirm_deletion to verify deletion logic
    mock_ui_components.confirm_deletion(delete_button)

    vehicle_table.item.assert_called_with("1", "values")
    vehicle_table.delete.assert_called_once_with("1")

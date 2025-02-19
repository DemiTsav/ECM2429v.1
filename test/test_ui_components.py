import pytest
import tkinter as tk
from tkinter import ttk
from asset_management.ui_components import UIComponents  # Adjust import as needed

@pytest.fixture
def root():
    return tk.Tk()

@pytest.fixture
def dynamic_content_frame(root):
    return tk.Frame(root)

@pytest.fixture
def vehicle_table(root):
    return ttk.Treeview(root, columns=("ID", "Name"))

@pytest.fixture
def vehicle_process():
    return {}  # Mock vehicle process (can be replaced with an actual mock)

@pytest.fixture
def ui_components(dynamic_content_frame, vehicle_process, vehicle_table):
    return UIComponents(dynamic_content_frame, vehicle_process, vehicle_table)

# Test create_button

def test_create_button(ui_components):
    parent = tk.Frame()
    command_called = []
    
    def sample_command():
        command_called.append(True)
    
    button = ui_components.create_button(parent, "Click Me", sample_command, padx=5)
    assert isinstance(button, tk.Button)
    assert button.cget("text") == "Click Me"
    button.invoke()
    assert command_called == [True]

# Test create_dropdown

def test_create_dropdown(ui_components):
    parent = tk.Frame()
    dropdown = ui_components.create_dropdown(parent, "Options", ["A", "B"], "A")
    assert isinstance(dropdown, ttk.Combobox)
    assert dropdown.get() == "A"
    assert "A" in dropdown["values"]

# Test create_checkbox

def test_create_checkbox(ui_components):
    var, checkbox = ui_components.create_checkbox("Test Checkbox")
    assert isinstance(var, tk.BooleanVar)
    assert isinstance(checkbox, tk.Checkbutton)
    assert var.get() is False
    var.set(True)
    assert var.get() is True

# Test create_text_entry

def test_create_text_entry(ui_components):
    entry = ui_components.create_text_entry("Test Field", "Default")
    assert isinstance(entry, tk.Entry)
    assert entry.get() == "Default"

# Test toggle_entry_state

def test_toggle_entry_state(ui_components):
    var = tk.BooleanVar(value=False)
    entry = ui_components.create_text_entry("Field")
    ui_components.toggle_entry_state(var, entry)
    assert entry.cget("state") == "disabled"
    var.set(True)
    ui_components.toggle_entry_state(var, entry)
    assert entry.cget("state") == "readonly"

# Test clear_dynamic_content

def test_clear_dynamic_content(ui_components):
    label = tk.Label(ui_components.dynamic_content_frame, text="Test")
    label.pack()
    assert len(ui_components.dynamic_content_frame.winfo_children()) > 0
    ui_components.clear_dynamic_content()
    assert len(ui_components.dynamic_content_frame.winfo_children()) == 0

# Test update_vehicle_table using monkeypatch

def test_update_vehicle_table(ui_components, monkeypatch):
    monkeypatch.setattr(ui_components.vehicle_table, "get_children", lambda: ["item1", "item2"])
    monkeypatch.setattr(ui_components.vehicle_table, "delete", lambda item: None)
    monkeypatch.setattr(ui_components.vehicle_table, "insert", lambda *args, **kwargs: None)
    
    ui_components.update_vehicle_table([(1, "Car"), (2, "Truck")])
    
    assert True  # No exceptions raised

# Test confirm_deletion with mock selection

def test_confirm_deletion(mocker):
    root = tk.Tk()
    frame = tk.Frame(root)
    table = ttk.Treeview(frame, columns=("ID", "Name"))
    table.pack()

    # Insert a test row
    test_item_id = table.insert("", "end", values=("123", "Test Vehicle"))

    # Ensure the item is selected
    table.selection_set(test_item_id)  # <-- This ensures selection is not empty

    # Mock database with a test vehicle
    mock_db = mocker.Mock()
    mock_db.get_vehicle.return_value = {"ID": "123", "Name": "Test Vehicle"}

    # Create UIComponents instance
    ui_components = UIComponents(frame, mock_db, table)

    # Mock delete button
    delete_button = tk.Button(frame)

    # Call confirm_deletion (should not crash)
    ui_components.confirm_deletion(delete_button)

    assert mock_db.get_vehicle.called  # Ensure database lookup happened

import pytest
import tkinter as tk
from tkinter import ttk
from asset_management.frontend.ui_components import UIComponents


@pytest.fixture
def root():
    """Fixture to create and return a Tkinter root window."""
    return tk.Tk()


@pytest.fixture
def dynamic_content_frame(root):
    """Fixture to create and return a Tkinter Frame for dynamic content."""
    return tk.Frame(root)


@pytest.fixture
def vehicle_table():
    """Fixture to create and return a Treeview widget representing a vehicle
    table."""
    return ttk.Treeview()


@pytest.fixture
def ui_components(dynamic_content_frame, vehicle_table):
    """Fixture to create and return an instance of UIComponents."""
    return UIComponents(dynamic_content_frame, None, vehicle_table)


def test_create_button(ui_components):
    """Test if create_button() creates a valid Tkinter Button with the correct
    label."""
    parent = tk.Frame()
    button = ui_components.create_button(parent, "Click Me", lambda: None, 5)
    assert isinstance(button, tk.Button)
    assert button["text"] == "Click Me"


def test_create_dropdown(ui_components):
    """Test if create_dropdown() creates a valid Tkinter Combobox with default
    selection."""
    parent = tk.Frame()
    dropdown = ui_components.create_dropdown(parent, "Test Field",
                                             ["Option1", "Option2"],
                                             "Option1")
    assert isinstance(dropdown, ttk.Combobox)
    assert dropdown.get() == "Option1"


def test_create_checkbox(ui_components):
    """Test if create_checkbox() returns a valid Checkbutton and BooleanVar."""
    var, checkbox = ui_components.create_checkbox("Test Checkbox")
    assert isinstance(checkbox, tk.Checkbutton)
    assert isinstance(var, tk.BooleanVar)


def test_create_text_entry(ui_components):
    """Test if create_text_entry() creates a valid Tkinter Entry with default
    text."""
    entry = ui_components.create_text_entry("Test Entry", "Default Text")
    assert isinstance(entry, tk.Entry)
    assert entry.get() == "Default Text"


def test_toggle_entry_state(ui_components, mocker):
    """Test if toggle_entry_state() correctly enables/disables an entry field
    based on a checkbox state."""
    var = tk.BooleanVar(value=False)
    entry = tk.Entry()
    mocker.patch.object(entry, "config")
    ui_components.toggle_entry_state(var, entry)
    entry.config.assert_called_with(state="disabled")
    var.set(True)
    ui_components.toggle_entry_state(var, entry)
    entry.config.assert_called_with(state="readonly")


def test_clear_dynamic_content(ui_components, dynamic_content_frame):
    """Test if clear_dynamic_content() removes all child widgets from the
    dynamic content frame."""
    tk.Label(dynamic_content_frame, text="Test").pack()
    assert len(dynamic_content_frame.winfo_children()) > 0
    ui_components.clear_dynamic_content()
    assert len(dynamic_content_frame.winfo_children()) == 0


def test_enable_delete_button(ui_components, mocker):
    """Test if enable_delete_button() enables/disables the delete button based
    on row selection."""
    delete_button = mocker.Mock()
    ui_components.vehicle_table.selection = mocker.Mock(return_value=["item1"])
    selected = ui_components.enable_delete_button(delete_button)
    assert selected == ["item1"]
    delete_button.config.assert_called_with(state="normal")

    ui_components.vehicle_table.selection = mocker.Mock(return_value=[])
    selected = ui_components.enable_delete_button(delete_button)
    assert selected is None
    delete_button.config.assert_called_with(state="disabled")


def test_update_vehicle_table(ui_components, mocker):
    """Test if update_vehicle_table() correctly updates the Treeview with new
    vehicle data."""
    mocker.patch.object(ui_components.vehicle_table, "insert")
    mocker.patch.object(ui_components.vehicle_table, "delete")
    ui_components.update_vehicle_table([
        (1, "ABC123", "Toyota", "Corolla", 2020)
        ])
    ui_components.vehicle_table.insert.assert_called()


def test_display_message(ui_components):
    """Test if display_message() correctly displays a label with the specified
    text and color."""
    ui_components.display_message("Test Message", "red")
    labels = [
        w for w in ui_components.dynamic_content_frame.winfo_children()
        if isinstance(w, tk.Label)
    ]
    assert any(label["text"] == "Test Message" for label in labels)
    assert any(label["fg"] == "red" for label in labels)


def test_checkbox_updates(ui_components, mocker):
    """Test if checkbox_updates() correctly creates a checkbox and entry field,
    and toggles their states."""
    vehicle_info = {"Tax Due Date": "2025-05-01", "Fuel Type": "Petrol"}
    ui_components.checkbox_updates("Tax Due Date", vehicle_info)
    field_frame = ui_components.dynamic_content_frame.winfo_children()[0]
    checkbox = field_frame.winfo_children()[0]
    entry = field_frame.winfo_children()[2]

    mock_var = mocker.MagicMock()
    mock_var.get.return_value = 0

    checkbox.configure(variable=mock_var)

    ui_components.toggle_entry_state(mock_var, entry)
    assert entry["state"] == "disabled"

    mock_var.get.return_value = 1
    ui_components.toggle_entry_state(mock_var, entry)
    assert entry["state"] == "readonly"

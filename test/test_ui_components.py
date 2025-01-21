import pytest
import tkinter as tk
from asset_management.ui_components import UIComponents

@pytest.fixture
def ui_components():
    root = tk.Tk()
    dynamic_content_frame = tk.Frame(root)
    return UIComponents(dynamic_content_frame, None, None)

def test_create_button(ui_components):
    button = ui_components.create_button(ui_components.dynamic_content_frame, "Click Me", lambda: print("Clicked"), 5)
    assert isinstance(button, tk.Button)
    assert button.cget("text") == "Click Me"

def test_create_dropdown(ui_components):
    dropdown = ui_components.create_dropdown(ui_components.dynamic_content_frame, "Test", ["Option 1", "Option 2"], "Option 1")
    assert isinstance(dropdown, tk.Combobox)
    assert dropdown.get() == "Option 1"

def test_create_text_entry(ui_components):
    entry = ui_components.create_text_entry("Field Name", "Default Text")
    assert isinstance(entry, tk.Entry)
    assert entry.get() == "Default Text"

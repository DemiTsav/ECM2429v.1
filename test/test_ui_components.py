import unittest
from unittest.mock import Mock, MagicMock
import tkinter as tk
from tkinter import ttk
from asset_management.ui_components import UIComponents


class TestUIComponents(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.dynamic_content_frame = tk.Frame(self.root)
        self.vehicle_process = Mock()
        self.vehicle_table = ttk.Treeview(self.root)
        self.ui_components = UIComponents(
            self.dynamic_content_frame, self.vehicle_process, self.vehicle_table
        )

    def tearDown(self):
        self.root.destroy()

    def test_create_button(self):
        command = Mock()
        button = self.ui_components.create_button(
            self.dynamic_content_frame, "Test Button", command, 5
        )
        self.assertIsInstance(button, tk.Button)
        self.assertEqual(button["text"], "Test Button")
        button.invoke()
        command.assert_called_once()

    def test_create_dropdown(self):
        values = ["Option 1", "Option 2"]
        dropdown = self.ui_components.create_dropdown(
            self.dynamic_content_frame, "Test Dropdown", values, "Option 1"
        )
        self.assertIsInstance(dropdown, ttk.Combobox)
        self.assertEqual(dropdown.get(), "Option 1")
        self.assertEqual(list(dropdown["values"]), values)


    def test_create_checkbox(self):
        var, checkbox = self.ui_components.create_checkbox("Test Checkbox", True)
        self.assertIsInstance(checkbox, tk.Checkbutton)
        self.assertTrue(var.get())

    def test_create_text_entry(self):
        entry = self.ui_components.create_text_entry("Test Entry", "Default Text")
        self.assertIsInstance(entry, tk.Entry)
        self.assertEqual(entry.get(), "Default Text")

    def test_toggle_entry_state(self):
        var = tk.BooleanVar(value=True)
        entry = tk.Entry(self.dynamic_content_frame)
        entry.pack()
        self.ui_components.toggle_entry_state(var, entry)
        self.assertEqual(str(entry["state"]), "readonly")

        var.set(False)
        self.ui_components.toggle_entry_state(var, entry)
        self.assertEqual(str(entry["state"]), "disabled")

    def test_checkbox_updates(self):
        vehicle_info = {"Test Field": "Test Value"}
        self.ui_components.checkbox_updates("Test Field", vehicle_info)
        self.assertIn("test_field", self.ui_components.update_entries)
        entry = self.ui_components.update_entries["test_field"]["entry"]
        self.assertEqual(entry.get(), "Test Value")

    def test_create_update_fields(self):
        vehicle_info = {"Test Field": "Test Value"}
        var, checkbox, entry = self.ui_components.create_update_fields(
            "Test Field", vehicle_info
        )
        self.assertIn("Test Field", self.ui_components.update_entries)
        self.assertEqual(entry.get(), "Test Value")

    def test_display_message(self):
        self.ui_components.display_message("Test Message", "blue")
        label = self.dynamic_content_frame.winfo_children()[-1]
        self.assertIsInstance(label, tk.Label)
        self.assertEqual(label["text"], "Test Message")
        self.assertEqual(label["fg"], "blue")

    def test_enable_delete_button(self):
        delete_button = tk.Button(self.root)
        self.vehicle_table.selection = Mock(return_value=["item1"])

        selected_items = self.ui_components.enable_delete_button(delete_button)
        self.assertEqual(delete_button["state"], "normal")
        self.assertEqual(selected_items, ["item1"])

        self.vehicle_table.selection = Mock(return_value=[])
        self.ui_components.enable_delete_button(delete_button)
        self.assertEqual(delete_button["state"], "disabled")

    def test_update_vehicle_table(self):
        vehicles = [("1", "Car", "2025"), ("2", "Truck", "2026")]
        self.ui_components.update_vehicle_table(vehicles)
        children = self.vehicle_table.get_children()
        self.assertEqual(len(children), 2)
        for i, vehicle in enumerate(vehicles):
            self.assertEqual(
                list(map(str, self.vehicle_table.item(children[i])["values"])),
                list(map(str, vehicle))
            )

    def test_clear_dynamic_content(self):
        tk.Label(self.dynamic_content_frame, text="Test").pack()
        self.ui_components.clear_dynamic_content()
        self.assertEqual(len(self.dynamic_content_frame.winfo_children()), 0)

if __name__ == "__main__":
    unittest.main()

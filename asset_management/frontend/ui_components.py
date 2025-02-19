import tkinter as tk
from tkinter import ttk
from typing import Dict, Tuple, List, Optional, Any


class UIComponents:
    """
    A class for managing and creating UI components
    """

    def __init__(
            self, dynamic_content_frame: tk.Frame, vehicle_process: Any,
            vehicle_table: ttk.Treeview):

        """
        Initialize the UIComponents class.

        Args:
            dynamic_content_frame (tk.Frame): The frame for dynamic content.
            vehicle_process (Any): The process handling vehicle-related logic.
            vehicle_table (ttk.Treeview): The table displaying vehicle data.
        """

        self.dynamic_content_frame: tk.Frame = dynamic_content_frame
        self.vehicle_process: Any = vehicle_process
        self.vehicle_table: ttk.Treeview = vehicle_table
        self.update_entries: Dict[str, Dict[str, Any]] = {}

    def create_button(
            self, parent_frame: tk.Frame, text: str, command: Any, padx: int
            ) -> tk.Button:

        """
        Create a button and add it to a parent frame.

        Args:
            parent_frame (tk.Frame): The frame to which the button will
            be added.
            text (str): The text displayed on the button.
            command (Any): The function to execute when the button is clicked.
            padx (int): The horizontal padding around the button.

        Returns:
            tk.Button: The created button.
        """

        button = tk.Button(parent_frame, text=text, command=command)
        button.pack(side="left", padx=padx)
        return button

    def create_dropdown(
        self, parent_frame: tk.Frame, field: str, values: List[str],
        default_value: str, state: str = "normal"
    ) -> ttk.Combobox:

        """
        Create a dropdown (combobox) and return it.

        Args:
            parent_frame (tk.Frame): The frame to add the dropdown to
            field (str): The label for the dropdown field.
            values (List[str]): The list of dropdown options.
            default_value (str): The default value for the dropdown.
            state (str, optional): The dropdown state ('normal'/'disabled')

        Returns:
            ttk.Combobox: The created dropdown.
        """

        frame = tk.Frame(parent_frame)
        frame.pack(fill="x", pady=2)

        label = tk.Label(frame, text=field)
        label.pack(side="left")

        dropdown = ttk.Combobox(frame, values=values, state=state)
        dropdown.set(default_value)
        dropdown.pack(side="left", fill="x", expand=True)

        return dropdown

    def create_checkbox(
            self, field: str, default_value: bool = False
    ) -> Tuple[tk.BooleanVar, tk.Checkbutton]:

        """
        Create a checkbox for a field.

        Args:
            field (str): The label for the checkbox field.
            default_value (bool, optional): The initial state of the checkbox.

        Returns:
            Tuple[tk.BooleanVar, tk.Checkbutton]: Tuple containing the variable
            associated with the checkbox and the checkbox widget.
        """

        field_frame = tk.Frame(self.dynamic_content_frame)
        field_frame.pack(fill="x", pady=2)

        var = tk.BooleanVar(value=default_value)
        checkbox = tk.Checkbutton(field_frame, variable=var)
        checkbox.pack(side="left")

        tk.Label(field_frame, text=field).pack(side="left")

        return var, checkbox

    def create_text_entry(
            self, field: str, default_value: str = "", state: str = "normal"
            ) -> tk.Entry:

        """
        Create a text entry field and return it.

        Args:
            field (str): The label for the text entry field.
            default_value (str, optional): The default text for the entry.
            state (str, optional): The state of the entry ('normal'/'disabled')

        Returns:
            tk.Entry: The created text entry field.
        """

        field_frame = tk.Frame(self.dynamic_content_frame)
        field_frame.pack(fill="x", pady=2)

        tk.Label(field_frame, text=field).pack(side="left")

        entry = tk.Entry(field_frame)
        entry.insert(0, default_value)
        entry.config(state=state)
        entry.pack(side="left", fill="x", expand=True)

        return entry

    def toggle_entry_state(
            self, checkbox_var: tk.BooleanVar, entry: tk.Entry
            ) -> None:

        """
        Toggle the state of an entry field based on the checkbox's state.

        Args:
            checkbox_var (tk.BooleanVar): The variable associated with
            the checkbox.
            entry (tk.Entry): The entry field to enable/disable.
        """

        state = "readonly" if checkbox_var.get() else "disabled"
        entry.config(state=state)

    def checkbox_updates(
            self, field: str, vehicle_info: Dict[str, str]
            ) -> None:

        """
        Create checkboxes and entry fields for vehicle updates.
        """

        field_frame = tk.Frame(self.dynamic_content_frame)
        field_frame.pack(fill="x", pady=2)

        var = tk.BooleanVar(value=False)
        checkbox = tk.Checkbutton(field_frame, variable=var)
        checkbox.pack(side="left")

        tk.Label(field_frame, text=field).pack(side="left")

        entry = tk.Entry(field_frame)
        entry.pack(side="left", fill="x", expand=True)
        entry.insert(0, vehicle_info.get(field, ""))
        entry.config(state="disabled")  # Initially disabled

        def toggle_entry_state(*args, var=var, entry=entry):
            entry.config(state="normal" if var.get() else "disabled")

        var.trace_add("write", lambda *args: toggle_entry_state(var, entry))

        # Adjusting field names
        if field in ["Tax Due Date", "Fuel Type", "Service Date"]:
            field = field.replace(" ", "_").lower()
        elif field == "Vehicle Type":
            field = "vehicle_type"
        formatted_field = field.replace(" ", "_").lower()
        self.update_entries[formatted_field] = {"checkbox": var, "entry": entry}


        entry.config(state="normal")
        self.update_entries[field] = {"checkbox": var, "entry": entry}

    def create_update_fields(
        self, field: str, vehicle_info: Dict[str, str]
    ) -> Tuple[tk.BooleanVar, tk.Checkbutton, tk.Entry]:

        """
        Create checkboxes and entry fields for vehicle updates.
        """

        var, checkbox = self.create_checkbox(field)
        entry = UIComponents.create_text_entry(
            self, field, vehicle_info.get(field, ""),
            state="disabled"
         )

        var.trace_add(
            "write", lambda *args: UIComponents.toggle_entry_state(var, entry)
            )
        self.update_entries[field] = {"checkbox": var, "entry": entry}

        return var, checkbox, entry

    def display_message(
            self, message: str, color: str, font: Tuple[str, int] =
            ("Helvetica", 12)
            ) -> None:

        """
        Display a message on the UI.

        Args:
            message (str): The message to display.
            color (str): The color of the message text.
            font (Tuple[str, int], optional): The font style & size of text.
        """

        tk.Label(
            self.dynamic_content_frame, text=message, fg=color, font=font
                 ).pack(pady=10)

    def enable_delete_button(
            self, delete_button: tk.Button
            ) -> Optional[List[str]]:

        """
        Enable or disable the delete button based on selection.
        """

        selected_items = self.vehicle_table.selection()
        if selected_items:
            delete_button.config(state="normal")
            return selected_items
        else:
            delete_button.config(state="disabled")
            self.display_message("No vehicles selected for deletion.", "red")

    def show_status_popup(status_popup: tk.Toplevel, message: str) -> None:
        status_popup = tk.Toplevel()
        if status_popup == "Success":
            tk.Label(status_popup, text=message, fg="green").pack(pady=10)
        else:
            tk.Label(status_popup, text=message, fg="red").pack(pady=10)
        tk.Button(
            status_popup, text="Close", command=status_popup.destroy
                  ).pack(pady=10)

    def clear_form_fields(self) -> None:

        """
        Clears all form fields after adding a vehicle.
        """

        for entry in self.entries.values():
            entry.delete(0, tk.END)
        if hasattr(self, 'tax_status_dropdown') and self.tax_status_dropdown:
            self.tax_status_dropdown.set("") 

    def update_vehicle_table(self, vehicles: List[Tuple[Any, ...]]) -> None:

        """
        Update the vehicle table with new data.
        """

        for row in self.vehicle_table.get_children():
            self.vehicle_table.delete(row)
        for vehicle in vehicles:
            self.vehicle_table.insert("", tk.END, values=vehicle)

    def clear_dynamic_content(self) -> None:

        """
        Clear all dynamic content in the UI.
        """

        for widget in self.dynamic_content_frame.winfo_children():
            widget.destroy()

    def display_vehicle_info(self, vehicle_info: Dict[str, str]) -> None:

        """
        Display vehicle information in the UI.
        """

        vehicle_details = (
            f"Vehicle ID: {vehicle_info["id"]}\n"
            f"Registration: {vehicle_info["Registration"]}\n"
            f"Make: {vehicle_info["Make"]}\n"
        )
        tk.Label(
            self.dynamic_content_frame,
            text="Selected Vehicle:",
            font=("Arial", 12, "bold"),
            fg="black"
        ).pack()
        tk.Label(
            self.dynamic_content_frame,
            text=vehicle_details,
            fg="black"
        ).pack()
        return

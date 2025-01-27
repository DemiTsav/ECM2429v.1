import tkinter as tk
from tkinter import ttk
from vehicle_management_task.database import VehicleDatabase
from asset_management.vehicle_processes import VehicleProcess
from asset_management.ui_components import UIComponents
from asset_reporting.asset_reporting import AssetReportingPage
from typing import Dict, Union


class AssetManagementPage(tk.Frame):
    """
    A class for displaying and using features on the asset management UI
    """
    def __init__(self, parent: tk.Tk, db: VehicleDatabase) -> None:
        """
        Initialize the Asset Management Page.

        Args:
            parent (tk.Tk): The parent Tkinter window.
            db (VehicleDatabase): The database instance for vehicle data.
        """
        super().__init__(parent)
        self.db: VehicleDatabase = db
        self.entries: Dict[str, tk.Entry] = {}
        self.update_entries: Dict[str, Union[tk.Entry, ttk.Combobox]] = {}
        self.search_entries: Dict[str, Union[tk.Entry, ttk.Combobox]] = {}
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self) -> None:
        """Initialize all widgets and layout."""
        self._create_title_label()
        self._create_vehicle_table()
        self._create_action_buttons()
        self._create_dynamic_content_frame()
        self.show_all_vehicles()

    # Title Label
    def _create_title_label(self) -> None:
        """
        Create and pack the title label at the top of the page.
        """
        self.title_label = tk.Label(
            self, text="Council Asset Management", font=("Helvetica", 20)
        )
        self.title_label.pack(pady=20)

    # Vehicle Table and Scrollbar
    def _create_vehicle_table(self) -> None:
        """
        Create and pack the vehicle table along with a scrollbar.
        """
        self.vehicle_table_frame = tk.Frame(self)
        self.vehicle_table_frame.pack(pady=10, fill="both", expand=True)
        self.vehicle_table = self._init_vehicle_table(self.vehicle_table_frame)
        self.scrollbar = self._add_scrollbar(
            self.vehicle_table_frame, self.vehicle_table
            )

    @staticmethod
    def _init_vehicle_table(parent: tk.Frame) -> ttk.Treeview:
        """
        Initialize the vehicle table.

        Args:
            parent (tk.Frame): The parent frame where the table will be placed.

        Returns:
            ttk.Treeview: The initialized vehicle table.
        """
        columns = (
            "ID", "Make", "Model", "Year", "Type", "Fuel",
            "Service Date", "Tax Due Date", "Tax Status"
        )
        vehicle_table = ttk.Treeview(
            parent, columns=columns, show="headings", selectmode='browse'
        )
        for col in columns:
            vehicle_table.heading(col, text=col)
            vehicle_table.column(col, width=120)
        vehicle_table.pack(side="left", fill="both", expand=True)
        return vehicle_table

    @staticmethod
    def _add_scrollbar(parent: tk.Frame, table: ttk.Treeview) -> tk.Scrollbar:
        """
        Add a vertical scrollbar to the vehicle table.

        Args:
            parent (tk.Frame): Parent frame for scrollbar.
            table (ttk.Treeview): The vehicle table which requires the
            scrollbar.

        Returns:
            tk.Scrollbar: The added vertical scrollbar.
        """
        scrollbar = tk.Scrollbar(
            parent, orient="vertical", command=table.yview
            )
        table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        return scrollbar

    # Action Buttons
    def _create_action_buttons(self) -> None:
        """
        Create and pack the action buttons;
        (Add, Update, Delete, Search, Report)
        """
        self.actions_frame = tk.Frame(self)
        self.actions_frame.pack(pady=5)

        buttons = [
            ("Add Vehicle", self.show_add_vehicle_form),
            ("Update Vehicle", self.show_update_vehicle_form),
            ("Delete Vehicle", self.delete_vehicle_prompt),
            ("Search Vehicles", self.show_search_form),
            ("Create a Report", lambda: self.open_new_window(
                self.open_asset_reporting_page, self.db)),
        ]

        for text, command in buttons:
            UIComponents.create_button(
                self, self.actions_frame, text=text, command=command, padx=10
                )

    # Dynamic Content Frame
    def _create_dynamic_content_frame(self) -> None:
        """
        Create and pack the dynamic content frame that holds form elements.
        """
        self.dynamic_content_frame = tk.Frame(self)
        self.dynamic_content_frame.pack(pady=10, fill="both", expand=True)

    # Vehicle Table Methods
    def show_all_vehicles(self) -> None:
        """Reset the vehicle table"""
        """display all vehicles from the database"""
        # Clear the existing rows in the table
        self._reset_table()
        # Fetch vehicles from the database
        vehicles = self.db.get_all_vehicles()
        if not vehicles:
            return
        # Insert vehicles into the table
        self._populate_table(vehicles)

    def _reset_table(self) -> None:
        """
        Clear all rows from the vehicle table.
        """
        for row in self.vehicle_table.get_children():
            self.vehicle_table.delete(row)

    def _populate_table(self, vehicles: list) -> None:
        """
        Populate the vehicle table with data from the database.

        Args:
            vehicles (list): A list of vehicle data for display in table.
        """
        for vehicle in vehicles:
            self.vehicle_table.insert("", tk.END, values=vehicle)

    # Dynamic Content Handling
    def clear_dynamic_content(self) -> None:
        """
        Clear all widgets from the dynamic content frame.
        """
        for widget in self.dynamic_content_frame.winfo_children():
            widget.destroy()

    # Add Vehicle Form
    def show_add_vehicle_form(self) -> None:
        """
        Display the form to add a new vehicle to the database.
        """
        self.clear_dynamic_content()
        self.show_all_vehicles()
        self._create_vehicle_form("Add Vehicle", self._process_add_vehicle)

    def _create_vehicle_form(
            self, action: str, process_callback: callable
            ) -> None:
        """
        Create a form to add or update a vehicle.

        Args:
            action (str): The action for the form (e.g., "Add Vehicle").
            process_callback (callable): The function called upon form
            submission.
        """
        tk.Label(
            self.dynamic_content_frame,
            text=f"{action} Form",
            font=("Helvetica", 14)
            )
        self.title_label.pack(pady=5)
        fields = [
            "Make", "Model", "Year", "Vehicle Type", "Fuel Type",
            "Service Date", "Tax Due Date"
            ]

        self.entries = {}
        for field in fields:
            self._create_form_entry(field)

        tax_status_dropdown = self._create_tax_status_dropdown()
        tk.Button(
            self.dynamic_content_frame, text=action,
            command=lambda: process_callback(
                self.entries, tax_status_dropdown.get()
            )
        ).pack(pady=10)

    def _create_form_entry(self, field: str) -> None:
        """
        Create a form entry for a given field.

        Args:
            field (str): The name of the field for the entry widget.
        """
        tk.Label(self.dynamic_content_frame, text=field).pack(anchor="w")
        entry = tk.Entry(self.dynamic_content_frame)
        entry.pack(fill="x", pady=2)
        self.entries[field] = entry

    def _create_tax_status_dropdown(self) -> ttk.Combobox:
        """
        Create a dropdown for selecting the tax status of the vehicle.
        """
        tk.Label(
            self.dynamic_content_frame, text="Tax Status"
        ).pack(anchor="w")

        # Create a readonly Combobox
        tax_status_dropdown = ttk.Combobox(
            self.dynamic_content_frame,
            values=["Tax Paid", "Tax Due", "SORN", "Exempt"],
            state="readonly"  # Ensure it's readonly
        )
        tax_status_dropdown.pack(fill="x", pady=2)

        # Automatically open dropdown options when clicked
        tax_status_dropdown.bind(
            "<Button-1>", lambda event: tax_status_dropdown.event_generate("<Down>")
        )

        return tax_status_dropdown

    def _process_add_vehicle(self, entries: dict, tax_status: str) -> None:
        """
        Process the addition of a new vehicle to the database.

        Args:
            entries (dict): The dictionary of form entries.
            tax_status (str): The selected tax status of the vehicle.
        """
        VehicleProcess.process_add_vehicle(
            self, entries, tax_status
            )

    def show_update_vehicle_form(self) -> None:
        """
        Display the form to update an existing vehicle.
        """
        selected_items: list = self.vehicle_table.selection()
        self.clear_dynamic_content()
        if not selected_items:
            self.show_all_vehicles()
            tk.Label(
                self.dynamic_content_frame,
                text="Select a vehicle to update.",
                fg="blue"
            ).pack()
            return
        else:
            self.confirm_update(selected_items)

    def confirm_update(self, selected_items):
        """
        Confirm and execute the update of a selected vehicle.
        """
        # self.update_button.pack_forget()
        # selected_items: list = self.vehicle_table.selection()
        # Get selected vehicle information
        vehicle_id: str = self.vehicle_table.item(
            selected_items[0], "values"
            )[0]
        try:
            vehicle_info: dict = self.db.get_vehicle(vehicle_id)
            if not vehicle_info:
                tk.Label(
                    self.dynamic_content_frame,
                    text="Vehicle not found in database.", fg="red"
                    ).pack()
                return
        except Exception as e:
            tk.Label(
                self.dynamic_content_frame,
                text=f"Error retrieving vehicle: {str(e)}",
                fg="red"
            ).pack()
            return

        tk.Label(
            self.dynamic_content_frame,
            text=f"Updating Vehicle ID: {vehicle_id}",
            font=("Helvetica", 14)
            ).pack(pady=5)

        fields: list = [
            "Make", "Model", "Year", "Vehicle Type", "Fuel Type",
            "Service Date", "Tax Due Date"
            ]
        self.update_entries = {}

        for field in fields:
            UIComponents.checkbox_updates(self, field, vehicle_info)

        tax_status_dropdown = self._create_tax_status_dropdown()
        
        tax_status_var, checkbox = UIComponents.create_checkbox(
            self, "Tax Status", default_value=False
        )
    
        # tax_status_dropdown.config(state="disabled")
        tax_status_dropdown.config(state="readonly")

        # Bind checkbox to enable/disable the dropdown
        tax_status_var.trace_add(
            "write",
            lambda *args: UIComponents.toggle_entry_state(
                self, tax_status_var, tax_status_dropdown
            )
        )
        tk.Button(
            self.dynamic_content_frame,
            text="Update vehicle",
            command=lambda: VehicleProcess.process_update_vehicle(
                self, vehicle_id
                )
        ).pack(pady=10)
        self.show_all_vehicles()

    def delete_vehicle_prompt(self) -> None:
        """
        Display a confirmation prompt to delete a vehicle.
        """
        selected_items: list = self.vehicle_table.selection()
        self.clear_dynamic_content()
        if not selected_items:
            tk.Label(
                self.dynamic_content_frame,
                text="Please select a vehicle to delete.",
                fg="blue"
            ).pack()
            self.show_all_vehicles()
            return
        else:
            self.confirm_deletion(selected_items)

    def confirm_deletion(self, selected_items):
        """
        Display the confirmation message and selected vehicle details
        """
        if not selected_items:
            return
        delete_button = tk.Button(
            self.dynamic_content_frame,
            text="Confirm Deletion",
            command=VehicleProcess.show_deletion_confirmation(
                self,
                selected_items
                ),
            state="disabled"  # Disabled until a vehicle is selected
        )
        UIComponents.enable_delete_button(self, delete_button)
        # Get selected vehicle information
        vehicle_id = self.vehicle_table.item(selected_items[0], "values")[0]
        try:
            vehicle_info = self.db.get_vehicle(vehicle_id)
            if not vehicle_info:
                tk.Label(
                    self.dynamic_content_frame,
                    text="Vehicle not found in database.",
                    fg="red"
                    ).pack()
                return
        except Exception as e:
            tk.Label(
                self.dynamic_content_frame,
                text=f"Error retrieving vehicle: {str(e)}",
                fg="red"
                ).pack()
            return


    def show_search_form(self) -> None:
        """
        Display the search form for filtering vehicles.
        """
        self.clear_dynamic_content()
        self.show_all_vehicles()  # Reset the table before showing the form

        # Title for Search
        tk.Label(
            self.dynamic_content_frame,
            text="Search Vehicles",
            font=("Helvetica", 14)
        ).pack(pady=5)

        # Fields available for search
        fields: list = [
            "Make", "Model", "Year", "Vehicle Type", "Fuel Type",
            "Service Date", "Tax Due Date"
            ]
        self.search_entries = {}
        for field in fields:
            frame = tk.Frame(self.dynamic_content_frame)
            frame.pack(fill="x", pady=2)

            tk.Label(frame, text=field, width=15, anchor="w").pack(side="left")
            entry = tk.Entry(frame, width=20)
            entry.pack(side="left", expand=True, padx=2)
            entry.bind(
                "<KeyRelease>",
                lambda event: VehicleProcess.perform_search(self)
                )
            self.search_entries[field] = entry

        # Tax Status Dropdown
        frame = tk.Frame(self.dynamic_content_frame)
        frame.pack(fill="x", pady=2)

        tax_status_dropdown = self._create_tax_status_dropdown()
        tax_status_dropdown.bind(
            "<<ComboboxSelected>>",
            lambda event: VehicleProcess.perform_search(self)
            )
        self.search_entries["Tax Status"] = tax_status_dropdown
        VehicleProcess.perform_search(self)

    def open_new_window(self, create_widget: callable, *args) -> None:
        """Initilise a new window for asset reporting functions"""
        new_window = tk.Toplevel()
        new_window.title("Asset Reporting")
        create_widget(new_window, *args)

    def open_asset_reporting_page(
            self, new_window: tk.Toplevel, db: VehicleDatabase
            ) -> None:
        """
        Open the page to generate asset reports.
        """
        AssetReportingPage(new_window, db)

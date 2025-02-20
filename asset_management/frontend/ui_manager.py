import tkinter as tk
from tkinter import ttk
from asset_management.backend.asset_management_handler import VehicleController
from asset_management.frontend.asset_reporting import AssetReportingPage
from typing import List, Tuple
from asset_management.backend.asset_management_handler import VehicleDatabase


class AssetManagementUI(tk.Frame):
    """
    A class for displaying the asset management UI.

    Inherits from Tkinter's Frame class. This UI allows users to interact
    with asset data including adding, updating, deleting, and searching for
    vehicles.
    """

    def __init__(self, parent: tk.Tk, controller: VehicleController) -> None:
        """
        Initialize the Asset Management Page.

        Args:
            parent (tk.Tk): The parent Tkinter window.
            controller (VehicleController): The business logic controller.
        """
        super().__init__(parent)
        self.controller = controller
        self.connection = self.controller.connection
        self.cursor = self.controller.cursor
        self.update_entries = {}
        self.search_entries = {}

        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self) -> None:
        """Initialize all widgets and layout."""
        self._create_title_label()
        self._create_vehicle_table()
        self._create_action_buttons()
        self._create_dynamic_content_frame()
        self.refresh_vehicle_table()

    def _create_title_label(self) -> None:
        """Create and pack the title label."""
        title_label = tk.Label(
            self,
            text="Council Asset Management",
            font=("Helvetica", 20)
            )
        title_label.pack(pady=20)

    def _create_vehicle_table(self) -> None:
        """Create vehicle table and scrollbar."""
        self.vehicle_table_frame = tk.Frame(self)
        self.vehicle_table_frame.pack(pady=10, fill="both", expand=True)

        columns = ("ID", "Registration", "Make", "Model", "Year", "Type",
                   "Fuel", "Service Date", "Tax Due Date", "Tax Status")
        self.vehicle_table = ttk.Treeview(
            self.vehicle_table_frame,
            columns=columns,
            show="headings",
            selectmode='browse'
            )

        for col in columns:
            self.vehicle_table.heading(col, text=col)
            self.vehicle_table.column(col, width=120)

        scrollbar = tk.Scrollbar(
            self.vehicle_table_frame,
            orient="vertical",
            command=self.vehicle_table.yview
            )
        self.vehicle_table.configure(yscrollcommand=scrollbar.set)

        self.vehicle_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _create_action_buttons(self) -> None:
        """Create and pack action buttons."""
        actions_frame = tk.Frame(self)
        actions_frame.pack(pady=5)

        buttons = [
            ("Add Vehicle", self.show_add_vehicle_form),
            ("Update Vehicle", self.show_update_vehicle_form),
            ("Delete Vehicle", self.show_delete_vehicle_prompt),
            ("Search Vehicles", self.show_search_form),
            ("Asset Reporting", lambda: self.open_new_window(
                self.open_asset_reporting_page,
                self.controller
                ))
        ]

        for text, command in buttons:
            tk.Button(actions_frame, text=text, command=command, padx=10).pack(
                side="left",
                padx=5
                )

    def _create_dynamic_content_frame(self) -> None:
        """Create the dynamic content frame that holds forms."""
        self.dynamic_content_frame = tk.Frame(self)
        self.dynamic_content_frame.pack(pady=10, fill="both", expand=True)

    def refresh_vehicle_table(self) -> None:
        """Fetch and display all vehicles in the table."""
        for row in self.vehicle_table.get_children():
            self.vehicle_table.delete(row)

        vehicles = self.controller.get_all_vehicles()
        if vehicles:
            for vehicle in vehicles:
                self.vehicle_table.insert("", tk.END, values=vehicle)

    def show_add_vehicle_form(self) -> None:
        """Display the add vehicle form using grid layout."""
        self.clear_dynamic_content()
        self.refresh_vehicle_table()
        tk.Label(self.dynamic_content_frame, text="Add Vehicle",
                 font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2,
                                              pady=5)

        entries = {}
        fields = ["Registration", "Make", "Model", "Year", "Vehicle Type",
                  "Fuel Type", "Service Date", "Tax Due Date"]

        for i, field in enumerate(fields):
            tk.Label(self.dynamic_content_frame, text=field).grid(
                row=i+1, column=0, sticky="w", padx=5, pady=2)
            entry = tk.Entry(self.dynamic_content_frame)
            entry.grid(row=i+1, column=1, sticky="ew", padx=5, pady=2)
            entries[field] = entry  # Store entry widget reference

        tk.Label(self.dynamic_content_frame, text="Tax Status").grid(
            row=len(fields) + 1, column=0, sticky="w", padx=5, pady=2)

        tax_status = ttk.Combobox(self.dynamic_content_frame, values=[
            "Tax Paid", "Tax Due", "SORN", "Exempt"
            ],
            state="readonly")
        tax_status.grid(row=len(fields) + 1, column=1, sticky="ew", padx=5,
                        pady=2)

        # Button passes 'entries' and gets tax_status when clicked
        tk.Button(
            self.dynamic_content_frame,
            text="Add Vehicle",
            command=lambda: VehicleController.add_vehicle(
                self,
                entries,
                tax_status,
                self.refresh_vehicle_table,
                self.clear_dynamic_content
                )
        ).grid(row=len(fields) + 2, column=0, columnspan=2, pady=10)

    def show_delete_vehicle_prompt(self) -> None:
        """
        Display a confirmation prompt to delete a vehicle.
        """
        selected_items: list = self.vehicle_table.selection()
        self.clear_dynamic_content()
        if not selected_items:
            self.refresh_vehicle_table()
            tk.Label(
                self.dynamic_content_frame,
                text="Please select a vehicle to delete.",
                fg="blue"
            ).pack()
            return
        else:
            VehicleController.confirm_deletion(
                self,
                selected_items,
                self.refresh_vehicle_table,
                self.clear_dynamic_content
                )

    def show_update_vehicle_form(self) -> None:
        """
        Display the form to update an existing vehicle.
        """
        selected_items: list = self.vehicle_table.selection()
        self.clear_dynamic_content()
        if not selected_items:
            self.refresh_vehicle_table()
            tk.Label(
                self.dynamic_content_frame,
                text="Select a vehicle to update.",
                fg="blue"
            ).pack()
            return
        else:
            self.display_vehicle_data(selected_items)

    def display_vehicle_data(self, selected_items: list) -> None:
        """
        Display vehicle data to be updated.

        Args:
            selected_items (list): The selected items from the vehicle table.
        """
        vehicle_info, vehicle_id = VehicleController.retrieve_vehicle_info(
            self,
            selected_items
            )
        tk.Label(
            self.dynamic_content_frame,
            text=f"Updating Vehicle ID: {vehicle_id}",
            font=("Helvetica", 14)
        ).pack(pady=5)

        update_entries = {}  # Store checkbox and entry widgets
        editable_fields = {"Service Date", "Tax Due Date", "Tax Status"}

        for i, (field, value) in enumerate(vehicle_info.items()):
            if field in editable_fields:

                var = tk.BooleanVar(value=False)
                checkbox = tk.Checkbutton(
                    self.dynamic_content_frame,
                    text=f"{field}",
                    variable=var
                    )
                checkbox.pack(anchor="w")

                entry = tk.Entry(self.dynamic_content_frame)
                entry.insert(0, value)
                entry.config(state="disabled")
                entry.pack(pady=2)

                def toggle_entry_state(entry=entry, var=var):
                    entry.config(state="normal" if var.get() else "disabled")

                var.trace_add("write", lambda *args, entry=entry,
                              var=var: toggle_entry_state(entry, var))

                update_entries[field] = {"entry": entry, "checkbox": var}

            else:
                tk.Label(self.dynamic_content_frame,
                         text=f"{field}: {value}").pack(anchor="w")

        tk.Button(
            self.dynamic_content_frame,
            text="Update vehicle",
            command=lambda: VehicleController.update_vehicle(
                self,
                vehicle_id,
                self.refresh_vehicle_table,
                self.clear_dynamic_content,
                update_entries
                )
        ).pack(pady=10)

    def clear_dynamic_content(self) -> None:
        """Clear all widgets from the dynamic content frame."""
        for widget in self.dynamic_content_frame.winfo_children():
            widget.destroy()

    def show_search_form(self) -> None:
        """Display the search form and execute search based on criteria."""
        self.clear_dynamic_content()
        self.refresh_vehicle_table()
        tk.Label(self.dynamic_content_frame,
                 text="Search Vehicles",
                 font=("Helvetica", 14, "bold")
                 ).pack(pady=5)
        self._create_search_fields()
        self._create_tax_status_dropdown()

        results = VehicleController.perform_search(self)
        print(results)
        self.update_vehicle_values(results)

    def _create_search_fields(self) -> None:
        """Create search fields for searching vehicles."""
        self.search_entries = {}
        for field in [
            "Registration", "Make", "Model", "Year", "Vehicle Type",
            "Fuel Type", "Service Date", "Tax Due Date"
        ]:
            frame = tk.Frame(self.dynamic_content_frame)
            frame.pack(fill="x", pady=2)

            tk.Label(frame, text=field, width=15, anchor="w").pack(side="left")

            entry = tk.Entry(frame, width=20)
            entry.pack(side="left", expand=True, padx=2)

            # Bind key release event to trigger perform_search dynamically
            entry.bind(
                "<KeyRelease>",
                lambda event: self.update_vehicle_values(
                    VehicleController.perform_search(self)
                    ))

            self.search_entries[field] = entry

    def update_vehicle_values(self, results: List[Tuple]) -> None:
        """
        Update the vehicle table with new data.

        Args:
            vehicles (List[Tuple]): List of vehicle details to populate table.
        """
        for row in self.vehicle_table.get_children():
            self.vehicle_table.delete(row)

        if results:
            # Insert new rows for each vehicle in the results
            for vehicle in results:
                print(vehicle)
                self.vehicle_table.insert("", tk.END, values=vehicle)

    def _create_tax_status_dropdown(self) -> None:
        """Create a dropdown for selecting the tax status of the vehicle."""
        tk.Label(self.dynamic_content_frame, text="Tax Status").pack(
            anchor="w"
            )

        self.tax_status_var = tk.StringVar()
        self.tax_status_dropdown = ttk.Combobox(
            self.dynamic_content_frame,
            textvariable=self.tax_status_var,
            values=["", "Tax Paid", "Tax Due", "SORN", "Exempt"],
            state="readonly"
        )
        self.tax_status_dropdown.pack(fill="x", pady=2)

        self.tax_status_dropdown.bind(
            "<<ComboboxSelected>>",
            lambda event: self.update_vehicle_values(
                VehicleController.perform_search(self)
                ))

    def open_new_window(self, create_widget: callable, *args) -> None:
        """
        Initialize a new window for asset reporting functions.

        Args:
            create_widget (Callable): The function to create the widget in the
            new window.
            *args: Additional arguments to pass to the widget creation
            function.
        """
        new_window = tk.Toplevel()
        new_window.title("Asset Reporting")
        create_widget(new_window, *args)

    def open_asset_reporting_page(self, new_window: tk.Toplevel,
                                  db: VehicleDatabase) -> None:
        """
        Open the page to generate asset reports.

        Args:
            new_window (tk.Toplevel): The newly created window for asset
            reporting.
            db (VehicleDatabase): The database connection instance.
        """
        AssetReportingPage(new_window, db)

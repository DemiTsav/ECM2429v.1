import tkinter as tk
from tkinter import ttk
from asset_management.backend.asset_management_handler import VehicleController


class AssetManagementUI(tk.Frame):
    """
    A class for displaying the asset management UI.
    """

class AssetManagementUI(tk.Frame):
    """
    A class for displaying the asset management UI.
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
        self.connection = self.controller.connection  # Use the connection from the controller
        self.cursor = self.controller.cursor  # Use the cursor from the controller
        self.entries = {}
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
        title_label = tk.Label(self, text="Council Asset Management", font=("Helvetica", 20))
        title_label.pack(pady=20)

    def _create_vehicle_table(self) -> None:
        """Create vehicle table and scrollbar."""
        self.vehicle_table_frame = tk.Frame(self)
        self.vehicle_table_frame.pack(pady=10, fill="both", expand=True)

        columns = ("ID", "Registration", "Make", "Model", "Year", "Type", "Fuel", "Service Date", "Tax Due Date", "Tax Status")
        self.vehicle_table = ttk.Treeview(self.vehicle_table_frame, columns=columns, show="headings", selectmode='browse')

        for col in columns:
            self.vehicle_table.heading(col, text=col)
            self.vehicle_table.column(col, width=120)

        scrollbar = tk.Scrollbar(self.vehicle_table_frame, orient="vertical", command=self.vehicle_table.yview)
        self.vehicle_table.configure(yscrollcommand=scrollbar.set)

        self.vehicle_table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _create_action_buttons(self) -> None:
        """Create and pack action buttons."""
        actions_frame = tk.Frame(self)
        actions_frame.pack(pady=5)

        buttons = [
            ("Add Vehicle", self.show_add_vehicle_form),
            # ("Update Vehicle", self.show_update_vehicle_form),
            # ("Delete Vehicle", self.show_delete_vehicle_prompt),
            # ("Search Vehicles", self.show_search_form)
        ]

        for text, command in buttons:
            tk.Button(actions_frame, text=text, command=command, padx=10).pack(side="left", padx=5)

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

        tk.Label(self.dynamic_content_frame, text="Add Vehicle", font=("Helvetica", 14)).grid(row=0, column=0, columnspan=2, pady=5)

        entries = {}
        fields = ["Registration", "Make", "Model", "Year", "Vehicle Type", "Fuel Type", "Service Date", "Tax Due Date"]

        for i, field in enumerate(fields):
            tk.Label(self.dynamic_content_frame, text=field).grid(row=i+1, column=0, sticky="w", padx=5, pady=2)
            entry = tk.Entry(self.dynamic_content_frame)
            entry.grid(row=i+1, column=1, sticky="ew", padx=5, pady=2)
            entries[field] = entry  # Store entry widget reference

        tk.Label(self.dynamic_content_frame, text="Tax Status").grid(row=len(fields) + 1, column=0, sticky="w", padx=5, pady=2)

        tax_status = ttk.Combobox(self.dynamic_content_frame, values=["Tax Paid", "Tax Due", "SORN", "Exempt"], state="readonly")
        tax_status.grid(row=len(fields) + 1, column=1, sticky="ew", padx=5, pady=2)

        # Button passes 'entries' and gets tax_status when clicked
        tk.Button(
            self.dynamic_content_frame, 
            text="Add Vehicle", 
            command=lambda: VehicleController.add_vehicle(self, entries, tax_status, self.refresh_vehicle_table, self.clear_dynamic_content)
        ).grid(row=len(fields) + 2, column=0, columnspan=2, pady=10)

    def clear_dynamic_content(self) -> None:
        """Clear all widgets from the dynamic content frame."""
        for widget in self.dynamic_content_frame.winfo_children():
            widget.destroy()


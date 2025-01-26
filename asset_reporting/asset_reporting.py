import tkinter as tk
from tkinter import messagebox, filedialog
import csv
from vehicle_management_task.database import VehicleDatabase
from typing import List, Dict, Tuple
from asset_management.ui_components import UIComponents


class AssetReportingPage(tk.Frame):
    
    """
    A Frame which allows the user to generate and display various reports
    about vehicles in the asset management system. Users can choose from predefined 
    report types or create a custom report with specific filters, and export reports 
    to CSV files.
    """
    
    def __init__(self, parent: tk.Widget, db: VehicleDatabase) -> None:
        """
        Initializes the AssetReportingPage with a connection to the database
        and sets up the user interface for generating reports.

        Args:
            parent (tk.Widget): The parent widget to place this frame in.
            db (VehicleDatabase): The database object to query for vehicle data.
        """
        super().__init__(parent)
        self.db = db
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self) -> None:
        """
        Creates and arranges the widgets on the page, including labels, dropdowns, 
        and buttons for report selection and generation.
        """
        self.title_label = tk.Label(
            self,
            text="Asset Reporting",
            font=("Helvetica", 16)
            )
        self.title_label.pack(pady=10)

        # Report Options Section
        self.report_label = tk.Label(
            self,
            text="Choose Report Type"
            )
        self.report_label.pack(pady=5)

        # Create a StringVar to hold the selected report type
        self.report_var = tk.StringVar()
        self.report_var.set("Choose a Report")  # Set a default value

        report_options: List[str] = ["All Vehicles",
                                     "Vehicles Due for Service",
                                     "Vehicles with Tax Due",
                                     "Vehicles Older Than 10 Years",
                                     "Diesel Vehicles",
                                     "Custom Report"]
        self.report_dropdown = tk.OptionMenu(
            self,
            self.report_var,
            *report_options
            )
        self.report_dropdown.pack(pady=10)

        # Button to generate the report
        self.generate_button = tk.Button(
            self,
            text="Generate Report",
            command=self.generate_report
            )
        self.generate_button.pack(pady=10)
        # Create a frame for filters on the left side
        self.filter_frame = tk.Frame(self)
        self.filter_frame.pack(side="left", fill="y", padx=10)

        # Create a frame for the report display on the right side
        self.report_frame = tk.Frame(self)
        self.report_frame.pack(side="right", fill="both", expand=True, padx=10)

        # Text widget to display report results
        self.report_text = tk.Text(self.report_frame, wrap="word")
        self.report_text.pack(fill="both", expand=True, pady=10)

        self.vehicles: List[Tuple] = []
        self.confirm_export_button = None

    def generate_report(self) -> None:
        """
        Generates a report based on the selected report type and displays it in the report area.

        Queries the database for the appropriate data based on the selected report type.
        If the report type is "Custom Report", a custom report generation form is shown instead.
        """
        self.report_text.delete(1.0, tk.END)

        # Get selected report type from the StringVar
        report_type: str = self.report_var.get()

        # Mapping of report types to their respective SQL queries
        report_queries = {
            "All Vehicles": "SELECT * FROM vehicles",
            "Vehicles Due for Service": (
                "SELECT * FROM vehicles WHERE service_date <= "
                "date('now', '+1 month')"
            ),
            "Vehicles with Tax Due": (
                "SELECT * FROM vehicles WHERE tax_due_date <= "
                "date('now', '+1 month')"
            ),
            "Vehicles Older Than 10 Years": (
                "SELECT * FROM vehicles WHERE year <= "
                "strftime('%Y', 'now') - 10"
            ),
            "Diesel Vehicles": (
                "SELECT * FROM vehicles WHERE LOWER(fuel_type) = "
                "LOWER('Diesel')"
            ),
            "Petrol Vehicles": (
                "SELECT * FROM vehicles WHERE LOWER(fuel_type) = "
                "LOWER('Petrol')"
            ),
        }
        if report_type == "Custom Report":
            self.custom_report()
            return

        # Fetch the query from the dictionary
        query = report_queries.get(report_type)

        if query:
            self.vehicles = self.db.query_vehicles(query)
        else:
            UIComponents.show_status_popup("Error", "Please select a valid report type.")
            return

        # Display the report
        AssetReportingPage.display_report(self)

    def display_report(self) -> None:
        """
        Displays the generated report in the report area.     
        The report is formatted as a text table,
        showing all relevant vehicle information.

        After the report is displayed, an export button is added to allow the user to export
        the report to a CSV file.
        """
        self.report_text.delete(1.0, tk.END)

        # Format and display the vehicles in the report text widget
        report_header: str = (
            "ID | Make | Model | Year | Vehicle Type | Fuel Type | "
            "Service Date | Tax Due Date | Tax Status\n"
        )

        report_separator: str = "-" * 90
        self.report_text.insert(
            tk.END,
            report_header + report_separator + "\n"
            )

        for vehicle in self.vehicles:

            vehicle_info: str = (
                f"{vehicle[0]} | {vehicle[1]} | {vehicle[2]} | {vehicle[3]} | "
                f"{vehicle[4]} | {vehicle[5]} | {vehicle[6]} | {vehicle[7]} | "
                f"{vehicle[8]}\n"
            )

            self.report_text.insert(tk.END, vehicle_info)

        # After the report is generated, add the export button
        if self.confirm_export_button is None:
            self.confirm_export_button = tk.Button(
                self.report_frame,
                text="Confirm Export to CSV",
                command=self.confirm_export_to_csv
                )
            self.confirm_export_button.pack(pady=10)

    def custom_report(self) -> None:
        """
        Creates a custom report form with filter fields for users to enter
        custom filtering criteria.
        Generates a report based on the user-defined filters.
        """
        for widget in self.filter_frame.winfo_children():
            widget.destroy()

        # Create labels and entry fields for filtering
        self.filters: Dict[str, tk.Entry] = {
            field: self.create_filter(self.filter_frame, field)
            for field in [
                "Make", "Model", "Year", "Fuel Type", "Vehicle Type",
                "Tax Status", "Tax Due Date", "Service Date"
            ]
        }
        # Button to generate the custom report
        self.generate_custom_report_button = tk.Button(
            self.filter_frame,
            text="Generate Custom Report",
            command=self.generate_custom_report
            )
        self.generate_custom_report_button.pack(pady=10)

    def create_filter(self, window: tk.Frame, label_text: str) -> tk.Entry:
        """
        Creates a filter field for a specific vehicle attribute.

        Args:
            window (tk.Frame): The frame where the filter widget is placed.
            label_text (str): The name of the vehicle attribute to filter by.

        Returns:
            tk.Entry: The entry widget for user input.
        """
        label = tk.Label(window, text=f"Filter by {label_text}:")
        label.pack(pady=5)
        entry = tk.Entry(window)
        entry.pack(pady=5)
        return entry

    def generate_custom_report(self) -> None:
        """
        Generates a custom report based on the filters provided by the user.

        Builds a dynamic SQL query based on entered fields and shows results.
        """
        self.report_text.delete(1.0, tk.END)

        # Build the SQL query dynamically based on user inputs
        query: str = "SELECT * FROM vehicles WHERE 1=1"

        # Check each filter fiel, add it to the query if the field is not empty
        filter_params: List[str] = []
        for field, entry in self.filters.items():
            if field == "Vehicle Type":
                field = "vehicle_type"
            value: str = entry.get()
            if value:
                filter_replace = field.lower().replace(' ', '_')
                filter_params.append(f"LOWER({filter_replace} LIKE LOWER(?)")

        # If filters are provided, append them to the query
        if filter_params:
            query += " AND " + " AND ".join(filter_params)

        # Query the database
        try:
            filter_values = [
                f"%{entry.get()}%"
                for entry in self.filters.values()
                if entry.get()
            ]

            self.vehicles = self.db.query_vehicles(
                query,
                tuple(filter_values)
            )

            self.display_report()  # Display the filtered report
        except Exception as e:
            messagebox.showerror(
                "Error", f"Error generating custom report: {e}"
                )

    def confirm_export_to_csv(self) -> None:
        """
        Confirms with the user if they want to export to a CSV file.
        If confirmed, the export process is triggered.
        """
        if not self.vehicles:
            messagebox.showerror(
                "Error", "No report data available to export."
                )
            return
        confirm: bool = messagebox.askyesno(
            "Export to CSV", "Do you want to export the report to a CSV file?"
            )
        if confirm:
            self.export_to_csv()

    def export_to_csv(self) -> None:
        """
        Exports the displayed report to a CSV file, user to choose file
        location and name. The report data is written to the selected file.
        """
        file_path: str = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
            )
        if file_path:
            try:
                # Write the vehicles data to the CSV file
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    # Write the header
                    writer.writerow([
                        "ID", "Make", "Model", "Year", "Type", "Fuel",
                        "Service Date", "Tax Due Date", "Tax Status"
                        ])
                    # Write the data rows
                    for vehicle in self.vehicles:
                        writer.writerow(vehicle)

                messagebox.showinfo(
                    "Success", f"Report successfully exported to {file_path}"
                    )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export report: {e}")

import tkinter as tk
from tkinter import messagebox, filedialog
import csv
from vehicle_management_task.database import VehicleDatabase
from typing import List, Dict, Tuple, Union, Optional

class AssetReportingPage(tk.Frame):
    def __init__(self, parent: tk.Widget, db: VehicleDatabase) -> None:
        super().__init__(parent)
        self.db = db
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self) -> None:
        self.title_label = tk.Label(self, text="Asset Reporting", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        # Report Options Section
        self.report_label = tk.Label(self, text="Choose Report Type:", font=("Helvetica", 12))
        self.report_label.pack(pady=5)

        # Create a StringVar to hold the selected report type
        self.report_var = tk.StringVar()
        self.report_var.set("Choose a Report")  # Set a default value

        report_options: List[str] = ["All Vehicles", "Vehicles Due for Service", "Vehicles with Tax Due",
                          "Vehicles Older Than 10 Years", "Diesel Vehicles", "Custom Report"]
        self.report_dropdown = tk.OptionMenu(self, self.report_var, *report_options)
        self.report_dropdown.pack(pady=10)

        # Button to generate the report
        self.generate_button = tk.Button(self, text="Generate Report", command=self.generate_report)
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

        self.vehicles: List[Tuple] = []  # Store vehicles data to be exported
        self.confirm_export_button = None  # Initialize the export button as None

    def generate_report(self) -> None:
        # Clear the previous report results
        self.report_text.delete(1.0, tk.END)

        # Get selected report type from the StringVar
        report_type: str = self.report_var.get()

        # Query the database based on the selected report type
        if report_type == "All Vehicles":
            self.vehicles = self.db.query_vehicles("SELECT * FROM vehicles")
        elif report_type == "Vehicles Due for Service":
            self.vehicles = self.db.query_vehicles("SELECT * FROM vehicles WHERE service_date <= date('now', '+1 month')")
        elif report_type == "Vehicles with Tax Due":
            self.vehicles = self.db.query_vehicles("SELECT * FROM vehicles WHERE tax_due_date <= date('now', '+1 month')")
        elif report_type == "Vehicles Older Than 10 Years":
            self.vehicles = self.db.query_vehicles("SELECT * FROM vehicles WHERE year <= strftime('%Y', 'now') - 10")
        elif report_type == "Diesel Vehicles":
            self.vehicles = self.db.query_vehicles("SELECT * FROM vehicles WHERE LOWER(fuel_type) = LOWER('Diesel')")
        elif report_type == "Petrol Vehicles":
            self.vehicles = self.db.query_vehicles("SELECT * FROM vehicles WHERE LOWER(fuel_type) = LOWER('Petrol')")
        elif report_type == "Custom Report":
            self.custom_report()
            return  # Skip the default report generation if it's a custom report
        else:
            messagebox.showerror("Error", "Please select a valid report type.")
            return

        # Display the report
        AssetReportingPage.display_report(self)

    def display_report(self) -> None:
        # Clear the previous report results before displaying the new report
        self.report_text.delete(1.0, tk.END)

        # Format and display the vehicles in the report text widget
        report_header: str = (
            "ID | Make | Model | Year | Vehicle Type | Fuel Type | Service Date | Tax Due Date | Tax Status\n"
        )
        report_separator: str = "-" * 90
        self.report_text.insert(tk.END, report_header + report_separator + "\n")

        for vehicle in self.vehicles:
            vehicle_info: str = (f"{vehicle[0]} | {vehicle[1]} | {vehicle[2]} | {vehicle[3]} | {vehicle[4]} | {vehicle[5]} | {vehicle[6]} | {vehicle[7]} | {vehicle[8]}\n")
            self.report_text.insert(tk.END, vehicle_info)

        # After the report is generated, add the export button
        if self.confirm_export_button is None:
            self.confirm_export_button = tk.Button(self.report_frame, text="Confirm Export to CSV", command=self.confirm_export_to_csv)
            self.confirm_export_button.pack(pady=10)

    def custom_report(self) -> None:
        # Clear the previous filters
        for widget in self.filter_frame.winfo_children():
            widget.destroy()

        # Create labels and entry fields for filtering
        self.filters: Dict[str, tk.Entry] = {
            field: self.create_filter(self.filter_frame, field)
            for field in [
                "Make", "Model", "Year", "Fuel Type", "Vehicle Type", "Tax Status", "Tax Due Date", "Service Date"
            ]
        }
        # Button to generate the custom report
        self.generate_custom_report_button = tk.Button(self.filter_frame, text="Generate Custom Report", command=self.generate_custom_report)
        self.generate_custom_report_button.pack(pady=10)

    def create_filter(self, window: tk.Frame, label_text: str) -> tk.Entry:
        label = tk.Label(window, text=f"Filter by {label_text}:")
        label.pack(pady=5)
        entry = tk.Entry(window)
        entry.pack(pady=5)
        return entry

    def generate_custom_report(self) -> None:
        # Clear the previous report results
        self.report_text.delete(1.0, tk.END)

        # Build the SQL query dynamically based on user inputs
        query: str = "SELECT * FROM vehicles WHERE 1=1"
        
        # Check each filter field and add it to the query if the field is not empty
        filter_params: List[str] = []
        for field, entry in self.filters.items():
            if field == "Vehicle Type":
                field = "vehicle_type"
            value: str = entry.get()
            if value:
                filter_params.append(f"LOWER({field.lower().replace(' ', '_')}) LIKE LOWER(?)")
        
        # If filters are provided, append them to the query
        if filter_params:
            query += " AND " + " AND ".join(filter_params)

        # Query the database
        try:
            self.vehicles = self.db.query_vehicles(query, tuple([f"%{entry.get()}%" for entry in self.filters.values() if entry.get()]))
            self.display_report()  # Display the filtered report
        except Exception as e:
            messagebox.showerror("Error", f"Error generating custom report: {e}")

    def confirm_export_to_csv(self) -> None:
        if not self.vehicles:
            messagebox.showerror("Error", "No report data available to export.")
            return
        
        # Ask the user for confirmation to export
        confirm: bool = messagebox.askyesno("Export to CSV", "Do you want to export the report to a CSV file?")
        if confirm:
            self.export_to_csv()

    def export_to_csv(self) -> None:
        # Open a file dialog to choose the location to save the CSV
        file_path: str = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                # Write the vehicles data to the CSV file
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    # Write the header
                    writer.writerow(["ID", "Make", "Model", "Year", "Type", "Fuel", "Service Date", "Tax Due Date", "Tax Status"])
                    # Write the data rows
                    for vehicle in self.vehicles:
                        writer.writerow(vehicle)

                messagebox.showinfo("Success", f"Report successfully exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export report: {e}")

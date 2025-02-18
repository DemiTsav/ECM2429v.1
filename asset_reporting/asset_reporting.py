import tkinter as tk
from tkinter import messagebox, filedialog
import csv
from vehicle_management_task.database import VehicleDatabase
from typing import List, Dict, Tuple
from asset_management.ui_components import UIComponents


class AssetReportingPage(tk.Frame):
    
    def __init__(self, parent: tk.Widget, db: VehicleDatabase) -> None:
        super().__init__(parent)
        self.db = db
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self) -> None:
        self.title_label = tk.Label(self, text="Asset Reporting", font=("Helvetica", 16))
        self.title_label.pack(pady=10)

        self.report_label = tk.Label(self, text="Choose Report Type")
        self.report_label.pack(pady=5)

        self.report_var = tk.StringVar()
        self.report_var.set("Choose a Report")

        report_options: List[str] = ["All Vehicles", "Vehicles Due for Service", "Vehicles with Tax Due", 
                                     "Vehicles Older Than 10 Years", "Diesel Vehicles", "Custom Report"]
        self.report_dropdown = tk.OptionMenu(self, self.report_var, *report_options)
        self.report_dropdown.pack(pady=10)

        self.generate_button = tk.Button(self, text="Generate Report", command=self.generate_report)
        self.generate_button.pack(pady=10)

        self.filter_frame = tk.Frame(self)
        self.filter_frame.pack(side="left", fill="y", padx=10)

        self.report_frame = tk.Frame(self)
        self.report_frame.pack(side="right", fill="both", expand=True, padx=10)

        self.report_text = tk.Text(self.report_frame, wrap="word")
        self.report_text.pack(fill="both", expand=True, pady=10)

        self.vehicles: List[Tuple] = []
        self.confirm_export_button = None

    def generate_report(self) -> None:
        self.report_text.delete(1.0, tk.END)
        report_type: str = self.report_var.get()

        report_queries = {
            "All Vehicles": "SELECT * FROM vehicles",
            "Vehicles Due for Service": "SELECT * FROM vehicles WHERE service_date <= date('now', '+1 month')",
            "Vehicles with Tax Due": "SELECT * FROM vehicles WHERE tax_due_date <= date('now', '+1 month')",
            "Vehicles Older Than 10 Years": "SELECT * FROM vehicles WHERE year <= strftime('%Y', 'now') - 10",
            "Diesel Vehicles": "SELECT * FROM vehicles WHERE LOWER(fuel_type) = LOWER('Diesel')",
        }

        if report_type == "Custom Report":
            self.custom_report()
            return

        query = report_queries.get(report_type)
        if query:
            self.vehicles = self.db.query_vehicles(query)
        else:
            UIComponents.show_status_popup("Error", "Please select a valid report type.")
            return

        self.display_report()

    def display_report(self) -> None:
        self.report_text.delete(1.0, tk.END)
        report_header = ("ID | Registration| Make | Model | Year | Vehicle Type | Fuel Type | "
                         "Service Date | Tax Due Date | Tax Status\n")
        report_separator = "-" * 90
        self.report_text.insert(tk.END, report_header + report_separator + "\n")

        for vehicle in self.vehicles:
            vehicle_info = (f"{vehicle[0]} | {vehicle[1]} | {vehicle[2]} | {vehicle[3]} | "
                            f"{vehicle[4]} | {vehicle[5]} | {vehicle[6]} | {vehicle[7]} | "
                            f"{vehicle[8]}\n")
            self.report_text.insert(tk.END, vehicle_info)

        if self.confirm_export_button is None:
            self.confirm_export_button = tk.Button(self.report_frame, text="Confirm Export to CSV",
                                                    command=self.confirm_export_to_csv)
            self.confirm_export_button.pack(pady=10)

    def custom_report(self) -> None:
        for widget in self.filter_frame.winfo_children():
            widget.destroy()

        self.filters: Dict[str, tk.Entry] = {
            field: self.create_filter(self.filter_frame, field)
            for field in ["Registration", "Make", "Model", "Year", "Fuel Type", "Vehicle Type", "Tax Status", "Tax Due Date", "Service Date"]
        }

        self.generate_custom_report_button = tk.Button(self.filter_frame, text="Generate Custom Report", 
                                                       command=self.generate_custom_report)
        self.generate_custom_report_button.pack(pady=10)

    def create_filter(self, window: tk.Frame, label_text: str) -> tk.Entry:
        label = tk.Label(window, text=f"Filter by {label_text}:")
        label.pack(pady=5)
        entry = tk.Entry(window)
        entry.pack(pady=5)
        return entry

    def generate_custom_report(self) -> None:
        self.report_text.delete(1.0, tk.END)

        query = "SELECT * FROM vehicles WHERE 1=1"
        filter_params = []
        for field, entry in self.filters.items():
            value = entry.get()
            if value:
                filter_replace = field.lower().replace(' ', '_')
                filter_params.append(f"LOWER({filter_replace}) LIKE LOWER(?)")

        if filter_params:
            query += " AND " + " AND ".join(filter_params)

        try:
            filter_values = [f"%{entry.get()}%" for entry in self.filters.values() if entry.get()]
            self.vehicles = self.db.query_vehicles(query, tuple(filter_values))
            self.display_report()
        except Exception as e:
            messagebox.showerror("Error", f"Error generating custom report: {e}")

    def confirm_export_to_csv(self) -> None:
        if not self.vehicles:
            messagebox.showerror("Error", "No report data available to export.")
            return
        confirm = messagebox.askyesno("Export to CSV", "Do you want to export the report to a CSV file?")
        if confirm:
            self.export_to_csv()

    def export_to_csv(self) -> None:
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["ID", "Registration", "Make", "Model", "Year", "Type", "Fuel", "Service Date", "Tax Due Date", "Tax Status"])
                    for vehicle in self.vehicles:
                        writer.writerow(vehicle)

                messagebox.showinfo("Success", f"Report successfully exported to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export report: {e}")

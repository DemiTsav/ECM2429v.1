import tkinter as tk
from tkinter import messagebox, filedialog
import csv
from asset_management.backend.report_generation import AssetReportingHandler
from asset_management.frontend.ui_components import UIComponents
from typing import List, Optional


class AssetReportingPage(tk.Frame):
    def __init__(self, parent: tk.Widget, db: object) -> None:
        super().__init__(parent)
        self.db = db
        self.pack(fill="both", expand=True)
        self.create_widgets()

    def create_widgets(self) -> None:
        """Creates UI components for the reporting page."""
        self.title_label = tk.Label(
            self,
            text="Asset Reporting",
            font=("Helvetica", 16)
            )
        self.title_label.pack(pady=10)

        self.report_label = tk.Label(self, text="Choose Report Type")
        self.report_label.pack(pady=5)

        self.report_var = tk.StringVar()
        self.report_var.set("Choose a Report")

        report_options = [
            "All Vehicles", "Vehicles Due for Service",
            "Vehicles with Tax Due", "Vehicles Older Than 10 Years",
            "Diesel Vehicles", "Custom Report"
        ]
        self.report_dropdown = tk.OptionMenu(
            self,
            self.report_var,
            *report_options
            )
        self.report_dropdown.pack(pady=10)

        self.generate_button = tk.Button(
            self,
            text="Generate Report",
            command=self.generate_report
            )
        self.generate_button.pack(pady=10)

        self.filter_frame = tk.Frame(self)
        self.filter_frame.pack(side="left", fill="y", padx=10)

        self.report_frame = tk.Frame(self)
        self.report_frame.pack(side="right", fill="both", expand=True, padx=10)

        self.report_text = tk.Text(self.report_frame, wrap="word")
        self.report_text.pack(fill="both", expand=True, pady=10)

        self.vehicles: List[List[str]] = []
        self.confirm_export_button: Optional[tk.Button] = None

    def generate_report(self) -> None:
        """Fetches the selected report and displays it."""
        self.report_text.delete(1.0, tk.END)
        report_type = self.report_var.get()

        if report_type == "Custom Report":
            self.custom_report()
            return

        self.vehicles = AssetReportingHandler.fetch_report(
            self.db,
            report_type
            )
        if not self.vehicles:
            UIComponents.show_status_popup(
                "Error",
                "Please select a valid report type."
                )
            return

        self.display_report()

    def display_report(self) -> None:
        """Displays the report in the text area."""
        self.report_text.delete(1.0, tk.END)
        header = (
            "ID | Registration | Make | Model | Year | Type | Fuel |"
            "Service Date | Tax Due Date | Tax Status\n"
        )
        separator = "-" * 120
        self.report_text.insert(tk.END, header + separator + "\n")

        for vehicle in self.vehicles:
            vehicle_data = " | ".join(str(v) for v in vehicle)
            self.report_text.insert(tk.END, vehicle_data + "\n")

        if self.confirm_export_button is None:
            self.confirm_export_button = tk.Button(
                self.report_frame,
                text="Confirm Export to CSV",
                command=self.confirm_export_to_csv
            )
            self.confirm_export_button.pack(pady=10)

    def custom_report(self) -> None:
        """Creates input fields for custom report filtering."""
        for widget in self.filter_frame.winfo_children():
            widget.destroy()

        self.filters = {
            field: self.create_filter(self.filter_frame, field)
            for field in ["Registration", "Make", "Model", "Year", "Fuel Type",
                          "Vehicle Type", "Tax Status", "Tax Due Date",
                          "Service Date"]
        }

        self.generate_custom_report_button = tk.Button(
            self.filter_frame,
            text="Generate Custom Report",
            command=self.generate_custom_report
        )
        self.generate_custom_report_button.pack(pady=10)

    def create_filter(self, window: tk.Frame, label_text: str) -> tk.Entry:
        """Creates a filter entry field."""
        label = tk.Label(window, text=f"Filter by {label_text}:")
        label.pack(pady=5)
        entry = tk.Entry(window)
        entry.pack(pady=5)
        return entry

    def generate_custom_report(self) -> None:
        """Fetches and displays a custom report based on user input."""
        filters = {
            field: entry.get().strip()
            for field, entry in self.filters.items()
            if entry.get().strip()
        }
        self.vehicles = AssetReportingHandler.fetch_custom_report(
            self.db,
            filters
            )
        self.display_report()

    def confirm_export_to_csv(self) -> None:
        """Confirms and triggers CSV export."""
        if not self.vehicles:
            messagebox.showerror(
                "Error",
                "No report data available to export."
                )
            return

        confirm = messagebox.askyesno(
            "Export to CSV",
            "Do you want to export the report to a CSV file?"
            )
        if confirm:
            self.export_to_csv()

    def export_to_csv(self) -> None:
        """Exports the report to a CSV file."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")]
        )
        if file_path:
            try:
                with open(file_path, mode="w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(["ID", "Registration", "Make", "Model",
                                     "Year", "Type", "Fuel", "Service Date",
                                     "Tax Due Date", "Tax Status"])
                    for vehicle in self.vehicles:
                        writer.writerow(vehicle)

                messagebox.showinfo(
                    "Success",
                    f"Report successfully exported to {file_path}"
                    )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export report: {e}")

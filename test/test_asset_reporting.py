import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from vehicle_management_task.database import VehicleDatabase
from asset_reporting.asset_reporting import AssetReportingPage  # Adjust the import if necessary


class TestAssetReportingPage(unittest.TestCase):
    
    def setUp(self):
        # Setup a mock database connection
        self.mock_db = MagicMock(VehicleDatabase)
        self.root = tk.Tk()
        self.asset_reporting_page = AssetReportingPage(self.root, self.mock_db)
        
    def test_generate_report_all_vehicles(self):
        # Simulate the "All Vehicles" report type selection
        self.asset_reporting_page.report_var.set("All Vehicles")
        self.asset_reporting_page.generate_report()

        # Ensure that the database query is executed for "All Vehicles"
        self.mock_db.query_vehicles.assert_called_with("SELECT * FROM vehicles")
        
        # Ensure the report text is cleared before new data is inserted
        self.asset_reporting_page.report_text.delete.assert_called_with(1.0, tk.END)

        # Ensure that the report content is generated
        self.assertIn("ID | Make | Model | Year | Vehicle Type", self.asset_reporting_page.report_text.get(1.0, tk.END))

    def test_generate_report_vehicles_due_for_service(self):
        # Simulate the "Vehicles Due for Service" report type selection
        self.asset_reporting_page.report_var.set("Vehicles Due for Service")
        self.asset_reporting_page.generate_report()

        # Ensure the correct query is called for "Vehicles Due for Service"
        self.mock_db.query_vehicles.assert_called_with("SELECT * FROM vehicles WHERE service_date <= date('now', '+1 month')")

    def test_generate_report_custom_report(self):
        # Simulate the "Custom Report" report type selection
        self.asset_reporting_page.report_var.set("Custom Report")
        
        # Mock user input for custom filters
        mock_filters = {
            "Make": MagicMock(get=MagicMock(return_value="Toyota")),
            "Model": MagicMock(get=MagicMock(return_value="Corolla")),
            "Year": MagicMock(get=MagicMock(return_value="2020")),
        }

        self.asset_reporting_page.filters = mock_filters  # Assign mock filters
        
        # Simulate custom report generation
        self.asset_reporting_page.generate_report()

        # Ensure that the custom report filters are correctly applied
        self.mock_db.query_vehicles.assert_called_with(
            "SELECT * FROM vehicles WHERE 1=1 AND LOWER(make) LIKE LOWER(?) AND LOWER(model) LIKE LOWER(?) AND LOWER(year) LIKE LOWER(?)", 
            ("%Toyota%", "%Corolla%", "%2020%")
        )

    def test_generate_custom_report_ui(self):
        # Simulate the Custom Report UI generation (filters)
        self.asset_reporting_page.custom_report()

        # Check if the filters are correctly created
        self.assertEqual(len(self.asset_reporting_page.filter_frame.winfo_children()), 9)  # 8 filters + 1 button

    @patch('tkinter.filedialog.asksaveasfilename')
    def test_export_to_csv(self, mock_saveasfilename):
        # Simulate generating a report
        self.asset_reporting_page.vehicles = [
            (1, "Toyota", "Corolla", 2020, "Sedan", "Petrol", "2023-05-01", "2023-10-01", "Paid"),
            (2, "Ford", "Focus", 2018, "Hatchback", "Diesel", "2022-06-01", "2022-12-01", "Unpaid"),
        ]

        # Mock file dialog to return a fake file path
        mock_saveasfilename.return_value = "test_report.csv"
        
        # Call the export method
        self.asset_reporting_page.export_to_csv()

        # Ensure that the file path is passed to the CSV writer
        mock_saveasfilename.assert_called_once()

    @patch('tkinter.messagebox.showerror')
    def test_export_to_csv_no_data(self, mock_showerror):
        # Call the export method with no vehicles data
        self.asset_reporting_page.vehicles = []
        self.asset_reporting_page.export_to_csv()

        # Ensure that an error message is shown when there is no data to export
        mock_showerror.assert_called_with("Error", "No report data available to export.")

    @patch('tkinter.messagebox.askyesno')
    def test_confirm_export_to_csv(self, mock_askyesno):
        # Simulate the "Yes" response for the export confirmation
        mock_askyesno.return_value = True
        
        # Simulate generating a report
        self.asset_reporting_page.vehicles = [
            (1, "Toyota", "Corolla", 2020, "Sedan", "Petrol", "2023-05-01", "2023-10-01", "Paid")
        ]
        
        # Call the confirm export method
        self.asset_reporting_page.confirm_export_to_csv()

        # Check if the export to CSV method was called
        self.asset_reporting_page.export_to_csv.assert_called()

    @patch('tkinter.messagebox.showerror')
    def test_generate_report_no_selection(self, mock_showerror):
        # Test the case when no report type is selected
        self.asset_reporting_page.report_var.set("Choose a Report")
        self.asset_reporting_page.generate_report()

        # Ensure that an error message is displayed when no report type is selected
        mock_showerror.assert_called_with("Error", "Please select a valid report type.")

    def test_generate_report_clear_previous(self):
        # Simulate generating a report
        self.asset_reporting_page.generate_report()

        # Check if the previous report was cleared
        self.asset_reporting_page.report_text.delete.assert_called_with(1.0, tk.END)


if __name__ == "__main__":
    unittest.main()

import unittest
import tkinter as tk
from unittest.mock import Mock, patch
from asset_reporting.asset_reporting import AssetReportingPage
from vehicle_management_task.database import VehicleDatabase


class TestAssetReportingPage(unittest.TestCase):

    def setUp(self):
        """Set up a test environment for AssetReportingPage"""
        self.root = tk.Tk()
        self.db = Mock(spec=VehicleDatabase)
        
        # Mock query_vehicles to return fake data
        self.db.query_vehicles.return_value = [
            ("1", "Toyota", "Corolla", "2020", "Sedan", "Petrol", "01-01-22", "01-01-23", "Tax Paid"),
            ("2", "Ford", "Focus", "2015", "Hatchback", "Diesel", "05-03-21", "02-02-22", "Tax Due"),
        ]
        
        self.asset_page = AssetReportingPage(self.root, self.db)

    def tearDown(self):
        """Destroy Tkinter root window after each test"""
        self.root.destroy()

    def test_create_widgets(self):
        """Test if widgets are properly created"""
        self.assertIsInstance(self.asset_page.title_label, tk.Label)
        self.assertIsInstance(self.asset_page.report_dropdown, tk.OptionMenu)
        self.assertIsInstance(self.asset_page.generate_button, tk.Button)
        self.assertIsInstance(self.asset_page.report_text, tk.Text)

    def test_generate_report_all_vehicles(self):
        """Test generating 'All Vehicles' report"""
        self.asset_page.report_var.set("All Vehicles")
        self.asset_page.generate_report()
        
        self.db.query_vehicles.assert_called_once_with("SELECT * FROM vehicles")
        self.assertGreater(len(self.asset_page.vehicles), 0)  # Ensure vehicles list is populated
        self.assertIn("Toyota", self.asset_page.report_text.get("1.0", "end"))

    def test_generate_report_tax_due(self):
        """Test generating 'Vehicles with Tax Due' report"""
        self.asset_page.report_var.set("Vehicles with Tax Due")
        self.asset_page.generate_report()
        
        self.db.query_vehicles.assert_called_once()
        self.assertIn("Tax Due", self.asset_page.report_text.get("1.0", "end"))

    def test_generate_report_invalid_selection(self):
        """Test generating report with an invalid selection"""
        self.asset_page.report_var.set("Invalid Report")
        
        with patch('asset_management.ui_components.UIComponents.show_status_popup') as mock_popup:
            self.asset_page.generate_report()
            mock_popup.assert_called_once_with("Error", "Please select a valid report type.")

    def test_display_report(self):
        """Test the report display functionality"""
        self.asset_page.vehicles = [
            ("1", "Toyota", "Corolla", "2020", "Sedan", "Petrol", "01-01-22", "01-01-23", "Tax Paid"),
        ]
        
        self.asset_page.display_report()
        content = self.asset_page.report_text.get("1.0", "end")
        
        self.assertIn("Toyota", content)
        self.assertIn("Corolla", content)

    def test_generate_custom_report(self):
        """Test generating a custom report with user-defined filters"""
        self.asset_page.custom_report()

        # Simulate user input in filters
        self.asset_page.filters["Make"].insert(0, "Toyota")
        self.asset_page.filters["Year"].insert(0, "2020")

        with patch.object(self.db, 'query_vehicles', return_value=[("1", "Toyota", "Corolla", "2020", "Sedan", "Petrol", "01-01-22", "01-01-23", "Tax Paid")]) as mock_query:
            self.asset_page.generate_custom_report()
            mock_query.assert_called_once()
            self.assertIn("Toyota", self.asset_page.report_text.get("1.0", "end"))

    def test_confirm_export_to_csv_no_data(self):
        """Test attempting to export without data"""
        self.asset_page.vehicles = []
        with patch("tkinter.messagebox.showerror") as mock_error:
            self.asset_page.confirm_export_to_csv()
            mock_error.assert_called_once_with("Error", "No report data available to export.")

    def test_confirm_export_to_csv_with_data(self):
        """Test confirming export to CSV when data is available"""
        self.asset_page.vehicles = [("1", "Toyota", "Corolla", "2020", "Sedan", "Petrol", "01-01-22", "01-01-23", "Tax Paid")]
        
        with patch("tkinter.messagebox.askyesno", return_value=True) as mock_confirm, \
             patch.object(self.asset_page, 'export_to_csv') as mock_export:
            self.asset_page.confirm_export_to_csv()
            mock_confirm.assert_called_once_with("Export to CSV", "Do you want to export the report to a CSV file?")
            mock_export.assert_called_once()

    def test_export_to_csv(self):
        """Test exporting report data to a CSV file without requiring user interaction."""
        self.asset_page.vehicles = [
            ("1", "Toyota", "Corolla", "2020", "Sedan", "Petrol", "01-01-22", "01-01-23", "Tax Paid"),
        ]

        with patch("tkinter.filedialog.asksaveasfilename", return_value="test_report.csv"), \
            patch("builtins.open", unittest.mock.mock_open()) as mock_open, \
            patch("csv.writer") as mock_csv_writer, \
            patch("tkinter.messagebox.showinfo") as mock_showinfo:  # Mock the popup to prevent it from appearing
            
            self.asset_page.export_to_csv()
            
            # Assertions
            mock_open.assert_called_once_with("test_report.csv", mode="w", newline="")
            mock_csv_writer.return_value.writerow.assert_any_call(["ID", "Make", "Model", "Year", "Type", "Fuel", "Service Date", "Tax Due Date", "Tax Status"])
            mock_csv_writer.return_value.writerow.assert_any_call(("1", "Toyota", "Corolla", "2020", "Sedan", "Petrol", "01-01-22", "01-01-23", "Tax Paid"))

            # Ensure messagebox was triggered, but no interaction is needed
            mock_showinfo.assert_called_once_with("Success", "Report successfully exported to test_report.csv")

    def test_custom_report_creates_filters(self):
        """Test custom report filters are correctly created"""
        self.asset_page.custom_report()
        self.assertIn("Make", self.asset_page.filters)
        self.assertIn("Year", self.asset_page.filters)
        self.assertIn("Tax Status", self.asset_page.filters)

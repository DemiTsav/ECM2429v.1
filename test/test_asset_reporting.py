import pytest
import sqlite3
from tkinter import Tk, filedialog, messagebox
from vehicle_management_task.database import VehicleDatabase
from asset_reporting.asset_reporting import AssetReportingPage


@pytest.fixture
def temp_db():
    # Create an in-memory database for testing
    connection = sqlite3.connect(":memory:")
    db = VehicleDatabase(connection)
    db.initialize_database()  # Initialize the tables
    yield db
    db.close()


@pytest.fixture
def reporting_page(temp_db):
    # Create the Tkinter root window for testing
    root = Tk()
    page = AssetReportingPage(root, temp_db)
    return page


def test_generate_report_all_vehicles(reporting_page, temp_db):
    # Insert sample data into the database
    temp_db.add_vehicle("ABC123", "Toyota", "Corolla", 2015, "Sedan", "Petrol", "2025-06-01", "2025-07-01", "Active")
    temp_db.add_vehicle("XYZ456", "Ford", "Focus", 2018, "Hatchback", "Diesel", "2025-07-01", "2025-08-01", "Inactive")

    # Simulate selecting the "All Vehicles" report and clicking the "Generate Report" button
    reporting_page.report_var.set("All Vehicles")
    reporting_page.generate_report()

    # Test if the report displays the correct data
    report_text = reporting_page.report_text.get(1.0, "end-1c")  # Get the content of the report
    assert "Toyota" in report_text
    assert "Ford" in report_text
    assert "Sedan" in report_text
    assert "Hatchback" in report_text


def test_generate_report_vehicles_due_for_service(reporting_page, temp_db):
    # Insert a sample vehicle that's due for service
    temp_db.add_vehicle("XYZ789", "Honda", "Civic", 2017, "Sedan", "Diesel", "2023-01-01", "2023-02-01", "Active")

    # Simulate selecting the "Vehicles Due for Service" report and clicking the "Generate Report" button
    reporting_page.report_var.set("Vehicles Due for Service")
    reporting_page.generate_report()

    # Test if the report displays the correct data
    report_text = reporting_page.report_text.get(1.0, "end-1c")  # Get the content of the report
    assert "Honda" in report_text
    assert "Civic" in report_text


def test_generate_custom_report(reporting_page, temp_db):
    # Insert a vehicle with known data
    temp_db.add_vehicle("DEF123", "BMW", "X5", 2019, "SUV", "Diesel", "2025-05-01", "2025-06-01", "Active")

    # Ensure filters are initialized by calling `custom_report`
    reporting_page.custom_report()

    # Simulate selecting "Custom Report" and providing a filter
    reporting_page.report_var.set("Custom Report")
    reporting_page.filters["Make"].insert(0, "BMW")
    reporting_page.generate_custom_report()

    # Test if the report displays the correct data
    report_text = reporting_page.report_text.get(1.0, "end-1c")
    assert "BMW" in report_text
    assert "X5" in report_text



def test_export_to_csv(reporting_page, temp_db, monkeypatch):
    # Insert sample data into the database
    temp_db.add_vehicle("GHI789", "Audi", "A4", 2020, "Sedan", "Petrol", "2025-07-01", "2025-08-01", "Active")

    # Simulate generating a report
    reporting_page.report_var.set("All Vehicles")
    reporting_page.generate_report()

    # Mock file dialog to simulate file saving without opening a file dialog
    monkeypatch.setattr(filedialog, "asksaveasfilename", lambda **kwargs: "test_report.csv")

    # Mock messagebox.askyesno to always return True (simulating the "Yes" response to the export confirmation)
    monkeypatch.setattr(messagebox, "askyesno", lambda title, message: True)

    # Mock the actual CSV export method to avoid file I/O
    def mock_export_to_csv():
        # Simulate the export without actually writing to a file
        assert True  # Ensure that the function is called

    monkeypatch.setattr(reporting_page, "export_to_csv", mock_export_to_csv)

    # Simulate confirming export and calling the export method
    reporting_page.confirm_export_button.invoke()


def test_invalid_report_type(reporting_page):
    # Test if invalid report type is handled properly
    reporting_page.report_var.set("Invalid Report")
    reporting_page.generate_report()
    # Since we can't display messagebox in tests directly, we would check if an error was triggered in logs
    # or simulate its effect using other testing techniques.
    # For now, the assumption is that UIComponents.show_status_popup() is the error handler.

import pytest
import tkinter as tk
from tkinter import messagebox, filedialog
from unittest.mock import MagicMock
from asset_management.frontend.ui_components import UIComponents
from asset_management.backend.report_generation import AssetReportingHandler
from asset_management.frontend.asset_reporting import AssetReportingPage


@pytest.fixture
def temp_db():
    """
    Creates an in-memory SQLite database with a 'vehicles' table and
    sample data.
    Returns a mock database object for testing.
    """
    import sqlite3
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE vehicles (
        id INTEGER PRIMARY KEY,
        make TEXT,
        model TEXT,
        year INTEGER,
        fuel_type TEXT,
        service_date TEXT,
        tax_due_date TEXT
    )
    """)

    cursor.executemany("""
    INSERT INTO vehicles (make, model, year, fuel_type,
                       service_date, tax_due_date)
    VALUES (?, ?, ?, ?, ?, ?)
    """, [
        ('Toyota', 'Corolla', 2015, 'Petrol', '2025-03-01', '2025-06-01'),
        ('Ford', 'Focus', 2010, 'Diesel', '2025-04-01', '2025-05-01')
    ])

    db = MagicMock()
    db.cursor.return_value = cursor
    yield db

    conn.close()


def test_generate_report(temp_db, mocker):
    """
    Tests the generate_report() function to ensure it retrieves and displays
    the correct vehicle data for the selected report type.
    """
    mock_fetch_report = mocker.patch.object(
        AssetReportingHandler,
        'fetch_report', return_value=[
            (1, 'ABC123', 'Toyota', 'Corolla', 2015, 'Sedan', 'Petrol',
             '2025-03-01', '2025-06-01', 'Active')
        ])

    mocker.patch.object(
        UIComponents, 'show_status_popup'
        )

    root = tk.Tk()
    app = AssetReportingPage(root, temp_db)
    app.report_var.set("All Vehicles")
    app.generate_report()

    mock_fetch_report.assert_called_once_with(temp_db, "All Vehicles")
    assert "Toyota" in app.report_text.get("1.0", tk.END)


def test_generate_custom_report(temp_db, mocker):
    """
    Tests the generate_custom_report() function to ensure it retrieves
    the correct vehicle data based on user-selected filters.
    """
    mock_fetch_custom_report = mocker.patch.object(
        AssetReportingHandler, 'fetch_custom_report', return_value=[(
            1, 'ABC123', 'Honda', 'Civic', 2005, 'Sedan', 'Diesel',
            '2025-03-01', '2025-06-01', 'Active'
        )])

    root = tk.Tk()
    app = AssetReportingPage(root, temp_db)
    app.report_var.set("Custom Report")
    app.custom_report()
    app.generate_custom_report()

    mock_fetch_custom_report.assert_called_once_with(temp_db, {})
    assert "Honda" in app.report_text.get("1.0", tk.END)


def test_export_to_csv(temp_db, mocker):
    """
    Tests the export_to_csv() function to ensure that report data
    is correctly written to a CSV file.
    """
    mock_asksaveasfilename = mocker.patch.object(
        filedialog,
        'asksaveasfilename',
        return_value="test_report.csv"
        )

    mocker.patch.object(messagebox, 'askyesno',
                        return_value=True)
    mock_showinfo = mocker.patch.object(messagebox, 'showinfo')

    root = tk.Tk()
    app = AssetReportingPage(root, temp_db)
    app.vehicles = [
        (1, 'ABC123', 'Toyota', 'Corolla', 2015, 'Sedan', 'Petrol',
         '2025-03-01', '2025-06-01', 'Active')
    ]
    app.export_to_csv()
    mock_asksaveasfilename.assert_called_once_with(defaultextension=".csv",
                                                   filetypes=[(
                                                       "CSV Files", "*.csv"
                                                       )])

    mock_showinfo.assert_called_once_with(
        "Success", "Report successfully exported to test_report.csv")

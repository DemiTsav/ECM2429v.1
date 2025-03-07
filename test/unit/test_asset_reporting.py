import pytest
import sqlite3
from asset_management.database import VehicleDatabase
from asset_management.frontend.asset_reporting import AssetReportingHandler


@pytest.fixture
def temp_db():
    """Creates an in-memory SQLite database with a 'vehicles' table and sample
    data."""
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
    INSERT INTO vehicles (make, model, year, fuel_type, service_date,
                       tax_due_date)
    VALUES (?, ?, ?, ?, ?, ?)
    """, [
        ('Toyota', 'Corolla', 2015, 'Petrol', '2025-03-01', '2025-06-01'),
        ('Ford', 'Focus', 2010, 'Diesel', '2025-04-01', '2025-05-01'),
        ('Honda', 'Civic', 2005, 'Diesel', '2025-02-15', '2025-05-01'),
        ('BMW', 'X5', 2000, 'Petrol', '2025-06-01', '2025-07-01')
    ])

    db = VehicleDatabase(conn)
    yield db

    conn.close()


def test_get_report_query():
    """Tests if get_report_query() returns the correct SQL queries based on
    the report type."""
    assert (AssetReportingHandler.get_report_query("All Vehicles") ==
            "SELECT * FROM vehicles")
    assert (AssetReportingHandler.get_report_query(
            "Vehicles Due for Service") ==
            ("SELECT * FROM vehicles WHERE service_date <= "
             "date('now', '+1 month')"))
    assert (AssetReportingHandler.get_report_query(
            "Vehicles with Tax Due") ==
            ("SELECT * FROM vehicles WHERE tax_due_date <= "
             "date('now', '+1 month')"))
    assert (AssetReportingHandler.get_report_query(
            "Vehicles Older Than 10 Years") ==
            "SELECT * FROM vehicles WHERE year <= strftime('%Y', 'now') - 10")
    assert (AssetReportingHandler.get_report_query("Diesel Vehicles") ==
            "SELECT * FROM vehicles WHERE LOWER(fuel_type) = LOWER('Diesel')")
    assert (AssetReportingHandler.get_report_query(
        "Nonexistent Report") is None)


def test_fetch_report(temp_db, mocker):
    """Tests if fetch_report() retrieves the correct data for a given report#
    type."""
    mock_fetch_report = mocker.patch.object(
        AssetReportingHandler,
        'fetch_report',
        return_value=[(1, 'Toyota', 'Corolla', 2015, 'Petrol', '2025-03-01')]
    )

    report = AssetReportingHandler.fetch_report(temp_db, "All Vehicles")

    assert len(report) == 1
    assert report[0][1] == 'Toyota'

    mock_fetch_report.assert_called_once_with(temp_db, "All Vehicles")


def test_fetch_custom_report(temp_db, mocker):
    """Tests if fetch_custom_report() correctly filters vehicles based on
    given criteria."""
    filters = {"Fuel Type": "Diesel"}
    report = AssetReportingHandler.fetch_custom_report(temp_db, filters)
    assert len(report) == 2
    assert report[0][1] == 'Ford'
    assert report[1][1] == 'Honda'

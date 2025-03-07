import pytest
import sqlite3
from asset_management.database import VehicleDatabase


@pytest.fixture
def db():
    """
    Creates an in-memory SQLite database and initializes the VehicleDatabase
    instance.
    Yields the database instance for testing and ensures proper cleanup after
    tests.
    """
    test_db = sqlite3.connect(":memory:")
    vehicle_db = VehicleDatabase(test_db)
    yield vehicle_db
    vehicle_db.close()


def test_initialize_database(db):
    """
    Tests whether the 'vehicles' table is created successfully upon database
    initialization.
    """
    db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'"
                      "AND name='vehicles'")
    table = db.cursor.fetchone()
    assert table is not None


def test_add_vehicle(db):
    """
    Tests the add_vehicle() function by inserting a vehicle into the database
    and verifying its details.
    """
    db.add_vehicle("ABC123", "Toyota", "Corolla", 2020, "Sedan", "Petrol",
                   "2023-05-01", "2025-05-01", "Paid")
    vehicle = db.get_vehicle(1)
    assert vehicle is not None
    assert vehicle["Registration"] == "ABC123"
    assert vehicle["Make"] == "Toyota"
    assert vehicle["Year"] == 2020


def test_get_all_vehicles(db):
    """
    Tests get_all_vehicles() to ensure it retrieves all vehicles correctly.
    """
    db.add_vehicle("ABC123", "Toyota", "Corolla", 2020, "Sedan", "Petrol",
                   "2023-05-01", "2025-05-01", "Paid")
    db.add_vehicle("XYZ456", "Honda", "Civic", 2022, "Sedan", "Diesel",
                   "2023-08-01", "2025-08-01", "Unpaid")
    vehicles = db.get_all_vehicles()
    assert len(vehicles) == 2


def test_update_vehicle(db):
    """
    Tests update_vehicle() by modifying a vehicle's details and verifying the
    changes.
    """
    db.add_vehicle("ABC123", "Toyota", "Corolla", 2020, "Sedan", "Petrol",
                   "2023-05-01", "2025-05-01", "Paid")
    db.update_vehicle(1, {"Year": 2021, "Tax Status": "Unpaid"})
    updated_vehicle = db.get_vehicle(1)
    assert updated_vehicle["Year"] == 2021
    assert updated_vehicle["Tax Status"] == "Unpaid"


def test_delete_vehicle(db):
    """
    Tests delete_vehicle() by removing a vehicle and ensuring it no longer
    exists.
    """
    db.add_vehicle("ABC123", "Toyota", "Corolla", 2020, "Sedan", "Petrol",
                   "2023-05-01", "2025-05-01", "Paid")
    db.delete_vehicle(1)
    vehicle = db.get_vehicle(1)
    assert vehicle is None


def test_query_vehicles(db):
    """
    Tests query_vehicles() by executing a SQL query to retrieve vehicles
    based on a condition.
    """
    db.add_vehicle("ABC123", "Toyota", "Corolla", 2020, "Sedan", "Petrol",
                   "2023-05-01", "2025-05-01", "Paid")
    results = db.query_vehicles("SELECT * FROM vehicles WHERE make = ?",
                                ("Toyota",))
    assert len(results) == 1
    assert results[0][2] == "Toyota"


def test_close_connection(db):
    """
    Tests close() by ensuring that database operations cannot be performed
    after closure.
    """
    db.close()
    with pytest.raises(sqlite3.ProgrammingError):
        db.cursor.execute("SELECT * FROM vehicles")

import pytest
import sqlite3
from asset_management.asset_management_page import AssetManagementPage
from vehicle_management_task.database import VehicleDatabase

@pytest.fixture
def temp_db():
    # Create an in-memory SQLite database
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()

    # Create the table structure
    cursor.execute("""
    CREATE TABLE vehicles (
        id INTEGER PRIMARY KEY,
        registration TEXT,
        make TEXT,
        model TEXT,
        year INTEGER,
        vehicle_type TEXT,
        fuel_type TEXT,
        service_date TEXT,
        tax_due_date TEXT,
        tax_status TEXT
    )
    """)

    # Insert sample data into the vehicles table
    cursor.executemany("""
    INSERT INTO vehicles (registration, make, model, year, vehicle_type, fuel_type, service_date, tax_due_date, tax_status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        ("ABC123", "Toyota", "Corolla", 2020, "Sedan", "Petrol", "2025-01-01", "2025-06-01", "Tax Paid"),
        ("XYZ789", "Honda", "Civic", 2021, "Sedan", "Diesel", "2025-03-01", "2025-08-01", "Tax Due"),
    ])

    conn.commit()

    # Return the connection object and database cursor for use in tests
    yield conn, cursor

    # Close the connection after test
    conn.close()

def test_show_all_vehicles(temp_db, monkeypatch):
    conn, cursor = temp_db
    db = VehicleDatabase(conn)
    
    # Mocking the method show_all_vehicles from AssetManagementPage
    def mock_show_all_vehicles(self):
        return [
            {"id": 1, "registration": "ABC123", "make": "Toyota", "model": "Corolla"},
            {"id": 2, "registration": "XYZ789", "make": "Honda", "model": "Civic"},
        ]
    
    monkeypatch.setattr(AssetManagementPage, 'show_all_vehicles', mock_show_all_vehicles)

    # Now run the test
    app = AssetManagementPage(None, db)
    vehicles = app.show_all_vehicles()
    
    assert len(vehicles) == 2
    assert vehicles[0]["registration"] == "ABC123"
    assert vehicles[1]["make"] == "Honda"

def test_show_add_vehicle_form(monkeypatch):
    # Mocking the method show_add_vehicle_form from AssetManagementPage
    def mock_show_add_vehicle_form(self):
        return {"make": "Toyota", "model": "Corolla", "year": 2020}

    monkeypatch.setattr(AssetManagementPage, 'show_add_vehicle_form', mock_show_add_vehicle_form)
    
    db = VehicleDatabase(":memory:")  # Simulating an empty database connection
    app = AssetManagementPage(None, db)
    form = app.show_add_vehicle_form()
    
    assert form["make"] == "Toyota"
    assert form["model"] == "Corolla"

def test_process_add_vehicle(monkeypatch):
    # Mocking process_add_vehicle from VehicleProcess
    def mock_process_add_vehicle(vehicle_data):
        return {"status": "success", "vehicle": vehicle_data}
    
    monkeypatch.setattr("asset_management.vehicle_processes.VehicleProcess.process_add_vehicle", mock_process_add_vehicle)
    
    vehicle_data = {"registration": "DEF456", "make": "Ford", "model": "Fiesta", "year": 2022}
    result = mock_process_add_vehicle(vehicle_data)
    
    assert result["status"] == "success"
    assert result["vehicle"]["registration"] == "DEF456"

def test_delete_vehicle_prompt(monkeypatch):
    # Mocking the delete_vehicle_prompt from AssetManagementPage
    def mock_delete_vehicle_prompt(self, vehicle_id):
        return {"status": "deleted", "vehicle_id": vehicle_id}
    
    monkeypatch.setattr(AssetManagementPage, 'delete_vehicle_prompt', mock_delete_vehicle_prompt)
    
    db = VehicleDatabase(":memory:")  # Simulating an empty database connection
    app = AssetManagementPage(None, db)
    result = app.delete_vehicle_prompt(1)
    
    assert result["status"] == "deleted"
    assert result["vehicle_id"] == 1

# New test: Testing update_vehicle_form method
def test_show_update_vehicle_form(monkeypatch):
    # Mocking the show_update_vehicle_form from AssetManagementPage
    def mock_show_update_vehicle_form(self, vehicle_id):
        return {
            "id": vehicle_id,
            "registration": "ABC123",
            "make": "Toyota",
            "model": "Corolla",
            "year": 2020
        }

    monkeypatch.setattr(AssetManagementPage, 'show_update_vehicle_form', mock_show_update_vehicle_form)

    db = VehicleDatabase(":memory:")  # Simulating an empty database connection
    app = AssetManagementPage(None, db)
    form = app.show_update_vehicle_form(1)
    
    assert form["registration"] == "ABC123"
    assert form["make"] == "Toyota"
    assert form["model"] == "Corolla"
    assert form["year"] == 2020

# New test: Testing process_update_vehicle method
def test_process_update_vehicle(monkeypatch):
    # Mocking process_update_vehicle from VehicleProcess
    def mock_process_update_vehicle(vehicle_id, updated_data):
        return {"status": "success", "updated_vehicle": updated_data}
    
    monkeypatch.setattr("asset_management.vehicle_processes.VehicleProcess.process_update_vehicle", mock_process_update_vehicle)
    
    updated_data = {
        "registration": "XYZ987",
        "make": "Honda",
        "model": "Civic",
        "year": 2021
    }
    result = mock_process_update_vehicle(1, updated_data)
    
    assert result["status"] == "success"
    assert result["updated_vehicle"]["registration"] == "XYZ987"
    assert result["updated_vehicle"]["make"] == "Honda"
    assert result["updated_vehicle"]["model"] == "Civic"
    assert result["updated_vehicle"]["year"] == 2021

import pytest
from asset_management.vehicle_processes import VehicleProcess
from asset_management.ui_components import UIComponents
from asset_management.field_validations import FieldValidations
from vehicle_management_task.database import VehicleDatabase
from asset_management.asset_management_page import AssetManagementPage


@pytest.fixture
def mock_db():
    db = VehicleDatabase("test.db")  # Use a separate test database for pytest
    yield db
    db.close()  # Close the database after test


@pytest.fixture
def vehicle_process(mock_db):
    return VehicleProcess(mock_db)


# Test - Add Vehicle (Success)
def test_process_add_vehicle_success(vehicle_process, mock_db):
    # Simulate data entries
    entries = {
        "Make": "Toyota",
        "Model": "Corolla",
        "Year": "2020",
        "Vehicle Type": "Sedan",
        "Fuel Type": "Petrol",
        "Service Date": "01-01-22",
        "Tax Due Date": "01-01-23",
    }
    tax_status = "SORN"

    # Call method
    vehicle_process.process_add_vehicle(entries, tax_status)

    # Check if vehicle was added to the DB
    vehicle = mock_db.get_vehicle_by_make_and_model("Toyota", "Corolla")
    assert vehicle is not None
    assert vehicle['Year'] == "2020"


# Test - Add Vehicle (Validation Errors)
def test_process_add_vehicle_validation_errors(vehicle_process):
    # Simulate data entries with validation errors
    entries = {"Make": "", "Model": "Corolla"}
    tax_status = "Taxed"
    
    result = vehicle_process.process_add_vehicle(entries, tax_status)
    
    assert result == "Make cannot be empty."


# Test - Update Vehicle (Success)
def test_process_update_vehicle_success(vehicle_process, mock_db):
    # Simulate updating a vehicle with new details
    vehicle_process.update_entries = {
        "Make": {"entry": "Toyota", "checkbox": True}
    }
    vehicle_process.process_update_vehicle("123")

    # Check if update was successful in DB
    updated_vehicle = mock_db.get_vehicle_by_id("123")
    assert updated_vehicle["Make"] == "Toyota"


# Test - Delete Vehicles (Success)
def test_process_delete_vehicles_success(vehicle_process, mock_db):
    # Simulate deleting vehicles
    vehicle_ids = ["123", "456"]
    vehicle_process.process_delete_vehicles(vehicle_ids)

    # Check if vehicles are deleted
    for vehicle_id in vehicle_ids:
        vehicle = mock_db.get_vehicle_by_id(vehicle_id)
        assert vehicle is None

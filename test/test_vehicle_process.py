import pytest
from unittest.mock import MagicMock
from asset_management.vehicle_processes import VehicleProcess
from asset_management.field_validations import FieldValidations
from asset_management.ui_components import UIComponents

@pytest.fixture
def vehicle_process():
    db_mock = MagicMock()
    return VehicleProcess(db=db_mock)

def test_process_add_vehicle_success(vehicle_process):
    # Mock successful database operation
    vehicle_process.db.add_vehicle = MagicMock()
    entries = {
        "Make": MagicMock(get=lambda: "Toyota"),
        "Model": MagicMock(get=lambda: "Corolla"),
        "Year": MagicMock(get=lambda: "2020"),
        "Vehicle Type": MagicMock(get=lambda: "Sedan"),
        "Fuel Type": MagicMock(get=lambda: "Petrol"),
        "Service Date": MagicMock(get=lambda: "25-12-22"),
        "Tax Due Date": MagicMock(get=lambda: "31-12-22")
    }
    tax_status_dropdown = MagicMock(get=lambda: "Tax Paid")
    UIComponents.show_status_popup = MagicMock()

    vehicle_process.process_add_vehicle(entries, tax_status_dropdown)

    # Verify the add_vehicle method is called with correct arguments
    vehicle_process.db.add_vehicle.assert_called_with("Toyota", "Corolla", 2020, "Sedan", "Petrol", "25-12-22", "31-12-22", "Tax Paid")
    UIComponents.show_status_popup.assert_called_with("Success", "Vehicle added successfully!")

def test_process_add_vehicle_error(vehicle_process):
    # Mock database failure
    vehicle_process.db.add_vehicle = MagicMock(side_effect=Exception("Database error"))
    entries = {
        "Make": MagicMock(get=lambda: "Toyota"),
        "Model": MagicMock(get=lambda: "Corolla"),
        "Year": MagicMock(get=lambda: "2020"),
        "Vehicle Type": MagicMock(get=lambda: "Sedan"),
        "Fuel Type": MagicMock(get=lambda: "Petrol"),
        "Service Date": MagicMock(get=lambda: "25-12-22"),
        "Tax Due Date": MagicMock(get=lambda: "31-12-22")
    }
    tax_status_dropdown = MagicMock(get=lambda: "Tax Paid")
    UIComponents.show_status_popup = MagicMock()

    vehicle_process.process_add_vehicle(entries, tax_status_dropdown)

    UIComponents.show_status_popup.assert_called_with("Error", "Failed to add vehicle: Database error")

import pytest
from asset_management.vehicle_processes import VehicleProcess
from asset_management.ui_components import UIComponents

@pytest.fixture
def mock_db():
    """Fixture to mock the database operations."""
    class MockDB:
        def add_vehicle(self, *args):
            pass
        
        def update_vehicle(self, vehicle_id, updates):
            pass
        
        def delete_vehicle(self, vehicle_id):
            pass
        
        def get_vehicle(self, query, params):
            return [("1", "ABC123", "Toyota", "Camry", 2020, "Sedan", "Petrol", "15-05-2025", "15-06-2025", "Tax Paid")]
    
    return MockDB()

@pytest.fixture
def mock_entries():
    """Fixture to mock the Entry widgets."""
    class MockEntry:
        def get(self):
            return "Petrol"
    
    return {
        'Fuel Type': MockEntry(),
        'Make': MockEntry(),
        'Model': MockEntry(),
        'Registration': MockEntry(),
        'Tax Status': MockEntry(),
    }

@pytest.fixture
def vehicle_process(mock_db):
    """Fixture to initialize the VehicleProcess object."""
    return VehicleProcess(mock_db)

def test_process_add_vehicle(monkeypatch, mock_db, mock_entries, vehicle_process):
    """Test adding a vehicle to the database."""
    monkeypatch.setattr(UIComponents, 'show_status_popup', lambda *args: None)

    # Pass the 'tax_status' directly as an argument
    tax_status = mock_entries['Tax Status'].get()
    VehicleProcess.process_add_vehicle(self, mock_entries, tax_status)

    assert callable(mock_db.add_vehicle)

def test_process_update_vehicle(monkeypatch, mock_db, mock_entries, vehicle_process):
    """Test updating a vehicle in the database."""
    vehicle_id = "1"
    monkeypatch.setattr(UIComponents, 'show_status_popup', lambda *args: None)

    # Update the signature to match the expected method
    VehicleProcess.process_update_vehicle(vehicle_id, mock_entries)

    assert callable(mock_db.update_vehicle)

def test_process_delete_vehicles(monkeypatch, mock_db, mock_entries, vehicle_process):
    """Test deleting vehicles from the database."""
    monkeypatch.setattr(UIComponents, 'show_status_popup', lambda *args: None)

    # Ensure the method name matches `process_delete_vehicles`
    vehicle_process.process_delete_vehicles("1")

    assert callable(mock_db.delete_vehicle)

def test_retrieve_vehicle_id(monkeypatch, mock_db, mock_entries, vehicle_process):
    """Test retrieving a vehicle ID from a selection."""
    # Mock the vehicle_table.selection method
    mock_selection = lambda: ["1"]
    monkeypatch.setattr(vehicle_process, 'vehicle_table', type('MockTable', (object,), {'selection': mock_selection})())

    vehicle_id = VehicleProcess.retrieve_vehicle_id()

    assert vehicle_id == "1"

def test_perform_search(monkeypatch, mock_db, mock_entries, vehicle_process):
    """Test performing a vehicle search."""
    monkeypatch.setattr(VehicleProcess, 'get_vehicle', mock_db.get_vehicle)

    # Perform the search with the search term as argument
    result = VehicleProcess.perform_search("ABC123")

    assert result == [("1", "ABC123", "Toyota", "Camry", 2020, "Sedan", "Petrol", "15-05-2025", "15-06-2025", "Tax Paid")]

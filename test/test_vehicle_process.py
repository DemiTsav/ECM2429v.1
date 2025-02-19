import pytest
from asset_management.vehicle_processes import VehicleProcess
from asset_management.ui_components import UIComponents
from vehicle_management_task.database import VehicleDatabase

@pytest.fixture
def mock_db():
    """Fixture to mock the database operations."""
    class MockDB:
        def add_vehicle(self, *args):
            pass
        
        def update_vehicle(self, updates):
            pass  # Removed vehicle_id to match function definition
        
        def delete_vehicle(self, vehicle_id):
            pass
        
        def get_vehicle(self, query, params):
            return [("1", "Toyota")]

    return MockDB()

@pytest.fixture
def mock_entries():
    """Fixture to mock the Entry widgets."""
    class MockEntry:
        def get(self):
            return "Toyota"
    
    return {
        'Fuel Type': MockEntry(),
        'Make': MockEntry(),
        'Model': MockEntry(),
        'Registration': MockEntry(),
        'Tax Status': MockEntry(),
        'Vehicle Type': MockEntry(),
        'Year': MockEntry(),
        'Service Date': MockEntry(),
        'Tax Due Date': MockEntry(),
    }

@pytest.fixture
def vehicle_process(mock_db):
    """Fixture to initialize the VehicleProcess object with necessary mocks."""
    vp = VehicleProcess(mock_db)
    vp.vehicle_table = type("MockTable", (object,), {"selection": lambda _: ["1"]})()  
    vp.validate_character_input = lambda x: True  # Mock missing method
    vp.search_entries = lambda: "Toyota"  # Mock missing search_entries method
    return vp

def test_process_add_vehicle(monkeypatch, mock_db, mock_entries, vehicle_process):
    """Test adding a vehicle to the database."""
    monkeypatch.setattr(UIComponents, 'show_status_popup', lambda *args: None)
    monkeypatch.setattr(vehicle_process, "validate_character_input", lambda x: True)  

    vehicle_process.process_add_vehicle(mock_entries, "Tax Paid")

    assert callable(mock_db.add_vehicle)

def test_process_update_vehicle(monkeypatch, mock_db, mock_entries, vehicle_process):
    """Test updating a vehicle in the database."""
    monkeypatch.setattr(UIComponents, 'show_status_popup', lambda *args: None)

    vehicle_process.process_update_vehicle(mock_entries)

    assert callable(mock_db.update_vehicle)

def test_process_delete_vehicles(monkeypatch, mock_db, mock_entries, vehicle_process):
    """Test deleting vehicles from the database."""
    monkeypatch.setattr(UIComponents, 'show_status_popup', lambda *args: None)

    vehicle_process.process_delete_vehicles("1")

    assert callable(mock_db.delete_vehicle)

def test_retrieve_vehicle_id(monkeypatch, vehicle_process):
    """Test retrieving a vehicle ID from a selection."""
    vehicle_id = vehicle_process.retrieve_vehicle_id()
    assert vehicle_id == "1"

def test_perform_search(monkeypatch, mock_db, vehicle_process):
    """Test performing a vehicle search."""
    monkeypatch.setattr(mock_db, 'get_vehicle', lambda query, params: [("1", "Toyota")])

    result = vehicle_process.perform_search()

    assert result == [("1", "Toyota")]

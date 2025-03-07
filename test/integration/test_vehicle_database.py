import pytest
from asset_management.database import VehicleDatabase


@pytest.fixture
def db():
    """Creates an in-memory database for testing."""
    db = VehicleDatabase(":memory:")
    yield db
    db.close()


def test_database_integration(db):
    """Ensure adding and retrieving a vehicle works correctly."""
    db.add_vehicle("ABC123", "Toyota", "Corolla", 2015, "SUV", "Diesel",
                   "11-02-2024", "30-01-2025", "Tax Paid")
    vehicles = db.get_all_vehicles()
    assert len(vehicles) == 1
    assert vehicles[0][1] == "ABC123"
    assert vehicles[0][2] == "Toyota"

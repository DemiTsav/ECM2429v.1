import pytest
import sqlite3
from asset_management.database import VehicleDatabase
from asset_management.backend.field_validations import FieldValidations
from asset_management.frontend.ui_components import UIComponents
from asset_management.backend.asset_management_handler import VehicleController


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    conn = sqlite3.connect(":memory:")
    db = VehicleDatabase(conn)
    db.initialize_database()
    yield db
    conn.close()


@pytest.fixture
def vehicle_table(mocker):
    """Mock the vehicle table (Treeview)."""
    return mocker.Mock()


@pytest.fixture
def vehicle_controller(temp_db, vehicle_table):
    """Instantiate VehicleController with temporary DB and mock table."""
    return VehicleController(temp_db, vehicle_table)


@pytest.fixture
def mock_ui_components(mocker):
    """Mock UIComponents methods."""
    mocker.patch.object(UIComponents, "show_status_popup")
    mocker.patch.object(UIComponents, "display_vehicle_info")
    mocker.patch.object(UIComponents, "create_button")


@pytest.fixture
def mock_validations(mocker):
    """Mock FieldValidations methods."""
    mocker.patch.object(FieldValidations, "validations", return_value=[])
    mocker.patch.object(FieldValidations, "update_validations",
                        return_value=[])


@pytest.fixture
def mock_callbacks(mocker):
    """Mock callback functions."""
    return mocker.Mock(), mocker.Mock()


def test_add_vehicle(vehicle_controller, mock_validations, mock_ui_components,
                     mock_callbacks, monkeypatch, mocker):
    """Test adding a vehicle successfully."""
    refresh_callback, clear_callback = mock_callbacks
    entries = {key: mocker.Mock(get=mocker.Mock(return_value=value)) for key,
               value in {
        "Registration": "ABC123",
        "Make": "Toyota",
        "Model": "Corolla",
        "Year": "2020",
        "Vehicle Type": "Sedan",
        "Fuel Type": "Petrol",
        "Service Date": "2025-01-01",
        "Tax Due Date": "2025-06-01",
    }.items()}
    tax_status = mocker.Mock(get=mocker.Mock(return_value="Valid"))

    monkeypatch.setattr(VehicleDatabase, "add_vehicle", lambda *args,
                        **kwargs: None)

    vehicle_controller.add_vehicle(
        entries,
        tax_status,
        refresh_callback,
        clear_callback
        )

    UIComponents.show_status_popup.assert_called_with(
        "Success",
        "Vehicle added successfully."
        )
    refresh_callback.assert_called_once()
    clear_callback.assert_called_once()


def test_delete_vehicle(vehicle_controller, mock_ui_components,
                        mock_callbacks, monkeypatch):
    """Test deleting a vehicle successfully."""
    refresh_callback, clear_callback = mock_callbacks
    vehicle_id = 1

    monkeypatch.setattr(VehicleDatabase, "delete_vehicle",
                        lambda *args, **kwargs: None)

    vehicle_controller.delete_vehicle(vehicle_id, refresh_callback,
                                      clear_callback)

    UIComponents.show_status_popup.assert_called_with(
        "Success",
        "Vehicle deleted successfully."
        )
    refresh_callback.assert_called_once()
    clear_callback.assert_called_once()


def test_update_vehicle(vehicle_controller, mock_validations,
                        mock_ui_components, mock_callbacks, monkeypatch,
                        mocker):
    """Test updating a vehicle successfully."""
    refresh_callback, clear_callback = mock_callbacks
    vehicle_id = "1"
    update_entries = {
        "Make": {"entry": mocker.Mock(get=mocker.Mock(return_value="Ford")),
                 "checkbox": mocker.Mock(get=mocker.Mock(return_value=True))}
    }

    monkeypatch.setattr(VehicleDatabase, "update_vehicle", lambda *args,
                        **kwargs: None)

    vehicle_controller.update_vehicle(vehicle_id, refresh_callback,
                                      clear_callback, update_entries)

    UIComponents.show_status_popup.assert_called_with(
        "Success", "Vehicle updated successfully!")
    refresh_callback.assert_called_once()
    clear_callback.assert_called_once()


def test_perform_search(vehicle_controller, monkeypatch, mocker):
    """Test performing a search."""
    mock_search_entries = {"Make": mocker.Mock(
        get=mocker.Mock(return_value="Toyota")
        )}
    mock_tax_status_var = mocker.Mock(get=mocker.Mock(return_value="Valid"))

    vehicle_controller.search_entries = mock_search_entries
    vehicle_controller.tax_status_var = mock_tax_status_var

    monkeypatch.setattr(VehicleDatabase, "query_vehicles", lambda self, query,
                        values: [(1, "ABC123", "Toyota", "Corolla", 2020)])

    results = vehicle_controller.perform_search()
    assert results == [(1, "ABC123", "Toyota", "Corolla", 2020)]


def test_get_all_vehicles(vehicle_controller, monkeypatch):
    """Test retrieving all vehicles from the database."""
    mock_vehicles = [
        {"id": 1,
         "Registration": "ABC123",
         "Make": "Toyota",
         "Model": "Corolla",
         "Year": "2020"
         },
        {"id": 2,
         "Registration": "DEF456",
         "Make": "Ford",
         "Model": "Focus",
         "Year": "2018"
         },
    ]

    monkeypatch.setattr(VehicleDatabase, "get_all_vehicles",
                        lambda self: mock_vehicles)

    vehicles = vehicle_controller.get_all_vehicles()

    assert vehicles == mock_vehicles
    assert isinstance(vehicles, list)
    assert len(vehicles) == 2
    assert vehicles[0]["Make"] == "Toyota"
    assert vehicles[1]["Model"] == "Focus"


def test_add_vehicle_with_validation_errors(vehicle_controller,
                                            mock_callbacks, mocker):
    """Test adding a vehicle when validations return errors."""
    refresh_callback, clear_callback = mock_callbacks
    entries = {key: mocker.Mock(get=mocker.Mock(return_value=value)) for key,
               value in {
        "Registration": "ABC123",
        "Make": "Toyota",
        "Model": "Corolla",
        "Year": "2020",
        "Vehicle Type": "Sedan",
        "Fuel Type": "Petrol",
        "Service Date": "2025-01-01",
        "Tax Due Date": "2025-06-01",
    }.items()}
    tax_status = mocker.Mock(get=mocker.Mock(return_value="Valid"))

    mocker.patch.object(FieldValidations, "validations",
                        return_value=["Invalid year", "Service date required"])

    mock_show_status_popup = mocker.patch.object(
        UIComponents, "show_status_popup"
        )

    vehicle_controller.add_vehicle(entries, tax_status, refresh_callback,
                                   clear_callback)

    mock_show_status_popup.assert_called_with(
        "Success", "Invalid year\nService date required"
        )


def test_confirm_deletion(mocker):
    """Test confirming deletion with selected vehicles."""
    mock_self = mocker.Mock()
    selected_items = ["1"]
    refresh_callback = mocker.Mock()
    clear_callback = mocker.Mock()

    mock_vehicle_info = {"Make": "Toyota", "Model": "Corolla"}
    mock_vehicle_id = "1"

    mocker.patch.object(VehicleController, "retrieve_vehicle_info",
                        return_value=(mock_vehicle_info, mock_vehicle_id))

    mocker.patch.object(UIComponents, "display_vehicle_info")
    mocker.patch.object(UIComponents, "create_button")
    VehicleController.confirm_deletion(mock_self, selected_items,
                                       refresh_callback, clear_callback)

    UIComponents.display_vehicle_info.assert_called_once_with(
        mock_self,
        mock_vehicle_info
        )


def test_confirm_deletion_no_selection(mocker):
    """Test confirming deletion with no selected vehicles."""
    mock_self = mocker.Mock()
    selected_items = []
    refresh_callback = mocker.Mock()
    clear_callback = mocker.Mock()

    result = VehicleController.confirm_deletion(mock_self, selected_items,
                                                refresh_callback,
                                                clear_callback
                                                )
    assert result is False

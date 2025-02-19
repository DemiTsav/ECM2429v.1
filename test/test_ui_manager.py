import pytest
import tkinter as tk
from asset_management.backend.asset_management_handler import (
    VehicleController, VehicleDatabase
)
from asset_management.frontend.ui_manager import (
    AssetManagementUI
)


@pytest.fixture
def temp_db():
    """Creates a temporary in-memory SQLite database."""
    db = VehicleDatabase()
    db.initialize_database()
    yield db
    db.close()


@pytest.fixture
def mock_controller(temp_db, mocker):
    """Creates a mock VehicleController with a temporary database."""
    mock = mocker.Mock(spec=VehicleController)
    mock.connection = temp_db.connection
    mock.cursor = temp_db.cursor
    mock.get_all_vehicles.return_value = [
        (1, "AB12 CDE", "Toyota", "Corolla", 2020, "Sedan",
         "Petrol", "2024-06-01", "2024-07-01", "Tax Paid")
         ]
    return mock


@pytest.fixture
def app(mock_controller):
    """Creates a Tkinter root and initializes AssetManagementUI."""
    root = tk.Tk()
    ui = AssetManagementUI(root, mock_controller)
    return ui


def test_ui_creation(app):
    assert isinstance(app, AssetManagementUI)
    assert app.controller is not None


def test_refresh_vehicle_table(app, mock_controller, mocker):
    mocker.patch.object(app.vehicle_table, 'insert')
    app.refresh_vehicle_table()
    app.vehicle_table.insert.assert_called()


def test_show_add_vehicle_form(app, mocker):
    mocker.patch.object(app, 'clear_dynamic_content')
    mocker.patch.object(app, 'refresh_vehicle_table')
    app.show_add_vehicle_form()
    app.clear_dynamic_content.assert_called_once()
    app.refresh_vehicle_table.assert_called_once()
    assert len(app.dynamic_content_frame.winfo_children()) > 0


def test_show_delete_vehicle_prompt(app, mocker):
    mocker.patch.object(app, 'clear_dynamic_content')
    mocker.patch.object(app, 'refresh_vehicle_table')
    app.vehicle_table.selection = mocker.Mock(return_value=[])
    app.show_delete_vehicle_prompt()
    app.refresh_vehicle_table.assert_called()
    app.clear_dynamic_content.assert_called()


def test_update_vehicle_values(app, mocker):
    mocker.patch.object(app.vehicle_table, 'insert')
    mocker.patch.object(app.vehicle_table, 'delete')
    app.update_vehicle_values([(
        1, "AB12 CDE", "Toyota", "Corolla", 2020, "Sedan", "Petrol",
        "2024-06-01", "2024-07-01", "Tax Paid"
        )])
    app.vehicle_table.insert.assert_called()
    app.vehicle_table.delete.assert_called()


def test_clear_dynamic_content(app):
    label = tk.Label(app.dynamic_content_frame, text="Test")
    label.pack()
    assert len(app.dynamic_content_frame.winfo_children()) > 0
    app.clear_dynamic_content()
    assert len(app.dynamic_content_frame.winfo_children()) == 0

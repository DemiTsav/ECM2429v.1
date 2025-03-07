import pytest
from asset_management.frontend.ui_manager import AssetManagementUI
from asset_management.backend.asset_management_handler import VehicleController
from asset_management.frontend.ui_components import UIComponents
import tkinter as tk


@pytest.fixture
def mock_ui(mocker):
    """Mock UI with a fake vehicle controller."""
    root = tk.Tk()
    mock_controller = mocker.Mock(spec=VehicleController)
    mock_controller.connection = mocker.Mock()
    mock_controller.cursor = mocker.Mock()

    mock_controller.get_all_vehicles = mocker.Mock(return_value=[])

    ui = AssetManagementUI(root, mock_controller)

    yield ui
    root.destroy()


def test_ui_calls_controller(mock_ui, mocker):
    """Test if UI calls backend when adding a vehicle."""

    mock_controller = mock_ui.controller
    mock_controller.add_vehicle()

    mock_components = mocker.Mock(spec=UIComponents)
    mock_components.show_status_popup()
    mock_ui.show_add_vehicle_form()

    button = mock_ui.dynamic_content_frame.children.get('!button')
    if button:
        button.invoke()
    else:
        pytest.fail("Add Vehicle button was not found.")

    mock_components.show_status_popup.assert_called_once

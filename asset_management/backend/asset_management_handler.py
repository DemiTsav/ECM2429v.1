from asset_management.database import VehicleDatabase
from asset_management.backend.field_validations import FieldValidations
from asset_management.frontend.ui_components import UIComponents

class VehicleController:
    """
    Handles business logic for vehicle operations.
    """

    def __init__(self, db: VehicleDatabase):
        """Initialize the controller with a database instance."""
        self.db = db

    def get_all_vehicles(self):
        """Retrieve all vehicles from the database."""
        return self.db.get_all_vehicles()

    def add_vehicle(self, entries, tax_status, refresh_table_callback, clear_content_callback):
        """Process adding a new vehicle."""
        registration = entries["Registration"].get()
        make = entries["Make"].get()
        model = entries["Model"].get()
        year = entries["Year"].get()
        vehicle_type = entries["Vehicle Type"].get()
        fuel_type = entries["Fuel Type"].get()
        service_date = entries["Service Date"].get()
        tax_due_date = entries["Tax Due Date"].get()
        tax_status = tax_status.get()
        errors = FieldValidations.validations(
            self, entries, year, service_date, tax_due_date, tax_status
        )
        if errors:
            errors_list = []
            for error in errors:
                errors_list.append(error)
            formatted_errors = "\n".join(errors_list)
            UIComponents.show_status_popup("Success", formatted_errors)
        else:
            try:
                VehicleDatabase.add_vehicle( 
                    self, registration, make, model, year, vehicle_type, fuel_type, service_date, tax_due_date, tax_status)
                UIComponents.show_status_popup("Success", "Vehicle added successfully.")
                refresh_table_callback()
                clear_content_callback()

            except Exception as e:
                UIComponents.show_status_popup("Error", [str(e)])


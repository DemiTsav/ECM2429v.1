from asset_management.database import VehicleDatabase
from asset_management.backend.field_validations import FieldValidations
from asset_management.frontend.ui_components import UIComponents
import tkinter as tk


class VehicleController:
    """
    Handles business logic for vehicle operations.
    """

    def __init__(self, db: VehicleDatabase, vehicle_table):
        """Initialize the controller with a database instance."""
        self.db = db
        self.vehicle_table = vehicle_table

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


    def confirm_deletion(self, selected_items, refresh_table_callback, clear_content_callback) -> bool:
        """Confirm deletion and enable delete button if a vehicle is selected."""
        if not selected_items:
            return False
        try:
            vehicle_id = self.vehicle_table.item(selected_items[0], "values")[0]
            vehicle_info = VehicleDatabase.get_vehicle(self, vehicle_id)
            if not vehicle_info:
                tk.Label(
                    self.dynamic_content_frame,
                    text="Vehicle not found in database.",
                    fg="red"
                ).pack()
                return False
            tk.Label()
        except Exception as e:
            tk.Label(
                self.dynamic_content_frame,
                text=f"Error retrieving vehicle: {str(e)}",
                fg="red"
            ).pack()
            return False
        
        UIComponents.display_vehicle_info(self, vehicle_info)

        delete_button = UIComponents.create_button(
            self,
            self.dynamic_content_frame,
            "Delete Vehicle",
            lambda: VehicleController.delete_vehicle(self, vehicle_id, refresh_table_callback, clear_content_callback),
            padx=10
        ).pack()

        cancel_button = UIComponents.create_button(
            self,
            self.dynamic_content_frame,
            "Cancel",
            clear_content_callback,
            padx=10
        ).pack()

    def delete_vehicle(self, vehicle_id, refresh_vehicle_table, clear_dynamic_content):
        """Delete a vehicle from the database."""
        try:
            VehicleDatabase.delete_vehicle(self, vehicle_id)
            UIComponents.show_status_popup("Success", "Vehicle deleted successfully.")
            refresh_vehicle_table()
            clear_dynamic_content()
        except Exception as e:
            UIComponents.show_status_popup("Error", str(e))
            clear_dynamic_content()

from asset_management.database import VehicleDatabase
from asset_management.backend.field_validations import FieldValidations
from asset_management.frontend.ui_components import UIComponents
import tkinter as tk
from typing import List


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
        vehicle_info, vehicle_id = VehicleController.retrieve_vehicle_info(self, selected_items)
        
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
    

    def retrieve_vehicle_info(self, selected_items):
        try:
            vehicle_id = self.vehicle_table.item(selected_items[0], "values")[0]
            vehicle_info = VehicleDatabase.get_vehicle(self, vehicle_id)
            print(vehicle_info)
            if not vehicle_info:
                tk.Label(
                    self.dynamic_content_frame,
                    text="Vehicle not found in database.",
                    fg="red"
                ).pack()
                return False
            return vehicle_info, vehicle_id
        except Exception as e:
            tk.Label(
                self.dynamic_content_frame,
                text=f"Error retrieving vehicle: {str(e)}",
                fg="red"
            ).pack()
            return False

    def update_vehicle(self, vehicle_id: str, refresh_vehicle_table, clear_dynamic_content, update_entries) -> None:
        """
        Process the update of a vehicle's details.

        Args:
            vehicle_id (str): The ID of the vehicle to be updated.
        """
        updates: Dict[str, str] = {
            field: widgets["entry"].get()
            for field, widgets in update_entries.items()
            if widgets["checkbox"].get()
        }
        if not updates:
            UIComponents.show_status_popup(
                "Error", "No fields selected for update!"
                )
            return

        errors: List[str] = FieldValidations.update_validations(self, updates)
        if errors:
            UIComponents.show_status_popup("Error", "\n".join(errors))
            return
        else:
            try:
                VehicleDatabase.update_vehicle(self, vehicle_id, updates)
                UIComponents.show_status_popup(
                    "Success", "Vehicle updated successfully!"
                    )
                clear_dynamic_content()
                refresh_vehicle_table()
            except Exception as e:
                UIComponents.show_status_popup(
                    "Error", f"Failed to update vehicle: {e}"
                    )
      
    def perform_search(self):
        """
        Perform a search based on user input. If no search parameters are provided, return all vehicles.
        """
        # Collect search parameters from the entry fields
        search_params = {
            field.strip().replace(" ", "_").lower(): entry.get().strip()
            for field, entry in self.search_entries.items()
            if entry.get().strip()  # Exclude empty fields
        }

        # Include tax status if selected
        tax_status = self.tax_status_var.get().strip()
        if tax_status:  # Ensure it's not empty
            search_params["tax_status"] = tax_status  # Ensuring consistency in field naming

        # If no search criteria, fetch all vehicles
        if not search_params:
            query = "SELECT * FROM vehicles"
            values = tuple()
        else:
            # Construct SQL WHERE clause dynamically
            query = "SELECT * FROM vehicles WHERE " + " AND ".join(
                f"[{field}] LIKE ?" for field in search_params.keys()
            )
            values = tuple(f"%{value}%" for value in search_params.values())

            print(f"Executing query: {query}")  # Debugging: Show query
            print(f"With values: {values}")  # Debugging: Show values

        # Execute the query and return the results
        results = VehicleDatabase.query_vehicles(self, query, values)

        # Return results or empty list if no matching results
        return results if results else []

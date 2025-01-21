from asset_management.field_validations import FieldValidations
from asset_management.ui_components import UIComponents
import tkinter as tk

class VehicleProcess:

    def __init__(self, db):
        self.db = db  # Database instance

    def process_add_vehicle(self, entries, tax_status_dropdown):
        # Retrieve values from the entries
        make = entries["Make"].get()
        model = entries["Model"].get()
        year = entries["Year"].get()
        vehicle_type = entries["Vehicle Type"].get()
        fuel_type = entries["Fuel Type"].get()
        service_date = entries["Service Date"].get()
        tax_due_date = entries["Tax Due Date"].get()
        tax_status = tax_status_dropdown.get()

        # Perform validations
        errors = FieldValidations.validations(self, entries, year, service_date, tax_due_date, tax_status)
        if errors:
            UIComponents.show_status_popup("Errors", "\n".join(errors))
            return
        
        try:
            self.db.add_vehicle(make, model, int(year), vehicle_type, fuel_type, service_date, tax_due_date, tax_status)
            message = "Vehicle added successfully!"
            UIComponents.show_status_popup("Success", message)
            UIComponents.clear_form_fields(self)
            self.show_all_vehicles()
        except Exception as e:
            UIComponents.show_status_popup("Error", f"Failed to add vehicle: {str(e)}")

    def process_update_vehicle(self, vehicle_id):
        updates = {
            field: widgets["entry"].get()
            for field, widgets in self.update_entries.items()
            if widgets["checkbox"].get()
        }
        if not updates:
            UIComponents.show_status_popup("Error", "No fields selected for update!")
            return
        
        errors = FieldValidations.update_validations(self, updates)
        print(errors)
        if errors:
            UIComponents.show_status_popup("Error", "\n".join(errors))
            return
        else:
            try:
                self.db.update_vehicle(vehicle_id, updates)
                UIComponents.show_status_popup("Success", "Vehicle updated successfully!")
                self.clear_dynamic_content()
                self.show_all_vehicles() 
            except Exception as e:
                UIComponents.show_status_popup("Error", f"Failed to update vehicle: {e}")

    def process_delete_vehicles(self, vehicle_info_list):
        """Deletes selected vehicles."""
        vehicle_ids = [vehicle[0] for vehicle in vehicle_info_list]
        try:
            for vehicle_id in vehicle_ids:
                self.db.delete_vehicle(vehicle_id)
            UIComponents.show_status_popup("Success", f"Deleted {len(vehicle_info_list)} vehicle(s) successfully!")
            self.clear_dynamic_content()
            self.show_all_vehicles()
        except Exception as e:
            UIComponents.show_status_popup("Error", f"Failed to delete vehicle(s): {e}")

    def retrieve_vehicle_id(self):
        # This should be handled by the UI and not by VehicleProcess directly
        selected_items = self.vehicle_table.selection()
        if not selected_items:
            UIComponents.show_status_popup("Select a vehicle to update.")
            return
        return self.vehicle_table.item(selected_items[0], "values")[0]

    def perform_search(self):
        """Performs a search based on user inputs."""
        conditions = []
        query_params = []

        for field, entry in self.search_entries.items():
            value = entry.get().strip()
            if value:
                if field in ["Tax Due Date", "Service Date"]:
                    try:
                        if len(value) == 8 and value.count('-') == 2:
                            day, month, year = value.split('-')
                            year = int(year)
                            conditions.append(f"CAST(SUBSTR({field.replace(' ', '_').lower()}, 7, 4) AS INTEGER) = ?")
                            query_params.append(year)
                        elif len(value) == 4:
                            year = int(value)
                            conditions.append(f"CAST(SUBSTR({field.replace(' ', '_').lower()}, 7, 4) AS INTEGER) = ?")
                            query_params.append(year)
                    except ValueError:
                        pass
                else:
                    conditions.append(f"CAST({field.replace(' ', '_').lower()} AS TEXT) LIKE ?")
                    query_params.append(f"%{value}%")

        query = "SELECT * FROM vehicles"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        try:
            results = self.db.query_vehicles(query, query_params)
            VehicleProcess.update_vehicle_table(self, results)
        except Exception as e:
            UIComponents.show_status_popup("Error",f"Search failed: {str(e)}")

    def update_vehicle_table(self, vehicles):
        """Update the vehicle table with search results."""
        for row in self.vehicle_table.get_children():
            self.vehicle_table.delete(row)
        for vehicle in vehicles:
            self.vehicle_table.insert("", tk.END, values=vehicle)

    def show_deletion_confirmation(self, selected_items):
        """Show confirmation message for deletion."""
        self.clear_dynamic_content()
        vehicle_info_list = [self.vehicle_table.item(item, "values") for item in selected_items]

        UIComponents.display_message(self, "Are you sure you want to delete the following vehicles?", "black")
        for vehicle_info in vehicle_info_list:
            vehicle_details = f"ID: {vehicle_info[0]}\nMake: {vehicle_info[1]}\nModel: {vehicle_info[2]}"
            UIComponents.display_message(self, vehicle_details, "black", font=("Helvetica", 10))

        VehicleProcess.show_confirm_cancel_buttons(self, vehicle_info_list)

    def show_confirm_cancel_buttons(self, vehicle_info_list):
        """Show confirm/cancel buttons for deletion."""
        confirm_button = tk.Button(
            self.dynamic_content_frame,
            text="Confirm Deletion",
            fg="white",
            bg="red",
            command=lambda: VehicleProcess.process_delete_vehicles(self, vehicle_info_list)
        )
        confirm_button.pack(side="left", padx=10, pady=10)

        cancel_button = tk.Button(self.dynamic_content_frame, text="Cancel", command=self.clear_dynamic_content)
        cancel_button.pack(side="left", padx=10, pady=10)


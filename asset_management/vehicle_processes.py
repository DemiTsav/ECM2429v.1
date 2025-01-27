from asset_management.field_validations import FieldValidations
from asset_management.ui_components import UIComponents
import tkinter as tk
from tkinter import ttk
from typing import Dict, List, Optional, Tuple, Union


class VehicleProcess:

    def __init__(self, db: object) -> None:
        self.db = db

    def process_add_vehicle(
        self, entries: Dict[str, tk.Entry], tax_status: ttk.Combobox
    ) -> None:
        # Retrieve values from the entries
        make: str = entries["Make"].get()
        model: str = entries["Model"].get()
        year: str = entries["Year"].get()
        vehicle_type: str = entries["Vehicle Type"].get()
        fuel_type: str = entries["Fuel Type"].get()
        service_date: str = entries["Service Date"].get()
        tax_due_date: str = entries["Tax Due Date"].get()
        # tax_status: str = tax_status)
        errors: List[str] = FieldValidations.validations(
            self, entries, year, service_date, tax_due_date, tax_status
            )
        if errors:
            UIComponents.show_status_popup("Errors", "\n".join(errors))
            return

        try:
            self.db.add_vehicle(
                make, model, int(year), vehicle_type, fuel_type, service_date,
                tax_due_date, tax_status
                )
            message: str = "Vehicle added successfully!"
            UIComponents.show_status_popup("Success", message)
            UIComponents.clear_form_fields(self)
            self.show_all_vehicles()
        except Exception as e:
            UIComponents.show_status_popup(
                "Error", f"Failed to add vehicle: {str(e)}"
                )

    def process_update_vehicle(self, vehicle_id: str) -> None:
        """
        Process the update of a vehicle's details.

        Args:
            vehicle_id (str): The ID of the vehicle to be updated.
        """
        updates: Dict[str, str] = {
            field: widgets["entry"].get()
            for field, widgets in self.update_entries.items()
            if widgets["checkbox"].get()
        }
        if not updates:
            UIComponents.show_status_popup(
                "Error", "No fields selected for update!"
                )
            return

        errors: List[str] = FieldValidations.update_validations(self, updates)
        print(errors)
        if errors:
            UIComponents.show_status_popup("Error", "\n".join(errors))
            return
        else:
            try:
                self.db.update_vehicle(vehicle_id, updates)
                UIComponents.show_status_popup(
                    "Success", "Vehicle updated successfully!"
                    )
                self.clear_dynamic_content()
                self.show_all_vehicles()
            except Exception as e:
                UIComponents.show_status_popup(
                    "Error", f"Failed to update vehicle: {e}"
                    )

    def process_delete_vehicles(
        self, vehicle_info_list: List[Tuple[str]]
    ) -> None:
        """
        Deletes selected vehicles from the database.

        Args:
            vehicle_info_list (List[Tuple[str]]): List of tuples containing
            vehicle IDs and details.
        """
        vehicle_ids: List[str] = [vehicle[0] for vehicle in vehicle_info_list]
        try:
            for vehicle_id in vehicle_ids:
                self.db.delete_vehicle(vehicle_id)
            UIComponents.show_status_popup(
                "Success",
                f"Deleted {len(vehicle_info_list)} vehicle(s) successfully!"
            )
            self.clear_dynamic_content()
            self.show_all_vehicles()
        except Exception as e:
            UIComponents.show_status_popup(
                "Error", f"Failed to delete vehicle(s): {e}"
                )

    def retrieve_vehicle_id(self) -> Optional[str]:
        """
        Retrieve the selected vehicle ID from the table.

        Returns:
            Optional[str]: The ID of the selected vehicle, or None if no
            selection is made.
        """
        selected_items: Tuple[str, ...] = self.vehicle_table.selection()
        if not selected_items:
            UIComponents.show_status_popup("Select a vehicle to update.")
            return
        return self.vehicle_table.item(selected_items[0], "values")[0]

    def perform_search(self) -> None:
        """
        Perform a search based on user input and display the results in the
        vehicle table.
        """
        conditions: List[str] = []
        query_params: List[Union[str, int]] = []

        for field, entry in self.search_entries.items():
            value: str = entry.get().strip()
            if value:
                field_replace = field.replace(' ', '_').lower()
                if field in ["Tax Due Date", "Service Date"]:
                    try:
                        if len(value) == 8 and value.count('-') == 2:
                            day, month, year = value.split('-')
                            year = int(year)
                            conditions.append(f"{field_replace} = ?")
                            query_params.append(value)
                    except ValueError:
                        pass
                else:
                    try:
                        conditions.append(f"CAST({field_replace} AS TEXT) LIKE ?")
                        query_params.append(f"%{value}%")
                    except ValueError:
                        pass

        query = "SELECT * FROM vehicles"
        if conditions:
            query += " WHERE "
            query += " AND ".join(
                conditions
            )

        try:
            results = self.db.query_vehicles(query, query_params)
            VehicleProcess.update_vehicle_table(self, results)
        except Exception as e:
            UIComponents.show_status_popup(
                "Error",
                f"Search failed: {str(e)}"
            )

    def update_vehicle_table(self, vehicles: List[Tuple]) -> None:
        """
        Update the vehicle table with new data.

        Args:
            vehicles (List[Tuple]): List of vehicle details to populate table.
        """
        for row in self.vehicle_table.get_children():
            self.vehicle_table.delete(row)
        for vehicle in vehicles:
            self.vehicle_table.insert("", tk.END, values=vehicle)

    def show_deletion_confirmation(
            self, selected_items: Tuple[str, ...]
            ) -> None:
        """
        Display a confirmation prompt for deleting selected vehicles.

        Args:
            selected_items (Tuple[str, ...]): Selected rows from table.
        """
        self.clear_dynamic_content()
        vehicle_info_list = [
            self.vehicle_table.item(item, "values") for item in selected_items
            ]

        UIComponents.display_message(
            self,
            "Are you sure you want to delete the following vehicles?",
            "black"
            )
        for vehicle_info in vehicle_info_list:
            id = vehicle_info[0]
            make = vehicle_info[1]
            model = vehicle_info[2]
            vehicle_details = f"ID: {id}\nMake: {make}\nModel: {model}"
            UIComponents.display_message(
                self, vehicle_details, "black", font=("Helvetica", 10)
                )

        VehicleProcess.show_confirm_cancel_buttons(self, vehicle_info_list)

    def show_confirm_cancel_buttons(
            self, vehicle_info_list: List[Tuple[str, ...]]
            ) -> None:
        """
        Display confirm and cancel buttons for vehicle deletion.

        Args:
            vehicle_info_list (List[Tuple[str, ...]]): List of vehicle details
            to be deleted.
        """
        confirm_button = tk.Button(
            self.dynamic_content_frame,
            text="Confirm Deletion",
            fg="white",
            bg="red",
            command=lambda: VehicleProcess.process_delete_vehicles(
                self, vehicle_info_list
                )
        )
        confirm_button.pack(side="left", padx=10, pady=10)

        cancel_button = tk.Button(
            self.dynamic_content_frame,
            text="Cancel",
            command=self.clear_dynamic_content
            )
        cancel_button.pack(side="left", padx=10, pady=10)

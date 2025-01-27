from datetime import datetime
from typing import Dict, List, Optional, Union
import tkinter as tk
import re


class FieldValidations:
    """
    A class to handle field validations for vehicle management forms.
    """

    def validations(
        self,
        entries: Dict[str, Union[str, tk.Entry]],
        year: Union[str, int],
        service_date: str,
        tax_due_date: str,
        tax_status: Optional[str]
    ) -> Optional[List[str]]:
        """
        Perform validations on user input fields.

        Args:
            entries (Dict[str, Union[str, tk.Entry]]): Dictionary of field
            names and their corresponding entry widgets.
            year (Union[str, int]): The year field to validate.
            service_date (str): The service date in dd-mm-yy format.
            tax_due_date (str): The tax due date in dd-mm-yy format.
            tax_status (Optional[str]): The selected tax status.

        Returns:
            Optional[List[str]]: A list of error messages if validation fails,
            or None if all fields are valid.
        """
        errors: List[str] = []
        for field, entry in entries.items():
            if not entry.get().strip():
                errors.append(f"{field} cannot be empty.")
            elif field in ["Make", "Model", "Fuel Type", "Vehicle Type"] and not FieldValidations.validate_character_input(self, entry.get()):
                errors.append(f"Value for {field} must use characters a-z")
        if not FieldValidations.validate_year(self, year):
            errors.append(
                "Year must be a valid number between 1900 and the current year"
                )
        if not FieldValidations.validate_date(self, service_date):
            errors.append("Service Date must be in dd-mm-yy format.")
        if not FieldValidations.validate_date(self, tax_due_date):
            errors.append("Tax Due Date must be in dd-mm-yy format.")
        if not tax_status:
            errors.append("Tax Status must be selected.")

        if errors:
            return errors

    def validate_year(self, year: Union[str, int]) -> bool:
        """
        Validate the year field.

        Args:
            year (Union[str, int]): The year to validate.

        Returns:
            bool: True if the year is a year 1900-current
        """
        try:
            year = int(year)
            return 1900 <= year <= datetime.now().year
        except ValueError:
            return False

    def validate_date(self, date_str: str) -> bool:
        """
        Validate a date string in the dd-mm-yy format.

        Args:
            date_str (str): The date string to validate.

        Returns:
            bool: True if the date is in the correct format, False otherwise.
        """
        try:
            datetime.strptime(date_str, "%d-%m-%y")
            return True
        except ValueError:
            return False

    def validate_character_input(self, value: str) -> bool:
        """
        Validate that typed input is unicode a-z and reject other characters
        """
        print(value)
        value = str(value)
        print(value)
        value_to_validate = value.replace(" ", "")
        print(value_to_validate)
        if re.fullmatch(r"[a-zA-Z0-9]*", value_to_validate):
            return True
        return False

    def update_validations(self, updates: Dict[str, str]) -> List[str]:
        """
        Perform validations on updated fields.

        Args:
            updates (Dict[str, str]): Dictionary of field names and
            their corresponding updated values.

        Returns:
            List[str]: A list of error messages if validation fails,
            or an empty list if all fields are valid.
        """
        errors: List[str] = []
        if "Year" in updates and not FieldValidations.validate_year(
                self, updates["Year"]
        ):
            errors.append("Invalid year!")
        if "service_date" in updates and not FieldValidations.validate_date(
            self, updates["service_date"]
        ):
            errors.append("Date fields must be in dd-mm-yy format!")
        if "tax_due_date" in updates and not FieldValidations.validate_date(
            self, updates["tax_due_date"]
        ):
            errors.append("Date fields must be in dd-mm-yy format!")
        for update in updates:
            print(update)
            if update in ["Make", "Model", "fuel_type", "vehicle_type"]:
                if not FieldValidations.validate_character_input(self, updates[update]):
                    errors.append(f" value for {update} must use only characters a-z")
        return errors

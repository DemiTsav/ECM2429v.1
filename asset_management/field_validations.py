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
            elif field in ["Make", "Registration", "Model", "Fuel Type", "Vehicle Type"] and not FieldValidations.validate_character_input(self, entry.get()):
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

    
    @staticmethod
    def validate_date(self, date_str: str) -> bool:
        """
        Validate a date string strictly in the dd-mm-yyyy format.

        Args:
            date_str (str): The date string to validate.

        Returns:
            bool: True if the date is in the dd-mm-yyyy format and year > 2000, False otherwise.
        """
        # Check if the date matches the dd-mm-yyyy format strictly
        if not re.match(r"^\d{2}-\d{2}-\d{4}$", date_str):
            return False  # Reject if it's not strictly in dd-mm-yyyy format

        try:
            # Try to parse the date
            date_obj = datetime.strptime(date_str, "%d-%m-%Y")
            
            # Ensure the year is greater than 2000
            if date_obj.year <= 2000:
                return False
            
            return True
        except ValueError:
            # If parsing fails, it's an invalid date format
            return False

    def validate_character_input(self, value: str) -> bool:
        """
        Validate that typed input is unicode a-z and reject other characters
        """
        value = str(value)
        value_to_validate = value.replace(" ", "")
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
        if "Service Date" in updates and not FieldValidations.validate_date(
            self, updates["Service Date"]
        ):
            errors.append("Date fields must be in dd-mm-yyyy format!")
        if "Tax Due Date" in updates and not FieldValidations.validate_date(
            self, updates["Tax Due Date"]
        ):
            errors.append("Date fields must be in dd-mm-yyyy format!")
        print(errors)
        return errors

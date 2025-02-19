from datetime import datetime
import re
from typing import Dict, List, Optional, Union
import tkinter as tk


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
        """
        errors: List[str] = []
        for field, entry in entries.items():
            if not entry.get().strip():
                errors.append(f"{field} cannot be empty.")
            elif field in ["Make", "Registration", "Model", "Fuel Type", "Vehicle Type"] and not FieldValidations.validate_character_input(entry.get()):
                errors.append(f"Value for {field} must use characters a-z")
        if not FieldValidations.validate_year(year):
            errors.append(
                "Year must be a valid number between 1900 and the current year"
            )
        if not FieldValidations.validate_date(service_date):
            errors.append("Service Date must be in dd-mm-yyyy format.")
        if not FieldValidations.validate_date(tax_due_date):
            errors.append("Tax Due Date must be in dd-mm-yyyy format.")
        if not tax_status:
            errors.append("Tax Status must be selected.")

        if errors:
            return errors

    def validate_date(self, date_str: str) -> bool:
        """
        Validate a date string strictly in the dd-mm-yyyy format.
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

    def validate_year(self, year: Union[str, int]) -> bool:
        """
        Validate the year to check if it's between 1900 and the current year.
        
        Args:
            year (Union[str, int]): The year to validate.
        
        Returns:
            bool: True if the year is valid, False otherwise.
        """
        current_year = datetime.now().year
        try:
            year = int(year)
        except ValueError:
            return False
        return 1900 <= year <= current_year

    def update_validations(self, updates: Dict[str, str]) -> List[str]:
        """
        Perform validations on updated fields.
        """
        errors: List[str] = []
        if "Service Date" in updates and not FieldValidations.validate_date(updates["Service Date"]):
            errors.append("Date fields must be in dd-mm-yyyy format!")
        if "Tax Due Date" in updates and not FieldValidations.validate_date(updates["Tax Due Date"]):
            errors.append("Date fields must be in dd-mm-yyyy format!")
        return errors

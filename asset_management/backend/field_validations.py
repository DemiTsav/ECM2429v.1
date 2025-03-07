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

        Args:
            entries (Dict[str, Union[str, tk.Entry]]): Dictionary of field
            names and their values or Tkinter entry widgets.
            year (Union[str, int]): The vehicle's manufacturing year.
            service_date (str): The last service date in "dd-mm-yyyy" format.
            tax_due_date (str): The tax due date in "dd-mm-yyyy" format.
            tax_status (Optional[str]): The tax status selection.

        Returns:
            Optional[List[str]]: A list of error messages if validation fails,
            otherwise None.
        """
        errors: List[str] = []
        for field, entry in entries.items():
            if not entry.get().strip():
                errors.append(f"{field} cannot be empty.")
            elif field in ["Make", "Registration", "Model", "Fuel Type",
                           "Vehicle Type"
                           ] and not FieldValidations.validate_character_input(
                               self, entry.get()):
                errors.append(
                    f"Value for {field} must use characters a-z"
                )
        if not FieldValidations.validate_year(self, year):
            errors.append(
                "Year must be a valid number between 1900 and the current year"
            )
        if not FieldValidations.validate_date(self, service_date):
            errors.append("Service Date must be in dd-mm-yyyy format.")
        if tax_status in ["SORN", "Exempt"]:
            if tax_due_date != "N/A":
                errors.append(
                    "Tax Due Date must be 'N/A' when Tax Status is SORN or "
                    "Exempt."
                    )
        else:
            if not FieldValidations.validate_date(self, tax_due_date):
                errors.append("Tax Due Date must be in dd-mm-yyyy format.")

        if not tax_status:
            errors.append("Tax Status must be selected.")

        if errors:
            return errors

    def validate_date(self, date_str: str) -> bool:
        """
        Validate a date string strictly in the "dd-mm-yyyy" format.

        Args:
            date_str (str): The date string to validate.

        Returns:
            bool: True if the date is valid and the year is greater than 2000,
            otherwise False.
        """
        if not re.match(r"^\d{2}-\d{2}-\d{4}$", date_str):
            return False

        try:
            date_obj = datetime.strptime(date_str, "%d-%m-%Y")

            if date_obj.year <= 2000:
                return False

            return True
        except ValueError:
            return False

    def validate_character_input(self, value: str) -> bool:
        """
        Validate that input contains only alphanumeric characters and spaces.

        Args:
            value (str): The input string to validate.

        Returns:
            bool: True if valid, False otherwise.
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

        Args:
            updates (Dict[str, str]): Dictionary containing field names and
            their updated values.

        Returns:
            List[str]: A list of error messages if validation fails.
        """
        errors: List[str] = []
        print(updates)
        if "Service Date" in updates and not FieldValidations.validate_date(
            self,
            updates["Service Date"]
                ):
            errors.append("Service date field must be in dd-mm-yyyy format!")
        if "Tax Due Date" in updates:
            if updates.get("Tax Status") in ["SORN", "Exempt"]:
                if updates["Tax Due Date"] != "N/A":
                    errors.append(
                        "Tax Due Date must be 'N/A' when Tax Status is "
                        "SORN or Exempt."
                        )
            elif not FieldValidations.validate_date(
                self,
                updates["Tax Due Date"]
            ):
                errors.append(
                    "Tax due date field must be in dd-mm-yyyy format!"
                    )
        if "Tax Status" in updates:
            if not updates["Tax Status"] in [
                "Tax Paid", "Tax Due", "SORN", "Exempt"
            ]:
                errors.append(
                    "Tax Status must be one of the following: Tax Paid,"
                    " Tax Due, SORN, Exempt."
                    )
            if updates["Tax Status"] in ["SORN", "Exempt"] and (
                "Tax Due Date" not in updates or
                updates["Tax Due Date"] != "N/A"
            ):
                errors.append(
                    "Tax Due Date must be 'N/A' when Tax Status is SORN or "
                    "Exempt, please update/ re-submit this field."
                    )
            if not updates["Tax Status"]:
                errors.append("Tax Due Date must be entered.")
        if errors:
            return errors

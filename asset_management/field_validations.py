from datetime import datetime
class FieldValidations:

    def validations(self, entries, year, service_date, tax_due_date, tax_status):
        errors = []
        for field, entry in entries.items():
            if not entry.get().strip():
                errors.append(f"{field} cannot be empty.")
                print(errors)
        if not FieldValidations.validate_year(self, year):
            errors.append("Year must be a valid number between 1900 and the current year.")
        if not FieldValidations.validate_date(self, service_date):
            errors.append("Service Date must be in dd-mm-yy format.")
        if not FieldValidations.validate_date(self, tax_due_date):
            errors.append("Tax Due Date must be in dd-mm-yy format.")
        if not tax_status:
            errors.append("Tax Status must be selected.")

        if errors:
            return errors

    def validate_year(self, year: int) -> bool:
        try:
            year = int(year)
            return 1900 <= year <= datetime.now().year
        except ValueError:
            return False


    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%d-%m-%y")
            return True
        except ValueError:
            return False
        
    def update_validations(self, updates):
        errors = []
        # Validate updates (add appropriate validations for your fields)
        if "Year" in updates and not FieldValidations.validate_year(self, updates["Year"]):
            errors.append("Invalid year!")
        if "service_date" in updates and not FieldValidations.validate_date(self, updates["service_date"]):
            errors.append("Date fields must be in dd-mm-yy format!")
        if "tax_due_date" in updates and not FieldValidations.validate_date(self, updates["tax_due_date"]):
            errors.append("Date fields must be in dd-mm-yy format!")
        return errors
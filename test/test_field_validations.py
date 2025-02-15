import unittest
from datetime import datetime
from unittest.mock import MagicMock
from asset_management.field_validations import FieldValidations

class TestFieldValidations(unittest.TestCase):

    def setUp(self):
        self.validator = FieldValidations()

    def test_validate_year_valid(self):
        self.assertTrue(self.validator.validate_year(2000))
        self.assertTrue(self.validator.validate_year(datetime.now().year))

    def test_validate_year_invalid(self):
        self.assertFalse(self.validator.validate_year(1800))
        self.assertFalse(self.validator.validate_year("invalid"))

    def test_validate_date_valid(self):
        self.assertTrue(self.validator.validate_date("01-01-20"))
        self.assertTrue(self.validator.validate_date("31-12-99"))

    def test_validate_date_invalid(self):
        self.assertFalse(self.validator.validate_date("2020-01-01"))
        self.assertFalse(self.validator.validate_date("01/01/20"))
        self.assertFalse(self.validator.validate_date("invalid"))

    def test_validate_character_input_valid(self):
        self.assertTrue(self.validator.validate_character_input("Toyota"))
        self.assertTrue(self.validator.validate_character_input("Model X"))

    def test_validate_character_input_invalid(self):
        self.assertFalse(self.validator.validate_character_input("@Invalid!"))

    def test_validations_all_valid(self):
        entries = {"Make": MagicMock(get=MagicMock(return_value="Toyota")),
                   "Model": MagicMock(get=MagicMock(return_value="Corolla"))}
        year = 2020
        service_date = "01-01-20"
        tax_due_date = "31-12-20"
        tax_status = "Active"

        errors = self.validator.validations(entries, year, service_date, tax_due_date, tax_status)
        self.assertIsNone(errors)

    def test_validations_with_errors(self):
        entries = {"Make": MagicMock(get=MagicMock(return_value="")),
                   "Model": MagicMock(get=MagicMock(return_value="123Invalid"))}
        year = 1800
        service_date = "invalid"
        tax_due_date = "invalid"
        tax_status = None

        errors = self.validator.validations(entries, year, service_date, tax_due_date, tax_status)
        print(errors)
        self.assertIsNotNone(errors)
        self.assertIn("Make cannot be empty.", errors)
        self.assertIn("Year must be a valid number between 1900 and the current year", errors)
        self.assertIn("Service Date must be in dd-mm-yy format.", errors)
        self.assertIn("Tax Due Date must be in dd-mm-yy format.", errors)
        self.assertIn("Tax Status must be selected.", errors)

    def test_update_validations_all_valid(self):
        updates = {"Year": "2020", "service_date": "01-01-20", "tax_due_date": "31-12-20", "Make": "Toyota"}

        errors = self.validator.update_validations(updates)
        self.assertEqual(errors, [])

    def test_update_validations_with_errors(self):
        updates = {"Year": "1800", "service_date": "invalid", "tax_due_date": "invalid", "Make": "@Invalid"}

        errors = self.validator.update_validations(updates)
        self.assertIn("Invalid year!", errors)
        self.assertIn("Date fields must be in dd-mm-yy format!", errors)
        self.assertIn(" value for Make must use only characters a-z", errors)

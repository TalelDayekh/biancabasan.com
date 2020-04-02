from django.test import TestCase

from users.auth import password_strength_validator
from users.exceptions import ValidationError


class PasswordStrengthValidatorTest(TestCase):
    def test_correctly_formatted_password_is_valid(self):
        valid_password_one = password_strength_validator("Password123")
        valid_password_two = password_strength_validator("P@$$w0rd")

        self.assertIsNone(valid_password_one)
        self.assertIsNone(valid_password_two)

    def test_password_with_not_enough_characters_is_invalid(self):
        with self.assertRaises(ValidationError):
            password_strength_validator("Qwerty1")

    def test_password_with_no_capital_letters_is_invalid(self):
        with self.assertRaises(ValidationError):
            password_strength_validator("password")
        with self.assertRaises(ValidationError):
            password_strength_validator("password123")

    def test_password_with_no_numbers_is_invalid(self):
        with self.assertRaises(ValidationError):
            password_strength_validator("Password")

    def test_password_with_only_numbers_is_invalid(self):
        with self.assertRaises(ValidationError):
            password_strength_validator(12345678)

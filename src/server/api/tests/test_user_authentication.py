from django.test import TestCase

from api.exceptions import ValidationError
from api.user_authentication import password_strength_validator
from rest_framework.test import APITestCase


class PasswordStrengthValidatorTest(TestCase):
    def test_correctly_formatted_password_is_valid(self):
        validate_password_one = password_strength_validator("Password123")
        validate_password_two = password_strength_validator("P@$$w0rd")

        self.assertIsNone(validate_password_one)
        self.assertIsNone(validate_password_two)

    def test_password_with_not_enough_characters_is_invalid(self):
        with self.assertRaises(ValidationError):
            validate_password = password_strength_validator("Qwerty1")

    def test_password_with_no_capital_letters_is_invalid(self):
        with self.assertRaises(ValidationError):
            validate_password = password_strength_validator("password")
        with self.assertRaises(ValidationError):
            validate_password = password_strength_validator("password123")

    def test_password_with_no_numbers_is_invalid(self):
        with self.assertRaises(ValidationError):
            validate_password = password_strength_validator("Password")

    def test_password_with_only_numbers_is_invalid(self):
        with self.assertRaises(ValidationError):
            validate_password = password_strength_validator(12345678)


class PasswordChangeTest(APITestCase):
    pass

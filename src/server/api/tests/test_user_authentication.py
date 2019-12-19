from django.test import TestCase

from api.user_authentication import password_strength_validator
from rest_framework.test import APITestCase


class PasswordStrengthValidatorTest(TestCase):
    def test_correctly_formatted_password_is_valid(self):
        validate_password_one = password_strength_validator("Password123")
        validate_password_two = password_strength_validator("P@$$w0rd")

        self.assertTrue(validate_password_one)
        self.assertTrue(validate_password_two)

    def test_password_with_not_enough_characters_is_invalid(self):
        validate_password = password_strength_validator("Qwerty1")

        self.assertFalse(validate_password)

    def test_password_with_no_capital_letters_is_invalid(self):
        validate_password_one = password_strength_validator("password")
        validate_password_two = password_strength_validator("password123")

        self.assertFalse(validate_password_one)
        self.assertFalse(validate_password_two)

    def test_password_with_no_numbers_is_invalid(self):
        validate_password = password_strength_validator("Password")

        self.assertFalse(validate_password)

    def test_password_with_only_numbers_is_invalid(self):
        validate_password = password_strength_validator(12345678)

        self.assertFalse(validate_password)


class PasswordChangeTest(APITestCase):
    pass

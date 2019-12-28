from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import TestCase
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from api.exceptions import ValidationError
from api.user_authentication import password_strength_validator
from rest_framework.test import APITestCase
from users.models import CustomUser


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


class PasswordUpdateTest(APITestCase):
    def setUp(self):
        self.password_payload = {
            "old_password": "OldPassword123",
            "new_password": "NewPassword123",
            "new_password_confirm": "NewPassword123",
        }
        self.user = CustomUser.objects.create_user(
            username="testuser", password=self.password_payload["old_password"]
        )
        self.client.force_authenticate(self.user)

    def test_can_update_password_for_user(self):
        new_password = self.password_payload["new_password"]
        res = self.client.patch(
            "http://127.0.0.1:8000/api/v1/password", self.password_payload
        )
        changed_user_password = CustomUser.objects.get(
            username=self.user.username
        ).check_password(new_password)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(changed_user_password)

    def test_cannot_update_password_for_unauthorized_user(self):
        self.client.force_authenticate(user=None)
        res = self.client.patch(
            "http://127.0.0.1:8000/api/v1/password", self.password_payload
        )

        self.assertEqual(res.status_code, 401)

    def test_cannot_update_password_if_invalid_old_password_is_provided(self):
        self.password_payload["old_password"] = "InvalidOldPassword123"
        res = self.client.patch(
            "http://127.0.0.1:8000/api/v1/password", self.password_payload
        )

        self.assertEqual(res.status_code, 400)

    def test_cannot_update_password_if_new_password_and_new_password_confirm_do_not_match(
        self
    ):
        self.password_payload["new_password_confirm"] = "InvalidNewPassword123"
        res = self.client.patch(
            "http://127.0.0.1:8000/api/v1/password", self.password_payload
        )

        self.assertEqual(res.status_code, 400)

    def test_cannot_update_password_if_new_password_has_invalid_formatting(
        self
    ):
        self.password_payload["new_password"] = "newpassword123"
        self.password_payload["new_password_confirm"] = "newpassword123"
        res = self.client.patch(
            "http://127.0.0.1:8000/api/v1/password", self.password_payload
        )

        self.assertEqual(res.status_code, 400)


class PasswordResetTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password_payload = {
            "new_password": "NewPassword123",
            "new_password_confirm": "NewPassword123",
        }
        cls.user = CustomUser.objects.create_user(
            username="testuser",
            password="OldPassword123",
            email="mail@testuser.com",
        )
        cls.uid = urlsafe_base64_encode(force_bytes(cls.user.pk))
        cls.token = default_token_generator.make_token(cls.user)

    def test_can_send_password_reset_email(self):
        res = self.client.post(
            "http://127.0.0.1:8000/api/v1/password_reset",
            {"email": "mail@testuser.com"},
        )
        password_reset_url = (
            f"http://testserver/password_reset/{self.uid}/{self.token}"
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(password_reset_url in mail.outbox[0].body)

    def test_cannot_send_password_reset_email_to_nonexistent_email(self):
        res = self.client.post(
            "http://127.0.0.1:8000/api/v1/password_reset",
            {"email": "nonexistent_mail@testuser.com"},
        )

        self.assertEqual(res.status_code, 404)

    def test_cannot_send_password_reset_email_if_request_body_has_invalid_data(
        self
    ):
        res = self.client.post("http://127.0.0.1:8000/api/v1/password_reset")

        self.assertEqual(res.status_code, 400)

    def test_can_reset_password_for_user(self):
        new_password = self.password_payload["new_password"]
        res = self.client.patch(
            f"http://127.0.0.1:8000/api/v1/password_reset/{self.uid}/{self.token}",
            self.password_payload,
        )
        changed_user_password = CustomUser.objects.get(
            username=self.user.username
        ).check_password(new_password)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(changed_user_password)

    def test_cannot_reset_password_if_new_password_and_new_password_confirm_do_not_match(
        self
    ):
        self.password_payload["new_password_confirm"] = "InvalidNewPassword123"
        res = self.client.patch(
            f"http://127.0.0.1:8000/api/v1/password_reset/{self.uid}/{self.token}",
            self.password_payload,
        )

        self.assertEqual(res.status_code, 400)

    def test_cannot_reset_password_if_new_password_has_invalid_formatting(
        self
    ):
        self.password_payload["new_password"] = "newpassword123"
        self.password_payload["new_password_confirm"] = "newpassword123"
        res = self.client.patch(
            f"http://127.0.0.1:8000/api/v1/password_reset/{self.uid}/{self.token}",
            self.password_payload,
        )

        self.assertEqual(res.status_code, 400)

    def test_cannot_reset_password_if_request_body_has_invalid_data(self):
        res = self.client.patch(
            f"http://127.0.0.1:8000/api/v1/password_reset/{self.uid}/{self.token}"
        )

        self.assertEqual(res.status_code, 400)

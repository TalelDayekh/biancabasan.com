from typing import Dict

from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from tests.utils import authorization_test_data
from users.models import CustomUser


class LogoutTest(APITestCase):
    def test_can_logout_user(self):
        password = authorization_test_data()["new_password"]
        user = CustomUser.objects.create_user(
            username="logout_testuser", password=password
        )
        self.client.post(
            "http://127.0.0.1:8000/api/v1/auth/login",
            {"username": "logout_testuser", "password": password},
        )
        self.client.force_authenticate(user)
        res = self.client.post("http://127.0.0.1:8000/api/v1/auth/logout")

        self.assertEqual(res.status_code, 200)
        self.assertFalse(Token.objects.filter(user=user).exists())


class PasswordUpdateTest(APITestCase):
    def setUp(self):
        self.passwords = authorization_test_data()
        old_password = self.passwords["old_password"]
        self.user = CustomUser.objects.create_user(
            username="password_update_testuser", password=old_password
        )
        self.client.force_authenticate(self.user)

    def test_can_update_password_for_user(self):
        new_password = self.passwords["new_password"]
        res = self.client.patch(
            "http://127.0.0.1:8000/api/v1/auth/password_update", self.passwords
        )
        changed_user_password = CustomUser.objects.get(
            username=self.user.username
        ).check_password(new_password)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(changed_user_password)

    def test_cannot_update_password_for_unauthorized_user(self):
        self.client.force_authenticate(user=None)
        res = self.client.patch(
            "http://127.0.0.1:8000/api/v1/auth/password_update", self.passwords
        )

        self.assertEqual(res.status_code, 401)

    def test_cannot_update_password_if_invalid_old_password_is_provided(self):
        self.passwords["old_password"] = "InvalidOldPassword123"
        res = self.client.patch(
            "http://127.0.0.1:8000/api/v1/auth/password_update", self.passwords
        )

        self.assertEqual(res.status_code, 400)

    def test_cannot_update_password_if_new_password_and_new_password_confirm_do_not_match(
        self
    ):
        self.passwords["new_password_confirm"] = "InvalidNewPassword123"
        res = self.client.patch(
            "http://127.0.0.1:8000/api/v1/auth/password_update", self.passwords
        )

        self.assertEqual(res.status_code, 400)

    def test_cannot_update_password_if_new_password_has_invalid_formatting(
        self
    ):
        self.passwords["new_password"] = "newpassword123"
        self.passwords["new_password_confirm"] = "newpassword123"
        res = self.client.patch(
            "http://127.0.0.1:8000/api/v1/auth/password_update", self.passwords
        )

        self.assertEqual(res.status_code, 400)

    def test_cannot_update_password_if_request_body_has_invalid_data(self):
        res = self.client.patch(
            "http://127.0.0.1:8000/api/v1/auth/password_update"
        )

        self.assertEqual(res.status_code, 400)


class PasswordResetTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.passwords = authorization_test_data()
        old_password = cls.passwords["old_password"]
        cls.user = CustomUser.objects.create_user(
            username="password_reset_testuser",
            password=old_password,
            email="mail@test.com",
        )
        cls.uid = urlsafe_base64_encode(force_bytes(cls.user.pk))
        cls.token = default_token_generator.make_token(cls.user)
        super(PasswordResetTest, cls).setUpClass()

    def test_can_send_password_reset_email(self):
        res = self.client.post(
            "http://127.0.0.1:8000/api/v1/auth/password_reset_email",
            {"email": "mail@test.com"},
        )
        password_reset_url = (
            f"http://testserver/password_reset/{self.uid}/{self.token}"
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertTrue(password_reset_url in mail.outbox[0].body)

    def test_cannot_send_password_reset_email_to_nonexistent_email(self):
        res = self.client.post(
            "http://127.0.0.1:8000/api/v1/auth/password_reset_email",
            {"email": "nonexistent_mail@test.com"},
        )

        self.assertEqual(res.status_code, 404)

    def test_cannot_send_password_reset_email_if_request_body_has_invalid_data(
        self
    ):
        res = self.client.post(
            "http://127.0.0.1:8000/api/v1/auth/password_reset_email"
        )

        self.assertEqual(res.status_code, 400)

    def test_can_reset_password_for_user(self):
        new_password = self.passwords["new_password"]
        res = self.client.patch(
            f"http://127.0.0.1:8000/api/v1/auth/password_reset/{self.uid}/{self.token}",
            self.passwords,
        )
        changed_user_password = CustomUser.objects.get(
            username=self.user.username
        ).check_password(new_password)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(changed_user_password)

    def test_cannot_reset_password_if_uid_is_invalid(self):
        invalid_uid = urlsafe_base64_encode(force_bytes(123))
        res = self.client.patch(
            f"http://127.0.0.1:8000/api/v1/auth/password_reset/{invalid_uid}/{self.token}",
            self.passwords,
        )

        self.assertEqual(res.status_code, 404)

    def test_cannot_reset_password_if_token_is_invalid(self):
        invalid_token = "123-abc"
        res = self.client.patch(
            f"http://127.0.0.1:8000/api/v1/auth/password_reset/{self.uid}/{invalid_token}",
            self.passwords,
        )

        self.assertEqual(res.status_code, 400)

    def test_cannot_reset_password_if_new_password_and_new_password_confirm_do_not_match(
        self
    ):
        passwords = self.passwords
        passwords["new_password_confirm"] = "InvalidNewPassword123"
        res = self.client.patch(
            f"http://127.0.0.1:8000/api/v1/auth/password_reset/{self.uid}/{self.token}",
            passwords,
        )

        self.assertEqual(res.status_code, 400)

    def test_cannot_reset_password_if_new_password_has_invalid_formatting(
        self
    ):
        passwords = self.passwords
        passwords["new_password"] = "newpassword123"
        passwords["new_password_confirm"] = "newpassword123"
        res = self.client.patch(
            f"http://127.0.0.1:8000/api/v1/auth/password_reset/{self.uid}/{self.token}",
            passwords,
        )

        self.assertEqual(res.status_code, 400)

    def test_cannot_reset_password_if_request_body_has_invalid_data(self):
        res = self.client.patch(
            f"http://127.0.0.1:8000/api/v1/auth/password_reset/{self.uid}/{self.token}"
        )

        self.assertEqual(res.status_code, 400)

    @classmethod
    def tearDownClass(cls):
        # Adding the tearDownClass seems to prevent
        # connection already closed InterfaceError.
        super(PasswordResetTest, cls).tearDownClass()

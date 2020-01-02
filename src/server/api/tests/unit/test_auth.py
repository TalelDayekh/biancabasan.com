from typing import Dict

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from users.models import CustomUser


def authorization_test_data() -> Dict[str, str]:
    return {
        "old_password": "OldPassword123",
        "new_password": "NewPassword123",
        "new_password_confirm": "NewPassword123",
    }


class LogoutTest(APITestCase):
    def test_can_logout_user(self):
        password = authorization_test_data()["new_password"]
        user = CustomUser.objects.create_user(
            username="testuser", password=password
        )
        self.client.post(
            "http://127.0.0.1:8000/api/v1/login",
            {"username": "testuser", "password": password},
        )
        self.client.force_authenticate(user)
        res = self.client.post("http://127.0.0.1:8000/api/v2/auth/logout")

        self.assertEqual(res.status_code, 200)
        self.assertFalse(Token.objects.filter(user=user).exists())


class PasswordUpdateTest(APITestCase):
    def setUp(self):
        self.passwords = authorization_test_data()
        old_password = self.passwords["old_password"]
        self.user = CustomUser.objects.create_user(
            username="testuser", password=old_password
        )
        self.client.force_authenticate(self.user)

    def test_can_update_password_for_user(self):
        new_password = self.passwords["new_password"]
        res = self.client.patch(
            "http://127.0.0.1:8000/api/v2/auth/password_update", self.passwords
        )
        changed_user_password = CustomUser.objects.get(
            username=self.user.username
        ).check_password(new_password)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(changed_user_password)

    def test_cannot_update_password_for_unauthorized_user(self):
        self.client.force_authenticate(user=None)
        res = self.client.patch(
            "http://127.0.0.1:8000/api/v2/auth/password_update", self.passwords
        )

        self.assertEqual(res.status_code, 401)

    def test_cannot_update_password_if_invalid_old_password_is_provided(self):
        self.passwords["old_password"] = "InvalidOldPassword123"
        res = self.client.patch(
            "http://127.0.0.1:8000/api/v2/auth/password_update", self.passwords
        )

        self.assertEqual(res.status_code, 400)

    def test_cannot_update_password_if_new_password_and_new_password_confirm_do_not_match(
        self
    ):
        self.passwords["new_password_confirm"] = "InvalidNewPassword123"
        res = self.client.patch(
            "http://127.0.0.1:8000/api/v2/auth/password_update", self.passwords
        )

        self.assertEqual(res.status_code, 400)

    def test_cannot_update_password_if_new_password_has_invalid_formatting(
        self
    ):
        self.passwords["new_password"] = "newpassword123"
        self.passwords["new_password_confirm"] = "newpassword123"
        res = self.client.patch(
            "http://127.0.0.1:8000/api/v2/auth/password_update", self.passwords
        )

        self.assertEqual(res.status_code, 400)

    def test_cannot_update_password_if_request_body_has_invalid_data(self):
        res = self.client.patch(
            "http://127.0.0.1:8000/api/v2/auth/password_update"
        )

        self.assertEqual(res.status_code, 400)

from pathlib import Path

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpRequest
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from api.exceptions import ValidationError
from api.serializers import (
    AuthenticationSerializer,
    PasswordResetRequestSerializer,
)
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import CustomUser


def password_strength_validator(password: str) -> bool:
    # Checks that a password has at least one capitalized letter,
    # one number and is longer than or equal to eight characters.
    password = str(password)
    if not (
        any(character.isupper() for character in password)
        and any(character.isdigit() for character in password)
        and len(password) >= 8
    ):
        raise ValidationError(
            "Your password has to be at least 8 characters and contain both digits and upper case letters."
        )


class AuthenticationToken(ObtainAuthToken):
    pass


class PasswordChange(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def patch(self, request: HttpRequest, version: str) -> Response:
        serializer = AuthenticationSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data["old_password"]
            new_password = serializer.data["new_password"]
            new_password_confirm = serializer.data["new_password_confirm"]
            user = CustomUser.objects.get(username=request.user)

            if not (
                new_password == new_password_confirm
                and user.check_password(old_password)
            ):
                return Response(
                    "Wrong password provided or your new password and confirmation password do not match.",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                try:
                    password_strength_validator(new_password)
                    user.set_password(new_password)
                    user.save()
                    return Response(status=status.HTTP_200_OK)
                except ValidationError as err:
                    return Response(
                        str(err), status=status.HTTP_400_BAD_REQUEST
                    )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordReset(APIView):
    def _send_password_reset_email(
        self, email: str, domain: str, use_https: bool = False
    ) -> None:
        try:
            user = CustomUser.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            protocol = "https://" if use_https else "http://"
            password_reset_url = Path(protocol).joinpath(
                domain, "password_reset", uid, token
            )
        except Exception:
            raise ValidationError("Email does not exist.")

    def post(self, request: HttpRequest, version: str) -> Response:
        serializer = PasswordResetRequestSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.data["email"]
            domain = get_current_site(request).domain

            try:
                self._send_password_reset_email(email, domain)
                return Response(status=status.HTTP_200_OK)
            except ValidationError as err:
                return Response(str(err), status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

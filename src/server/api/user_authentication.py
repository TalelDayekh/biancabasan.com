import os
from pathlib import Path
from typing import Type

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpRequest
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from api.exceptions import ValidationError
from api.serializers import (
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
    PasswordUpdateSerializer,
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


def send_password_reset_email(
    user: Type[CustomUser], domain: str, use_https: bool = False
) -> None:
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    protocol = "https://" if use_https else "http://"
    password_reset_url = protocol + str(
        Path(domain).joinpath("password_reset", uid, token)
    )

    email = EmailMessage(
        subject="Password Reset",
        body="Click the link and follow the instructions to reset your password: "
        + str(password_reset_url),
        from_email=os.environ.get("BIANCA_BASAN_EMAIL_USERNAME"),
        to=[user.email],
    )
    email.send()


class AuthenticationToken(ObtainAuthToken):
    pass


class PasswordUpdate(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def patch(self, request: HttpRequest, version: str) -> Response:
        serializer = PasswordUpdateSerializer(data=request.data)

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
    def post(self, request: HttpRequest, version: str) -> Response:
        serializer = PasswordResetRequestSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.data["email"]
            domain = get_current_site(request).domain

            try:
                user = CustomUser.objects.get(email=email)
                send_password_reset_email(user, domain)
                return Response(status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(
        self, request: HttpRequest, version: str, uid: str, token: str
    ) -> Response:
        serializer = PasswordResetSerializer(data=request.data)

        try:
            user_id = urlsafe_base64_decode(uid).decode()
            user = CustomUser.objects.get(id=user_id)

            if not default_token_generator.check_token(user, token):
                raise ValidationError("Token not valid.")
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except ValidationError as err:
            return Response(str(err), status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            new_password = serializer.data["new_password"]
            new_password_confirm = serializer.data["new_password_confirm"]

            try:
                if not new_password == new_password_confirm:
                    raise ValidationError(
                        "Your new password and confirmation password do not match."
                    )
                password_strength_validator(new_password)
                user.set_password(new_password)
                user.save()
                return Response(status=status.HTTP_200_OK)
            except ValidationError as err:
                return Response(str(err), status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

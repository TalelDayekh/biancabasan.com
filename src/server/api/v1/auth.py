from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest
from django.utils.http import urlsafe_base64_decode

from api.v1.serializers import (
    PasswordResetEmailSerializer,
    PasswordResetSerializer,
    PasswordUpdateSerializer,
)
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from users.auth import password_strength_validator, send_password_reset_email
from users.exceptions import ValidationError
from users.models import CustomUser


class Login(ObtainAuthToken):
    pass


class Logout(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request: HttpRequest, format=None) -> Response:
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class PasswordUpdate(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def patch(self, request: HttpRequest, format=None) -> Response:
        serializer = PasswordUpdateSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data["old_password"]
            new_password = serializer.data["new_password"]
            new_password_confirm = serializer.data["new_password_confirm"]
            user = CustomUser.objects.get(username=request.user)

            try:
                if not (
                    new_password == new_password_confirm
                    and user.check_password(old_password)
                ):
                    raise ValidationError(
                        {
                            "message": "Wrong password provided or your new password and confirmation password do not match."
                        }
                    )
                else:
                    password_strength_validator(new_password)
                    user.set_password(new_password)
                    user.save()
                    return Response(status=status.HTTP_200_OK)
            except ValidationError as err:
                return Response(str(err), status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordReset(APIView):
    def post(self, request: HttpRequest, format=None) -> Response:
        serializer = PasswordResetEmailSerializer(data=request.data)

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

    def patch(self, request: HttpRequest, uid: str, token: str) -> Response:
        serializer = PasswordResetSerializer(data=request.data)

        if serializer.is_valid():
            new_password = serializer.data["new_password"]
            new_password_confirm = serializer.data["new_password_confirm"]

            try:
                user_id = urlsafe_base64_decode(uid).decode()
                user = CustomUser.objects.get(id=user_id)

                if not default_token_generator.check_token(user, token):
                    raise ValidationError("Token not valid.")

                if not new_password == new_password_confirm:
                    raise ValidationError(
                        "Your new password and confirmation password do not match."
                    )

                password_strength_validator(new_password)
                user.set_password(new_password)
                user.save()
                return Response(status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            except ValidationError as err:
                return Response(str(err), status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

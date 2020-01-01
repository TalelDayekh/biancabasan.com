from django.http import HttpRequest

from api.v2.serializers import PasswordUpdateSerializer
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from users.auth import password_strength_validator
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
                return Response(err, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

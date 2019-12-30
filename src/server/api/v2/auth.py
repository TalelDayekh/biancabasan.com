from django.http import HttpRequest

from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView


class Logout(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request: HttpRequest, format=None) -> Response:
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

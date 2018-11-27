from django.shortcuts import render

from rest_framework import viewsets
from .serializers import CreateUserSerializer

from django.contrib.auth.models import User


class CreateUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
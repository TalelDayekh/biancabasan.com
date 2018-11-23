from django.shortcuts import render

from rest_framework import viewsets
from .serializers import ArtworkTitleSerializer, ArtworkDetailsSerializer

from .models import ArtworkTitle, ArtworkDetails


class ArtworkTitleViewSet(viewsets.ModelViewSet):
    queryset = ArtworkTitle.objects.all()
    serializer_class = ArtworkTitleSerializer


class ArtworkDetailsViewSet(viewsets.ModelViewSet):
    queryset = ArtworkDetails.objects.all()
    serializer_class = ArtworkDetailsSerializer
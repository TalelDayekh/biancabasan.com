from django.shortcuts import render

from rest_framework import viewsets
from .serializers import ArtworkTitleSerializer, ArtworkDetailsSerializer, ArtworkImagesSerializer

from .models import ArtworkTitle, ArtworkDetails, ArtworkImages


class ArtworkTitleViewSet(viewsets.ModelViewSet):
    queryset = ArtworkTitle.objects.all()
    serializer_class = ArtworkTitleSerializer


class ArtworkDetailsViewSet(viewsets.ModelViewSet):
    queryset = ArtworkDetails.objects.all()
    serializer_class = ArtworkDetailsSerializer


class ArtworkImagesViewSet(viewsets.ModelViewSet):
    queryset = ArtworkImages.objects.all()
    serializer_class = ArtworkImagesSerializer
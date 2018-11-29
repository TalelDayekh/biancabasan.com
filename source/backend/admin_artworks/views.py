from django.shortcuts import render

from rest_framework import viewsets, permissions
from .serializers import ArtworkTitleSerializer, ArtworkDetailsSerializer

from .models import ArtworkTitle, ArtworkDetails


# Artwork title
class ArtworkTitleViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = ArtworkTitle.objects.all()
    serializer_class = ArtworkTitleSerializer

    """
    Custom queryset that filters artwork titles against current logged in user
    but only displays artwork titles by user biancabasan when no one is logged in
    """
    def get_queryset(self):
        filtered_queryset = ArtworkTitle.objects.filter(
            owner__username = 'biancabasan'
            )
        
        if self.request.user.is_authenticated:
            filtered_queryset = self.queryset.filter(
                owner = self.request.user
                )
        
        return filtered_queryset

    # Associate artworks with users
    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)


# Artwork details
class ArtworkDetailsViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = ArtworkDetails.objects.all()
    serializer_class = ArtworkDetailsSerializer

    """
    Custom queryset that filters artwork details against current logged in user
    but only displays artwork details by user biancabasan when no one is logged in
    """
    def get_queryset(self):
        filtered_queryset = ArtworkDetails.objects.filter(
            title_id__owner__username = 'biancabasan'
        )

        if self.request.user.is_authenticated:
            filtered_queryset = self.queryset.filter(
                title_id__owner = self.request.user
            )

        return filtered_queryset
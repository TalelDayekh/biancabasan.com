from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import (
    ArtworkTitlesSerializer,
    ArtworkDetailsSerializer,
    ArtworkImagesSerializer,
)
from ..models import (
    ArtworkTitles,
    ArtworkDetails,
)


"""
Create artwork titles
"""
@api_view(['POST'])
def artwork_create_title(request):

    if request.method == 'POST':
        title_serialized = ArtworkTitlesSerializer(data = request.data)

        if title_serialized.is_valid():
            title_serialized.save()
            return Response(
                title_serialized.data,
                status = status.HTTP_201_CREATED,
                )
        
        return Response(
            title_serialized.errors,
            status = status.HTTP_400_BAD_REQUEST,
        )


"""
Create artwork details
"""
@api_view(['POST'])
def artwork_create_details(request, id):

    if request.method == 'POST':
        # Add details to a specific artwork or raise
        # exception if details already exist
        try:
            ArtworkDetails.objects.get(title_id = id)

        except ArtworkDetails.DoesNotExist:
            details_serialized = ArtworkDetailsSerializer(data = request.data)

            if details_serialized.is_valid():
                details_serialized.save(title_id = id)
    
        else:
            # Retrieve and display artwork title in exception message
            artwork_title = ArtworkTitles.objects.get(id = id)

            return Response(
                ('Unable to create new details for '
                + artwork_title.title
                + ', details already exist'),
                status = status.HTTP_409_CONFLICT
            )
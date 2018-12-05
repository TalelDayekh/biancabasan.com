from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import (
    ArtworkTitlesSerializer,
    ArtworkDetailsSerializer,
)
from ..models import (
    ArtworkTitles,
    ArtworkDetails,
)


"""
List all artwork titles with full details and images
"""
@api_view(['GET'])
def artworks_list(request):

    if request.method == 'GET':
        list_query = ArtworkTitles.objects.all()
        list_serialized = ArtworkTitlesSerializer(
            list_query,
            many = True
        )

        return Response(
            list_serialized.data,
            status = status.HTTP_200_OK
            )
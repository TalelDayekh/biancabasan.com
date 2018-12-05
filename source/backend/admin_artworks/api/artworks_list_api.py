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
List all artwork titles
"""
@api_view(['GET'])
def titles_list(request):

    if request.method == 'GET':
        titles_query = ArtworkTitles.objects.all()
        titles_serialized = ArtworkTitlesSerializer(
            titles_query,
            many = True
        )

        return Response(
            titles_serialized.data,
            status = status.HTTP_200_OK
            )
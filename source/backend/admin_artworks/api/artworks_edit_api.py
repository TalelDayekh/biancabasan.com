from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import (
    ArtworkTitlesSerializer,
    ArtworkDetailsSerializer
)
from ..models import (
    ArtworkTitles,
    ArtworkDetails
)


"""
Edit artwork title and delete artwork object
"""
@api_view(['PUT', 'DELETE'])
def artwork_edit_title(request, id):

    artwork_title_obj = ArtworkTitles.objects.get(id = id)

    if request.method == 'PUT':
        title_serialized = ArtworkTitlesSerializer(
            artwork_title_obj, 
            data = request.data, 
            partial = True
        )

        if title_serialized.is_valid():
            title_serialized.save()

            return Response(
                title_serialized.data,
                status = status.HTTP_201_CREATED
            )

        return Response(
            title_serialized.errors,
            status = status.HTTP_400_BAD_REQUEST
        )

    elif request.method == 'DELETE':
        artwork_title_obj.delete()
        return Response(
            status = status.HTTP_204_NO_CONTENT
        )


"""
Edit artwork details
"""
@api_view(['PUT'])
def artwork_edit_details(request, id):

    artwork_details_obj = ArtworkDetails.objects.get(title = id)

    if request.method == 'PUT':
        details_serialized = ArtworkDetailsSerializer(
            artwork_details_obj,
            data = request.data,
            partial = True
        )

        if details_serialized.is_valid():
            details_serialized.save()

            return Response(
                details_serialized.data,
                status = status.HTTP_201_CREATED
            )
        
        return Response(
            details_serialized.errors,
            status = status.HTTP_400_BAD_REQUEST
        )
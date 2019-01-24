from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import(
    ArtworkSerializer
)
from ..models import(
    ArtworkInfo
)


"""
List all artworks with full details and all images
"""
@api_view(['GET'])
def artworks_list(request):
    if request.method == 'GET':
        querylist = ArtworkInfo.objects.all()
        serialized_querylist = ArtworkSerializer(
            querylist,
            many=True
        )

        return Response(
            serialized_querylist.data,
            status=status.HTTP_200_OK
        )
from rest_framework.decorators import api_view
from rest_framework.response import Response
from artworks.models import ArtworkDetails, ArtworkImages
from .serializers import ArtworksSerializer


@api_view(['GET'])
def artworks_list(request):
    if request.method == 'GET':
        artworks = ArtworkDetails.objects.all()
        serialized_artworks = ArtworksSerializer(
            artworks,
            many=True
        )

        return Response(serialized_artworks.data)
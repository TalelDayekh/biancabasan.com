from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from PIL import Image
from .serializers import(
    ArtworkSerializer,
    ArtworkImagesCreateSerializer
)


"""
Create info for artwork object
"""
@api_view(['POST'])
def create_artwork_info(request):
    if request.method == 'POST':
        serialized_artwork_info = ArtworkSerializer(
            data=request.data,
            partial=True
        )

        if serialized_artwork_info.is_valid():
            serialized_artwork_info.save()
            return Response(
                serialized_artwork_info.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serialized_artwork_info.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
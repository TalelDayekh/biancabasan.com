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


"""
Add images to artwork object
"""
@api_view(['POST'])
# Parser classes used for accepting
# requests with various media types
@parser_classes((MultiPartParser, FormParser))
def add_artwork_images(request):
    if request.method == 'POST':
        # Validate that image file
        # is not larger than 2MB
        if request.data['image'].size > 2000000:
            return Response(
                'Image file is to large',
                status=status.HTTP_406_NOT_ACCEPTABLE
            )

        else:
            serialized_artwork_image = ArtworkImagesCreateSerializer(
                data=request.data
            )
            if serialized_artwork_image.is_valid():
                """
                Image manipulation
                """
                image = serialized_artwork_image.validated_data['image']
                
                # Retrieve image file and image title
                image_title = str(image)
                image_file = Image.open(image)

                # Modify image
                # Resize image and keep proportions
                image_width, image_height = image_file.size
                image_new_width = 1024
                image_new_height = (image_height/image_width) * image_new_width
                modified_image = image_file.resize(
                    (image_new_width, int(round(image_new_height)))
                )
                # Save modified image to in memory buffer and change the
                # previously InMemoryUploadedFile to the newly modified image
                buffer = BytesIO()
                modified_image.save(buffer, format='JPEG', quality=10)
                serialized_artwork_image.validated_data['image'] = InMemoryUploadedFile(
                    buffer,
                    None,
                    image_title,
                    None,
                    None,
                    None
                )
                serialized_artwork_image.save()
                return Response(
                    serialized_artwork_image.data,
                    status=status.HTTP_200_CREATED
                )
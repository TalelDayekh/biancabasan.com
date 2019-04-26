from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from artworks.models import ArtworkDetails, ArtworkImages
from .serializers import ArtworksSerializer, ArtworkImagesSerializer


@api_view(['GET'])
def artworks_list(request):
	if request.method == 'GET':
		artworks = ArtworkDetails.objects.all()
		serialized_artworks = ArtworksSerializer(
			artworks,
			many=True
		)
		return Response(serialized_artworks.data)


@api_view(['POST'])
def create_artwork_details(request):
	if request.method == 'POST':
		serialized_artwork_details = ArtworksSerializer(
			data=request.data,
			partial=True
		)
		
		if serialized_artwork_details.is_valid():
			serialized_artwork_details.save()
			return Response(
				serialized_artwork_details.data,
				status=status.HTTP_201_CREATED
			)
		return Response(
			serialized_artwork_details.error,
			status=status.HTTP_400_BAD_REQUEST
		)


@api_view(['POST'])
def create_artwork_images(request):
	if request.method == 'POST':
		serialized_artwork_images = ArtworkImagesSerializer(
			data=request.data
		)

		if serialized_artwork_images.is_valid():
			serialized_artwork_images.save()
			return Response(
				serialized_artwork_images.data,
				status=status.HTTP_201_CREATED
			)
		return Response(
			serialized_artwork_images.error,
			status=status.HTTP_400_BAD_REQUEST
		)
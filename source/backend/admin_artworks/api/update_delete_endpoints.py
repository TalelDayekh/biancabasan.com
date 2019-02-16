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
Update artwork info and delete artwork object
"""
@api_view(['PUT', 'DELETE'])
def update_delete_artwork_info(request):
    artwork_id = request.data['id']
    artwork_obj = ArtworkInfo.objects.get(id=artwork_id)
    serialized_artwork_info = ArtworkSerializer(
        artwork_obj,
        data=request.data,
        partial=True
    )

    if request.method == 'PUT':
        if serialized_artwork_info.is_valid():
            serialized_artwork_info.save(owner=request.user)
            return Response(
                serialized_artwork_info.data,
                status=status.HTTP_201_CREATED
            )

    elif request.method == 'DELETE':
        if serialized_artwork_info.is_valid():
            # Artworks can only be deleted by its owner
            if str(serialized_artwork_info.data['owner']) == str(request.user):
                artwork_obj.delete()
                return Response(
                    status=status.HTTP_204_NO_CONTENT
                )
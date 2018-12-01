from rest_framework import status

from rest_framework.decorators import (
    api_view,
)

from rest_framework.response import (
    Response,
)

from .serializers import (
    ArtworkTitleSerializer,
)

from .models import (
    ArtworkTitle,
)


# Artwork titles
@api_view(['GET', 'POST'])
def create_title(request):

    """
    Create new artwork title
    """

    if request.method == 'GET':
        artwork_titles_list = ArtworkTitle.objects.all()
        titles_list_serializer = ArtworkTitleSerializer(
            artwork_titles_list,
            many = True
        )

        return Response(titles_list_serializer.data)

    elif request.method == 'POST':
        title_serializer = ArtworkTitleSerializer(data = request.data)
        current_user = request.user

        if title_serializer.is_valid():
            title_serializer.save(owner = current_user)


@api_view(['GET', 'PUT', 'DELETE'])
def edit_titles(request, id):

    """
    Update or delete artwork titles
    """

    # Raise exception if title does not exist
    try:
        artwork_title = ArtworkTitle.objects.get(id = id)
    except ArtworkTitle.DoesNotExist:
        return Response(status = status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET':
        title_serializer = ArtworkTitleSerializer(artwork_title)
        return Response(title_serializer.data)

    elif request.method == 'PUT':
        title_serializer = ArtworkTitleSerializer(
            artwork_title,
            data = request.data
            )
        if title_serializer.is_valid():
            title_serializer.save()
    
    elif request.method == 'DELETE':
        artwork_title.delete()
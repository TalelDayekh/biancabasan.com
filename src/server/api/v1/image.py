from django.http import Http404, HttpRequest

from api.v1.serializers import ImageSerializer
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from works.models import Image


class ImageList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request: HttpRequest, work_id: int, format=None) -> Response:
        images = Image.objects.filter(work_id=work_id)

        if not images:
            raise Http404
        else:
            serializer = ImageSerializer(images, many=True)
            return Response(serializer.data)

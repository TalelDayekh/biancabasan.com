from typing import Type

from django.http import Http404, HttpRequest

from api.v1.serializers import ImageSerializer
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from works.image_handlers import ImageFileHandler, ImageValidationHandler
from works.models import Image, Work


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

    def post(
        self, request: HttpRequest, work_id: int, format=None
    ) -> Response:
        pass


class ImageDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def _get_image_object(self, work_id: int, image_id: int) -> Type[Image]:
        try:
            return Image.objects.get(work_id=work_id, id=image_id)
        except Image.DoesNotExist:
            raise Http404

    def get(
        self, request: HttpRequest, work_id: int, image_id: int, format=None
    ) -> Response:
        image = self._get_image_object(work_id, image_id)
        serializer = ImageSerializer(image)
        return Response(serializer.data)

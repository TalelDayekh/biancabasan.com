from pathlib import Path
from typing import Type

from django.conf import settings
from django.http import Http404, HttpRequest

from api.v1.serializers import ImageSerializer
from rest_framework import status
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
        work_owner = Work.objects.get(id=work_id).owner
        image_validation = ImageValidationHandler(request.FILES["image"])
        serializer = ImageSerializer(data=request.data)

        if (
            serializer.is_valid()
            and image_validation.is_valid()
            and work_owner == request.user
        ):
            serializer.save(work_id=work_id)
            image_file = Path(settings.BASE_DIR + serializer.data["image"])
            ImageFileHandler.create_web_image_set(image_file)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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

    def delete(
        self, request: HttpRequest, work_id: int, image_id: int, format=None
    ) -> Response:
        image = self._get_image_object(work_id, image_id)
        image_owner = image.work.owner
        image_file = Path(image.image.path)

        if image_owner == request.user:
            ImageFileHandler(image_file).delete_image_set()

            if image_file.exists():
                return Response(status=status.HTTP_409_CONFLICT)
            else:
                image.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

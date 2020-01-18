from collections import OrderedDict
from pathlib import Path
from typing import Optional, Type

from django.conf import settings
from django.http import Http404, HttpRequest

from api.v1.serializers import ImageSerializerVersion1, WorkSerializerVersion1
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from works.image_handlers import ImageFileHandler, ImageValidationHandler
from works.models import Image, Work


class GetSerializerClasses:
    api_work_serializer_mapping = {"v1": WorkSerializerVersion1}
    api_image_serializer_mapping = {"v1": ImageSerializerVersion1}

    def __init__(self, api_version: str) -> None:
        self.api_version = api_version

    @property
    def work_serializer(self) -> object:
        return self.api_work_serializer_mapping.get(self.api_version)

    @property
    def image_serializer(self) -> object:
        return self.api_image_serializer_mapping.get(self.api_version)


# class WorkDetail(APIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def delete(
#         self, request: HttpRequest, version: str, work_id: int, format=None
#     ) -> Response:
#         work = self.get_work_object(work_id, request.user)

#         for image in work.images.all():
#             image_file = Path(image.image.path)
#             ImageFileHandler(image_file).delete_image_set()

#             if image_file.exists():
#                 return Response(status=status.HTTP_409_CONFLICT)

#         work.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class ImageList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get(
        self, request: HttpRequest, version: str, work_id: int, format=None
    ) -> Response:
        image_serializer = GetSerializerClasses(version).image_serializer
        images = Image.objects.filter(work_id=work_id)

        if not images:
            raise Http404
        else:
            serializer = image_serializer(images, many=True)
            return Response(serializer.data)

    def post(
        self, request: HttpRequest, version: str, work_id: int, format=None
    ) -> Response:
        work_owner = Work.objects.get(id=work_id).owner
        image_serializer = GetSerializerClasses(version).image_serializer
        image_validation = ImageValidationHandler(request.FILES["image"])
        serializer = image_serializer(data=request.data)

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

    def get_image_object(self, work_id: int, image_id: int) -> Type[Image]:
        try:
            return Image.objects.get(work_id=work_id, id=image_id)
        except Image.DoesNotExist:
            raise Http404

    def get(
        self,
        request: HttpRequest,
        version: str,
        work_id: int,
        image_id: int,
        format=None,
    ) -> Response:
        image_serializer = GetSerializerClasses(version).image_serializer
        image = self.get_image_object(work_id, image_id)
        serializer = image_serializer(image)
        return Response(serializer.data)

    def delete(
        self,
        request: HttpRequest,
        version: str,
        work_id: int,
        image_id: int,
        format=None,
    ) -> Response:
        image = self.get_image_object(work_id, image_id)
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
            raise Http404

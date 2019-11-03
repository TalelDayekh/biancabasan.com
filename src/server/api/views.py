from collections import OrderedDict
from pathlib import Path
from typing import Optional, Type

from django.conf import settings
from django.http import Http404, HttpRequest

from api.v1.serializers import ImageSerializerVersion1, WorkSerializerVersion1
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
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


class WorkList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request: HttpRequest, version: str, format=None) -> Response:
        work_serializer = GetSerializerClasses(version).work_serializer
        query_params = self.request.query_params.get("year_to")

        try:
            if query_params:
                works = Work.objects.filter(year_to=query_params)
                serializer = work_serializer(works, many=True)
            else:
                works = Work.objects.all()
                serializer = work_serializer(works, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(
        self, request: HttpRequest, version: str, format=None
    ) -> Response:
        work_serializer = GetSerializerClasses(version).work_serializer
        serializer = work_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class WorkDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_work_object(self, work_id: int) -> Type[Work]:
        try:
            return Work.objects.get(id=work_id)
        except Work.DoesNotExist:
            raise Http404

    def get(
        self, request: HttpRequest, version: str, work_id: int, format=None
    ) -> Response:
        work_serializer = GetSerializerClasses(version).work_serializer
        work = self.get_work_object(work_id)
        serializer = work_serializer(work)
        return Response(serializer.data)


class WorkYearsList(APIView):
    def get(self, request: HttpRequest, version: str, format=None) -> Response:
        work_years = Work.objects.all().values_list("year_to", flat=True)

        # Sort all work years descending and remove duplicate years
        work_years_descending = sorted(work_years, reverse=True)
        work_years_sorted = list(OrderedDict.fromkeys(work_years_descending))
        return Response(work_years_sorted)


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

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


# def get_work_object(user: str, work_id: int) -> Type[Work]:
#     try:
#         return Work.objects.get(owner__username=user, id=work_id)
#     except Work.DoesNotExist:
#         raise Http404

# class AllWorks(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request: HttpRequest, version: str, format=None) -> Response:
#         work_serializer = GetSerializerClasses(version).work_serializer
#         query_params = self.request.query_params.get("year_to")

#         try:
#             if query_params:
#                 works = Work.objects.filter(
#                     owner__username=request.user, year_to=query_params
#                 )
#                 serializer = work_serializer(works, many=True)
#             else:
#                 works = Work.objects.filter(owner__username=request.user)
#                 serializer = work_serializer(works, many=True)
#             return Response(serializer.data)
#         except ValueError:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#     def post(
#         self, request: HttpRequest, version: str, format=None
#     ) -> Response:
#         work_serializer = GetSerializerClasses(version).work_serializer
#         serializer = work_serializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save(owner=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class SingleWork(APIView):
#     permission_classes = [IsAuthenticated]

#     def get_object(self, username: str, work_id: int) -> object:
#         try:
#             return Work.objects.get(owner__username=username, id=work_id)
#         except Work.DoesNotExist:
#             raise Http404

#     def get(
#         self, request: HttpRequest, version: str, work_id: int, format=None
#     ) -> Response:
#         work_serializer = GetSerializerClasses(version).work_serializer
#         work = self.get_object(request.user, work_id)
#         serializer = work_serializer(work)
#         return Response(serializer.data)

#     def patch(
#         self, request: HttpRequest, version: str, work_id: int, format=None
#     ) -> Response:
#         work_serializer = GetSerializerClasses(version).work_serializer
#         work = self.get_object(request.user, work_id)
#         serializer = work_serializer(work, data=request.data, partial=True)

#         if serializer.is_valid():
#             serializer.save(owner=request.user)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(
#         self, request: HttpRequest, version: str, work_id: int, format=None
#     ) -> Response:
#         work = self.get_object(request.user, work_id)
#         work.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class YearsToList(APIView):
#     def get(
#         self, request: HttpRequest, version: str, username: str, format=None
#     ) -> Response:
#         work_serializer = GetSerializerClasses(version).work_serializer
#         years_to = Work.objects.filter(owner__username=username).values_list(
#             "year_to", flat=True
#         )

#         # Sort all year_to descending and remove duplicate years
#         years_to_descending = sorted(years_to, reverse=True)
#         sorted_years_to = list(OrderedDict.fromkeys(years_to_descending))

#         return Response(sorted_years_to)

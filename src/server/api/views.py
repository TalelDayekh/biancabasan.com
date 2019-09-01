from django.http import HttpRequest

from api.v1.serializers import ImageSerializerVersion1, WorkSerializerVersion1
from rest_framework.response import Response
from rest_framework.views import APIView

from works.models import Work


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


class Works(APIView):
    def get(
        self, request: HttpRequest, version: str, username: str, format=None
    ) -> Response:
        work_serializer = GetSerializerClasses(version).work_serializer
        works = Work.objects.filter(owner__username=username)
        serializer = work_serializer(works, many=True)
        return Response(serializer.data)

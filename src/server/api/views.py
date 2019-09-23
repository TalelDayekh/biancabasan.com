from django.http import Http404, HttpRequest

from api.v1.serializers import ImageSerializerVersion1, WorkSerializerVersion1
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
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


class AllWorks(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: HttpRequest, version: str, format=None) -> Response:
        work_serializer = GetSerializerClasses(version).work_serializer
        query_params = self.request.query_params.get("year_to")

        try:
            if query_params:
                works = Work.objects.filter(
                    owner__username=request.user, year_to=query_params
                )
                serializer = work_serializer(works, many=True)
            else:
                works = Work.objects.filter(owner__username=request.user)
                serializer = work_serializer(works, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response(data=[], status=status.HTTP_400_BAD_REQUEST)

    def post(
        self, request: HttpRequest, version: str, format=None
    ) -> Response:
        work_serializer = GetSerializerClasses(version).work_serializer
        serializer = work_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SingleWork(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, username: str, pk: int) -> object:
        try:
            return Work.objects.get(owner__username=username, id=pk)
        except Work.DoesNotExist:
            raise Http404

    def get(
        self, request: HttpRequest, version: str, pk: int, format=None
    ) -> Response:
        work_serializer = GetSerializerClasses(version).work_serializer
        work = self.get_object(request.user, pk)
        serializer = work_serializer(work)
        return Response(serializer.data)

    def put(
        self, request: HttpRequest, version: str, pk: int, format=None
    ) -> Response:
        pass

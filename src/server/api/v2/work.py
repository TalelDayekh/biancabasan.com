from collections import OrderedDict

from django.http import HttpRequest

from api.v2.serializers import WorkSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from works.models import Work


class WorkList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request: HttpRequest, format=None) -> Response:
        query_params = self.request.query_params.get("year_to")

        try:
            if query_params:
                works = Work.objects.filter(year_to=query_params)
                serializer = WorkSerializer(works, many=True)
            else:
                works = Work.objects.all()
                serializer = WorkSerializer(works, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class WorkYearsList(APIView):
    def get(self, request: HttpRequest, format=None) -> Response:
        work_years = Work.objects.all().values_list("year_to", flat=True)

        # Sort all work years descending and remove duplicate years
        work_years_descending = sorted(work_years, reverse=True)
        work_years_sorted = list(OrderedDict.fromkeys(work_years_descending))
        return Response(work_years_sorted, status=status.HTTP_200_OK)

from django.test import TestCase
from django.urls import reverse

from api.v1.serializers import WorkSerializerVersion1
from api.views import GetSerializerClasses, Works
from rest_framework.test import APITestCase
from users.models import CustomUser

from works.models import Work


class SerializerRetrievalTest(TestCase):
    def test_can_get_correct_serializers_for_api_version(self):
        work_serializer = GetSerializerClasses("v1").work_serializer
        image_serializer = GetSerializerClasses("v1").image_serializer

        self.assertEqual(work_serializer.__name__, "WorkSerializerVersion1")
        self.assertEqual(image_serializer.__name__, "ImageSerializerVersion1")


class WorksAPIRequestTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="matisse")
        self.work = Work.objects.create(
            owner=self.user,
            title="Dance",
            year_from=1910,
            year_to=1910,
            technique="Oil on canvas",
            height=260,
            width=391,
            description=(
                "The painting shows five dancing figures, painted in a strong red,"
                " set against a very simplified green landscape and deep blue sky."
            ),
        )

    def test_can_get_works_for_specific_user(self):
        response = self.client.get(
            reverse("Works", kwargs={"version": "v1", "username": self.user})
        )
        works = Work.objects.filter(owner__username=self.user)
        serializer = WorkSerializerVersion1(works, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

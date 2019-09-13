from django.test import TestCase

from api.v1.serializers import WorkSerializerVersion1
from api.views import AllWorks, GetSerializerClasses, SingleWork
from rest_framework.test import APITestCase
from users.models import CustomUser

from works.models import Work


class SerializerRetrievalTest(TestCase):
    def test_can_get_correct_serializers_for_api_version(self):
        work_serializer = GetSerializerClasses("v1").work_serializer
        image_serializer = GetSerializerClasses("v1").image_serializer

        self.assertEqual(work_serializer.__name__, "WorkSerializerVersion1")
        self.assertEqual(image_serializer.__name__, "ImageSerializerVersion1")


class WorksGetRequestTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_one = CustomUser.objects.create(username="matisse")
        cls.user_one_work = Work.objects.create(
            owner=cls.user_one,
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

        cls.user_two = CustomUser.objects.create(username="rousseau")
        cls.user_two_work = Work.objects.bulk_create(
            [
                Work(
                    owner=cls.user_two,
                    title="Exotic Landscape",
                    year_to=1908,
                    technique="Oil on canvas",
                    description=(
                        "The painting shows monkeys picking up oranges it has"
                        " rich shades of green used in the leaves, grass and "
                        "trees of the jungle."
                    ),
                ),
                Work(
                    owner=cls.user_two,
                    title="Combat of a Tiger and a Buffalo",
                    year_to=1908,
                    technique="Oil on canvas",
                    description=(
                        "The painting shows a imaginary scene of a tiger attacking a"
                        " buffalo within a fantastic jungle environment derived from"
                        " reading travel books and visiting the botanical garden."
                    ),
                ),
                Work(
                    owner=cls.user_two,
                    title="The Dream",
                    year_to=1910,
                    technique="Oil on canvas",
                    description=(
                        "The painting shows an almost surreal portrait of Rousseau's "
                        "mistress lying naked on a divan, gazing over a landscape of "
                        "lotus flowers and animals."
                    ),
                ),
            ]
        )

    def test_can_get_works_for_specific_user(self):
        response = self.client.get(
            "http://127.0.0.1:8000/api/v1/users/matisse/works/"
        )
        works = Work.objects.filter(owner__username=self.user_one)
        serializer = WorkSerializerVersion1(works, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_cannot_get_works_for_non_existing_user(self):
        response = self.client.get(
            "http://127.0.0.1:8000/api/v1/users/non-existing-user/works/"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_can_get_works_from_year_to_for_specific_user(self):
        response = self.client.get(
            "http://127.0.0.1:8000/api/v1/users/rousseau/works/",
            {"year_to": 1908},
        )
        works = Work.objects.filter(
            owner__username=self.user_two, year_to=1908
        )
        serializer = WorkSerializerVersion1(works, many=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_cannot_get_works_from_non_year(self):
        response = self.client.get(
            "http://127.0.0.1:8000/api/v1/users/rousseau/works/",
            {"year_to": "not a year"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, [])


class SingleWorkGETRequestTest(APITestCase):
    pass

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


class WorkViewsGETTest(APITestCase):
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
                "Five dancing figures painted in a strong red and set"
                " against a green landscape and deep blue sky."
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
                        "Monkeys picking up oranges in a jungle painted with"
                        " rich greens in the leaves, grass and trees."
                    ),
                ),
                Work(
                    owner=cls.user_two,
                    title="Fight Between a Tiger and a Buffalo",
                    year_to=1908,
                    technique="Oil on canvas",
                    description=(
                        "A imaginary scene of a tiger attacking a buffalo in"
                        " a fantastic jungle environment."
                    ),
                ),
                Work(
                    owner=cls.user_two,
                    title="The Dream",
                    year_to=1910,
                    technique="Oil on canvas",
                    description=(
                        "A surreal scene of Rousseau's mistress on a divan,"
                        "gazing over a landscape of flowers and animals."
                    ),
                ),
            ]
        )

    def test_can_get_all_works_for_user(self):
        self.client.force_authenticate(self.user_one)

        res = self.client.get("http://127.0.0.1:8000/api/v1/works/")
        works = Work.objects.filter(owner__username=self.user_one)
        serializer = WorkSerializerVersion1(works, many=True)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)

    def test_cannot_get_works_for_unauthorized_user(self):
        res = self.client.get("http://127.0.0.1:8000/api/v1/works/")

        self.assertEqual(res.status_code, 401)

    def test_can_get_all_works_from_year_to_for_user(self):
        self.client.force_authenticate(self.user_two)

        res = self.client.get(
            "http://127.0.0.1:8000/api/v1/works/", {"year_to": 1908}
        )
        works = Work.objects.filter(
            owner__username=self.user_two, year_to=1908
        )
        serializer = WorkSerializerVersion1(works, many=True)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)

    def test_cannot_get_works_from_non_existing_year_to(self):
        self.client.force_authenticate(self.user_two)

        res = self.client.get(
            "http://127.0.0.1:8000/api/v1/works/", {"year_to": "not a year"}
        )

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data, [])

    def test_can_get_single_work_for_user(self):
        self.client.force_authenticate(self.user_two)

        res = self.client.get("http://127.0.0.1:8000/api/v1/works/4/")
        work = Work.objects.filter(owner__username=self.user_two, id=4)
        serializer = WorkSerializerVersion1(work, many=True)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)

    def test_cannot_get_work_from_invalid_id(self):
        self.client.force_authenticate(self.user_two)

        res_invalid_int = self.client.get(
            "http://127.0.0.1:8000/api/v1/works/1000/"
        )
        res_invalid_str = self.client.get(
            "http://127.0.0.1:8000/api/v1/works/not-a-integer/"
        )

        self.assertEqual(res_invalid_int.status_code, 200)
        self.assertEqual(res_invalid_int.data, [])
        self.assertEqual(res_invalid_str.status_code, 404)


class WorkViewPOSTTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="adrianghenie")
        self.valid_payload = {
            "title": "The Sunflowers in 1937",
            "year_to": 2014,
            "technique": "Oil on canvas",
            "description": "A homage to Van Gogh's sunflowers.",
        }
        self.invalid_payload = {
            "title": "",
            "year_to": "",
            "technique": "",
            "description": "",
        }

    def test_can_create_work_for_user(self):
        self.client.force_authenticate(self.user)

        res = self.client.post(
            "http://127.0.0.1:8000/api/v1/works/", self.valid_payload
        )

        self.assertEqual(res.status_code, 201)

    def test_cannot_create_work_for_unauthorized_user(self):
        res = self.client.post(
            "http://127.0.0.1:8000/api/v1/works/", self.valid_payload
        )

        self.assertEqual(res.status_code, 401)

    def test_cannot_create_work_from_invalid_payload(self):
        self.client.force_authenticate(self.user)

        res = self.client.post(
            "http://127.0.0.1:8000/api/v1/works/", self.invalid_payload
        )

        self.assertEqual(res.status_code, 400)

    def test_cannot_create_work_from_non_selectable_year(self):
        self.client.force_authenticate(self.user)

        self.valid_payload["year_to"] = 1888
        res = self.client.post(
            "http://127.0.0.1:8000/api/v1/works/", self.valid_payload
        )

        self.assertEqual(res.status_code, 400)

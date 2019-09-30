from api.v1.serializers import WorkSerializerVersion1
from rest_framework.test import APITestCase
from users.models import CustomUser

from works.models import Work


def test_data():
    return [
        {
            "title": "Exotic Landscape",
            "year_to": 1908,
            "technique": "Oil on canvas",
            "description": "Monkeys picking up oranges in a jungle painted with rich greens in the leaves, grass and trees.",
        },
        {
            "title": "Fight Between a Tiger and a Buffalo",
            "year_to": 1908,
            "technique": "Oil on canvas",
            "description": "A imaginary scene of a tiger attacking a buffalo in a fantastic jungle environment.",
        },
        {
            "title": "The Dream",
            "year_to": 1910,
            "technique": "Oil on canvas",
            "description": "A surreal scene of Rousseau's mistress on a divan, gazing over a landscape of flowers and animals.",
        },
        {
            "title": "Teenage Wildlife",
            "year_to": 2003,
            "technique": "Oil on canvas",
            "description": "Life, colour, motion and erotic power pervades this abstract expressionist work.",
        },
        {"title": "", "year_to": "", "technique": "", "description": ""},
    ]


class WorksGETTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="rousseau")
        self.client.force_authenticate(self.user)
        Work.objects.bulk_create(
            [
                Work(owner=self.user, **test_data()[0]),
                Work(owner=self.user, **test_data()[1]),
                Work(owner=self.user, **test_data()[2]),
            ]
        )

    def test_can_get_all_works_for_user(self):
        res = self.client.get("http://127.0.0.1:8000/api/v1/works/")
        works = Work.objects.filter(owner__username=self.user)
        serializer = WorkSerializerVersion1(works, many=True)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)

    def test_cannot_get_works_for_unauthorized_user(self):
        self.client.force_authenticate(user=None)
        res = self.client.get("http://127.0.0.1:8000/api/v1/works/")

        self.assertEqual(res.status_code, 401)

    def test_can_get_all_works_from_year_to_for_user(self):
        res = self.client.get(
            "http://127.0.0.1:8000/api/v1/works/", {"year_to": 1908}
        )
        works = Work.objects.filter(owner__username=self.user, year_to=1908)
        serializer = WorkSerializerVersion1(works, many=True)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)

    def test_cannot_get_works_from_non_existing_year_to(self):
        res = self.client.get(
            "http://127.0.0.1:8000/api/v1/works/", {"year_to": "not a year"}
        )

        self.assertEqual(res.status_code, 400)

    def test_can_get_sorted_list_of_year_to_for_user(self):
        res = self.client.get(
            f"http://127.0.0.1:8000/api/v1/{self.user}/works/years/"
        )

        self.assertEqual(res.data, [1910, 1908])

    def test_can_get_single_work_for_user(self):
        # Get id from work title instead of hardcoding it in the request
        # in case the database provides different id values on testruns.
        work = Work.objects.get(owner__username=self.user, title="The Dream")
        work_id = work.id
        res = self.client.get(f"http://127.0.0.1:8000/api/v1/works/{work_id}/")
        serializer = WorkSerializerVersion1(work)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)

    def test_cannot_get_work_from_invalid_id(self):
        res_int = self.client.get("http://127.0.0.1:8000/api/v1/works/9999/")
        res_str = self.client.get("http://127.0.0.1:8000/api/v1/works/NaN/")

        self.assertEqual(res_int.status_code, 404)
        self.assertEqual(res_str.status_code, 404)


class WorksPOSTTest(APITestCase):
    def setUp(self):
        user = CustomUser.objects.create(username="cecilybrown")
        self.client.force_authenticate(user)

    def test_can_create_work_for_user(self):
        res = self.client.post(
            "http://127.0.0.1:8000/api/v1/works/", test_data()[3]
        )

        self.assertEqual(res.status_code, 201)

    def test_cannot_create_work_for_unauthorized_user(self):
        self.client.force_authenticate(user=None)
        res = self.client.post(
            "http://127.0.0.1:8000/api/v1/works/", test_data()[3]
        )

        self.assertEqual(res.status_code, 401)

    def test_cannot_create_work_from_invalid_payload(self):
        res = self.client.post(
            "http://127.0.0.1:8000/api/v1/works/", test_data()[4]
        )

        self.assertEqual(res.status_code, 400)

    def test_cannot_create_work_from_non_selectable_year(self):
        valid_payload = test_data()[3]
        valid_payload["year_to"] = 1986
        res = self.client.post(
            "http://127.0.0.1:8000/api/v1/works/", valid_payload
        )

        self.assertEqual(res.status_code, 400)


class WorksPATCHTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(username="cecilybrown")
        self.client.force_authenticate(self.user)
        work = Work.objects.create(owner=self.user, **test_data()[3])
        self.work_id = work.id
        self.updated_payload = {"year_from": 2003, "height": 203, "width": 229}

    def test_can_update_work_for_user(self):
        res = self.client.patch(
            f"http://127.0.0.1:8000/api/v1/works/{self.work_id}/",
            self.updated_payload,
        )

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.data["year_from"])
        self.assertTrue(res.data["height"])
        self.assertTrue(res.data["width"])

    def test_cannot_update_work_for_unauthorized_user(self):
        self.client.force_authenticate(user=None)
        res = self.client.patch(
            f"http://127.0.0.1:8000/api/v1/works/{self.work_id}/",
            self.updated_payload,
        )

        self.assertEqual(res.status_code, 401)

    def test_cannot_update_work_from_invalid_id(self):
        res_int = self.client.patch(
            "http://127.0.0.1:8000/api/v1/works/9999/", self.updated_payload
        )
        res_str = self.client.patch(
            "http://127.0.0.1:8000/api/v1/works/NaN/", self.updated_payload
        )

        self.assertEqual(res_int.status_code, 404)
        self.assertEqual(res_str.status_code, 404)


class WorksDELETETest(APITestCase):
    def setUp(self):
        user = CustomUser.objects.create(username="rousseau")
        self.client.force_authenticate(user)
        Work.objects.bulk_create(
            [
                Work(owner=user, **test_data()[0]),
                Work(owner=user, **test_data()[1]),
                Work(owner=user, **test_data()[2]),
            ]
        )
        work_to_delete = Work.objects.get(
            owner__username=user, title="The Dream"
        )
        self.work_to_delete_id = work_to_delete.id

    def test_can_delete_work_for_user(self):
        res_delete = self.client.delete(
            f"http://127.0.0.1:8000/api/v1/works/{self.work_to_delete_id}/"
        )
        res_get = self.client.get(
            f"http://127.0.0.1:8000/api/v1/works/{self.work_to_delete_id}/"
        )

        self.assertEqual(res_delete.status_code, 204)
        self.assertEqual(res_get.status_code, 404)

    def test_cannot_delete_work_for_unauthorized_user(self):
        self.client.force_authenticate(user=None)
        res = self.client.delete(
            f"http://127.0.0.1:8000/api/v1/works/{self.work_to_delete_id}/"
        )

        self.assertEqual(res.status_code, 401)

from api.tests.unit.utils import work_test_data
from api.v2.serializers import WorkSerializer
from rest_framework.test import APITestCase
from users.models import CustomUser

from works.models import Work


class WorkGETTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        user = CustomUser.objects.create_user(username="get_work_testuser")
        Work.objects.bulk_create(
            [
                Work(owner=user, **work_test_data()[0]),
                Work(owner=user, **work_test_data()[1]),
                Work(owner=user, **work_test_data()[2]),
            ]
        )
        super(WorkGETTest, cls).setUpClass()

    def test_can_get_all_works(self):
        res = self.client.get("http://127.0.0.1:8000/api/v2/works")
        works = Work.objects.all()
        serializer = WorkSerializer(works, many=True)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)

    def test_can_get_all_works_from_year_to(self):
        res = self.client.get(
            "http://127.0.0.1:8000/api/v2/works", {"year_to": 2019}
        )
        works = Work.objects.filter(year_to=2019)
        serializer = WorkSerializer(works, many=True)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)

    def test_cannot_get_works_from_invalid_year_to(self):
        res_invalid_year_to_int = self.client.get(
            "http://127.0.0.1:8000/api/v2/works", {"year_to": 2020}
        )
        res_invalid_year_to_str = self.client.get(
            "http://127.0.0.1:8000/api/v2/works", {"year_to": "NaN"}
        )

        self.assertEqual(res_invalid_year_to_int.data, [])
        self.assertEqual(res_invalid_year_to_int.status_code, 400)
        self.assertEqual(res_invalid_year_to_str.data, None)
        self.assertEqual(res_invalid_year_to_str.status_code, 400)

    @classmethod
    def tearDownClass(cls):
        # Adding the tearDownClass seems to prevent
        # connection already closed InterfaceError.
        super(WorkGETTest, cls).tearDownClass()

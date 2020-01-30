import shutil
import tempfile
from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

from api.tests.unit.utils import create_temporary_test_image, work_test_data
from api.v1.serializers import WorkSerializer
from rest_framework.test import APITestCase
from users.models import CustomUser

from works.models import Image, Work

work_delete_request_test_folder = tempfile.mkdtemp(
    prefix="work_delete_request_test_folder"
)


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
        res = self.client.get("http://127.0.0.1:8000/api/v1/works")
        works = Work.objects.all()
        serializer = WorkSerializer(works, many=True)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)

    def test_can_get_all_works_from_year_to(self):
        res = self.client.get(
            "http://127.0.0.1:8000/api/v1/works", {"year_to": 2019}
        )
        works = Work.objects.filter(year_to=2019)
        serializer = WorkSerializer(works, many=True)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)

    def test_cannot_get_works_from_invalid_year_to(self):
        res_invalid_year_to_int = self.client.get(
            "http://127.0.0.1:8000/api/v1/works", {"year_to": 2020}
        )
        res_invalid_year_to_str = self.client.get(
            "http://127.0.0.1:8000/api/v1/works", {"year_to": "NaN"}
        )

        self.assertEqual(res_invalid_year_to_int.data, [])
        self.assertEqual(res_invalid_year_to_str.data, None)
        self.assertEqual(res_invalid_year_to_str.status_code, 400)

    def test_can_get_sorted_list_of_years(self):
        res = self.client.get("http://127.0.0.1:8000/api/v1/works/years")

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, [2019, 2018])

    def test_can_get_work_from_id(self):
        work = Work.objects.get(title="Black Square #3")
        res = self.client.get(f"http://127.0.0.1:8000/api/v1/works/{work.id}")
        serializer = WorkSerializer(work)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)

    def test_cannot_get_work_from_invalid_id(self):
        res_invalid_id_int = self.client.get(
            "http://127.0.0.1:8000/api/v1/works/999"
        )
        res_invalid_id_str = self.client.get(
            "http://127.0.0.1:8000/api/v1/works/NaN"
        )

        self.assertEqual(res_invalid_id_int.status_code, 404)
        self.assertEqual(res_invalid_id_str.status_code, 404)

    @classmethod
    def tearDownClass(cls):
        # Adding the tearDownClass seems to prevent
        # connection already closed InterfaceError.
        super(WorkGETTest, cls).tearDownClass()


class WorkPOSTTest(APITestCase):
    def setUp(self):
        user = CustomUser.objects.create_user(username="post_work_testuser")
        self.client.force_authenticate(user)

    def test_can_create_work_for_user(self):
        res = self.client.post(
            "http://127.0.0.1:8000/api/v1/works", work_test_data()[0]
        )

        self.assertEqual(res.status_code, 201)

    def test_cannot_create_work_as_unauthorized_user(self):
        self.client.force_authenticate(user=None)
        res = self.client.post(
            "http://127.0.0.1:8000/api/v1/works", work_test_data()[0]
        )

        self.assertEqual(res.status_code, 401)

    def test_cannot_create_work_from_invalid_payload(self):
        res = self.client.post(
            "http://127.0.0.1:8000/api/v1/works", work_test_data()[4]
        )

        self.assertEqual(res.status_code, 400)

    def test_cannot_create_work_with_out_of_range_year(self):
        res = self.client.post(
            "http://127.0.0.1:8000/api/v1/works", work_test_data()[3]
        )

        self.assertEqual(res.status_code, 400)

    @classmethod
    def tearDownClass(cls):
        # Adding the tearDownClass seems to prevent
        # connection already closed interfaceError.
        super(WorkPOSTTest, cls).tearDownClass()


class WorkPATCHTest(APITestCase):
    def setUp(self):
        user_one = CustomUser.objects.create_user(
            username="patch_work_testuser_one"
        )
        user_two = CustomUser.objects.create_user(
            username="patch_work_testuser_two"
        )
        user_one_work = Work.objects.create(
            owner=user_one, **work_test_data()[0]
        )
        user_two_work = Work.objects.create(
            owner=user_two, **work_test_data()[0]
        )
        self.user_one_work_id = user_one_work.id
        self.user_two_work_id = user_two_work.id
        self.patch_payload = {
            "year_to": 2020,
            "height": 100.00,
            "width": 100.00,
        }
        self.client.force_authenticate(user_one)

    def test_can_update_work_for_user(self):
        res = self.client.patch(
            f"http://127.0.0.1:8000/api/v1/works/{self.user_one_work_id}",
            self.patch_payload,
        )

        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.data["year_to"] == 2020)
        self.assertTrue(res.data["height"] == 100.00)
        self.assertTrue(res.data["width"] == 100.00)

    def test_cannot_update_work_for_other_user(self):
        res = self.client.patch(
            f"http://127.0.0.1:8000/api/v1/works/{self.user_two_work_id}",
            self.patch_payload,
        )

        self.assertEqual(res.status_code, 404)

    def test_cannot_update_work_as_unauthorized_user(self):
        self.client.force_authenticate(user=None)
        res = self.client.patch(
            f"http://127.0.0.1:8000/api/v1/works/{self.user_one_work_id}",
            self.patch_payload,
        )

        self.assertEqual(res.status_code, 401)

    def test_cannot_update_work_from_invalid_id(self):
        res_invalid_id_int = self.client.patch(
            "http://127.0.0.1:8000/api/v1/999", self.patch_payload
        )
        res_invalid_id_str = self.client.patch(
            "http://127.0.0.1:8000/api/v1/NaN", self.patch_payload
        )

        self.assertEqual(res_invalid_id_int.status_code, 404)
        self.assertEqual(res_invalid_id_str.status_code, 404)

    @classmethod
    def tearDownClass(cls):
        # Adding the tearDownClass seems to prevent
        # connection already closed interfaceError.
        super(WorkPATCHTest, cls).tearDownClass()


@override_settings(
    BASE_DIR=work_delete_request_test_folder,
    MEDIA_URL="/",
    MEDIA_ROOT=work_delete_request_test_folder,
)
class WorkDELETETest(APITestCase):
    def setUp(self):
        user_one = CustomUser.objects.create_user(
            username="delete_work_testuser_one"
        )
        user_two = CustomUser.objects.create_user(
            username="delete_work_testuser_two"
        )
        self.user_one_work = Work.objects.create(
            owner=user_one, **work_test_data()[0]
        )
        user_two_work = Work.objects.create(
            owner=user_two, **work_test_data()[0]
        )
        self.user_one_work_id = self.user_one_work.id
        self.user_two_work_id = user_two_work.id
        self.uploaded_images_paths = []
        self.client.force_authenticate(user_one)

        for i in range(5):
            with create_temporary_test_image("JPEG") as test_image:
                image = Image.objects.create(
                    work=self.user_one_work,
                    image=SimpleUploadedFile(
                        f"Black Square {i + 1}.JPEG", test_image.read()
                    ),
                )
                self.uploaded_images_paths.append(Path(image.image.path))

    def test_can_delete_work_for_user(self):
        res = self.client.delete(
            f"http://127.0.0.1:8000/api/v1/works/{self.user_one_work_id}"
        )

        for image in self.uploaded_images_paths:
            self.assertFalse(image.exists())
        self.assertEqual(res.status_code, 204)

    def test_cannot_delete_work_by_other_user(self):
        res = self.client.delete(
            f"http://127.0.0.1:8000/api/v1/works/{self.user_two_work_id}"
        )

        self.assertEqual(res.status_code, 404)

    def test_cannot_delete_work_as_unauthorized_user(self):
        self.client.force_authenticate(user=None)
        res = self.client.delete(
            f"http://127.0.0.1:8000/api/v1/works/{self.user_one_work_id}"
        )

        self.assertEqual(res.status_code, 401)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(work_delete_request_test_folder)
        super(WorkDELETETest, cls).tearDownClass()

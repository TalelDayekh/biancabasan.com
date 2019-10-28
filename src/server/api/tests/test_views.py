import random
import shutil
import tempfile
from contextlib import contextmanager

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

from api.v1.serializers import ImageSerializerVersion1
from PIL import Image as pil_image
from rest_framework.test import APITestCase
from users.models import CustomUser

from works.models import Image, Work

image_get_request_test_folder = tempfile.mkdtemp(
    prefix="image_get_request_test_folder"
)
image_post_request_test_folder = tempfile.mkdtemp(
    prefix="image_post_request_test_folder"
)
image_delete_request_test_folder = tempfile.mkdtemp(
    prefix="image_delete_request_test_folder"
)


def test_data() -> list:
    return [
        {
            "title": "Black Square",
            "year_to": 2019,
            "technique": "Oil on canvas",
            "description": "A painting of a black square.",
        }
    ]


@contextmanager
def create_temporary_test_image(
    image_format: str
) -> tempfile.NamedTemporaryFile:
    try:
        test_image = pil_image.new("RGB", (500, 500))
        temporary_image_file = tempfile.NamedTemporaryFile(
            suffix=f".{image_format}", prefix="black_square"
        )
        test_image.save(temporary_image_file)
        temporary_image_file.seek(0)
        yield temporary_image_file
    finally:
        temporary_image_file.close()


@override_settings(
    BASE_DIR=image_get_request_test_folder,
    MEDIA_URL="/",
    MEDIA_ROOT=image_get_request_test_folder,
)
class ImageGETTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create(username="get_image_user")
        work = Work.objects.create(owner=cls.user, **test_data()[0])
        cls.work_id = work.id
        cls.images_id = []

        # Uploads 5 images to user's work as test data
        for i in range(5):
            with create_temporary_test_image("JPEG") as test_image:
                image = Image.objects.create(
                    work=work,
                    image=SimpleUploadedFile(
                        f"Black Square {i + 1}", test_image.read()
                    ),
                )
                cls.images_id.append(image.id)

    def test_can_get_all_images_for_work(self):
        res = self.client.get(
            f"http://127.0.0.1:8000/api/v1/works/{self.work_id}/images"
        )
        images = Image.objects.filter(
            work__owner__username=self.user, work__id=self.work_id
        )
        serializer = ImageSerializerVersion1(images, many=True)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)

    def test_cannot_get_images_from_invalid_work_id(self):
        res_int = self.client.get(
            "http://127.0.0.1:8000/api/v1/works/9999/images"
        )
        res_str = self.client.get(
            "http://127.0.0.1:8000/api/v1/works/NaN/images"
        )

        self.assertEqual(res_int.status_code, 404)
        self.assertEqual(res_str.status_code, 404)

    def test_can_get_image_for_work(self):
        # Tests with a random image from
        # the test data on each test run.
        image_id = random.choice(self.images_id)
        res = self.client.get(
            f"http://127.0.0.1:8000/api/v1/works/{self.work_id}/images/{image_id}"
        )
        image = Image.objects.get(
            work__owner__username=self.user, work__id=self.work_id, id=image_id
        )
        serializer = ImageSerializerVersion1(image)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)

    def test_cannot_get_image_from_invalid_image_or_work_id(self):
        image_id = random.choice(self.images_id)
        res_invalid_image_id_int = self.client.get(
            f"http://127.0.0.1:8000/api/v1/works/{self.work_id}/images/9999"
        )
        res_invalid_image_id_str = self.client.get(
            f"http://127.0.0.1:8000/api/v1/works/{self.work_id}/images/NaN"
        )
        res_invalid_work_id_int = self.client.get(
            f"http://127.0.0.1:8000/api/v1/works/9999/images/{image_id}"
        )
        res_invalid_work_id_str = self.client.get(
            f"http://127.0.0.1:8000/api/v1/works/NaN/images/{image_id}"
        )

        self.assertEqual(res_invalid_image_id_int.status_code, 404)
        self.assertEqual(res_invalid_image_id_str.status_code, 404)
        self.assertEqual(res_invalid_work_id_int.status_code, 404)
        self.assertEqual(res_invalid_work_id_str.status_code, 404)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(image_get_request_test_folder)


@override_settings(
    BASE_DIR=image_post_request_test_folder,
    MEDIA_URL="/",
    MEDIA_ROOT=image_post_request_test_folder,
)
class ImagePOSTTest(APITestCase):
    def setUp(self):
        user_one = CustomUser.objects.create(username="post_image_user_one")
        self.work = Work.objects.create(owner=user_one, **test_data()[0])
        self.client.force_authenticate(user_one)

    def test_can_post_valid_image_to_work_by_user(self):
        with create_temporary_test_image("JPEG") as test_image:
            res = self.client.post(
                f"http://127.0.0.1:8000/api/v1/works/{self.work.id}/images",
                {"image": test_image},
                format="multipart",
            )

            self.assertEqual(res.status_code, 201)

    def test_cannot_post_invalid_image_to_work_by_user(self):
        with create_temporary_test_image("PNG") as test_image:
            res = self.client.post(
                f"http://127.0.0.1:8000/api/v1/works/{self.work.id}/images",
                {"image": test_image},
                format="multipart",
            )

            self.assertEqual(res.status_code, 400)

    def test_cannot_post_valid_image_to_work_by_other_user(self):
        user_two = CustomUser.objects.create(username="post_image_user_two")
        work = Work.objects.create(owner=user_two, **test_data()[0])

        with create_temporary_test_image("JPEG") as test_image:
            res = self.client.post(
                f"http://127.0.0.1:8000/api/v1/works/{work.id}/images",
                {"image": test_image},
                format="multipart",
            )

            self.assertEqual(res.status_code, 400)

    def test_cannot_post_valid_image_to_work_as_unauthorized_user(self):
        self.client.force_authenticate(user=None)

        with create_temporary_test_image("JPEG") as test_image:
            res = self.client.post(
                f"http://127.0.0.1:8000/api/v1/works/{self.work.id}/images",
                {"image": test_image},
                format="multipart",
            )

            self.assertEqual(res.status_code, 401)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(image_post_request_test_folder)


@override_settings(
    BASE_DIR=image_delete_request_test_folder,
    MEDIA_URL="/",
    MEDIA_ROOT=image_delete_request_test_folder,
)
class ImageDELETETest(APITestCase):
    def setUp(self):
        self.user_one = CustomUser.objects.create(
            username="delete_image_user_one"
        )
        self.user_two = CustomUser.objects.create(
            username="delete_image_user_two"
        )
        user_one_work = Work.objects.create(
            owner=self.user_one, **test_data()[0]
        )
        user_two_work = Work.objects.create(
            owner=self.user_two, **test_data()[0]
        )
        self.user_one_work_id = user_one_work.id
        self.user_two_work_id = user_two_work.id
        self.client.force_authenticate(self.user_one)

        with create_temporary_test_image("JPEG") as test_image:
            user_one_image = Image.objects.create(
                work=user_one_work,
                image=SimpleUploadedFile(test_image.name, test_image.read()),
            )
            self.user_one_image_id = user_one_image.id

        with create_temporary_test_image("JPEG") as test_image:
            user_two_image = Image.objects.create(
                work=user_two_work,
                image=SimpleUploadedFile(test_image.name, test_image.read()),
            )
            self.user_two_image_id = user_two_image.id

    def test_can_delete_image_for_work_by_user(self):
        res = self.client.delete(
            f"http://127.0.0.1:8000/api/v1/works/{self.user_one_work_id}/images/{self.user_one_image_id}"
        )

        self.assertEqual(res.status_code, 204)

    def test_cannot_delete_image_for_work_by_other_user(self):
        res = self.client.delete(
            f"http://127.0.0.1:8000/api/v1/works/{self.user_two_work_id}/images/{self.user_two_image_id}"
        )

        self.assertEqual(res.status_code, 404)

    def test_cannot_delete_image_for_work_as_unauthorized_user(self):
        self.client.force_authenticate(user=None)
        res = self.client.delete(
            f"http://127.0.0.1:8000/api/v1/works/{self.user_one_work_id}/images/{self.user_one_image_id}"
        )

        self.assertEqual(res.status_code, 401)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(image_delete_request_test_folder)


# from api.v1.serializers import WorkSerializerVersion1
# from rest_framework.test import APITestCase
# from users.models import CustomUser

# from works.models import Work


# def test_data():
#     return [
#         {
#             "title": "Exotic Landscape",
#             "year_to": 1908,
#             "technique": "Oil on canvas",
#             "description": "Monkeys picking up oranges in a jungle painted with rich greens in the leaves, grass and trees.",
#         },
#         {
#             "title": "Fight Between a Tiger and a Buffalo",
#             "year_to": 1908,
#             "technique": "Oil on canvas",
#             "description": "A imaginary scene of a tiger attacking a buffalo in a fantastic jungle environment.",
#         },
#         {
#             "title": "The Dream",
#             "year_to": 1910,
#             "technique": "Oil on canvas",
#             "description": "A surreal scene of Rousseau's mistress on a divan, gazing over a landscape of flowers and animals.",
#         },
#         {
#             "title": "Teenage Wildlife",
#             "year_to": 2003,
#             "technique": "Oil on canvas",
#             "description": "Life, colour, motion and erotic power pervades this abstract expressionist work.",
#         },
#         {"title": "", "year_to": "", "technique": "", "description": ""},
#     ]


# class WorksGETTest(APITestCase):
#     def setUp(self):
#         self.user = CustomUser.objects.create(username="rousseau")
#         self.client.force_authenticate(self.user)
#         Work.objects.bulk_create(
#             [
#                 Work(owner=self.user, **test_data()[0]),
#                 Work(owner=self.user, **test_data()[1]),
#                 Work(owner=self.user, **test_data()[2]),
#             ]
#         )

#     def test_can_get_all_works_for_user(self):
#         res = self.client.get("http://127.0.0.1:8000/api/v1/works/")
#         works = Work.objects.filter(owner__username=self.user)
#         serializer = WorkSerializerVersion1(works, many=True)

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res.data, serializer.data)

#     def test_cannot_get_works_for_unauthorized_user(self):
#         self.client.force_authenticate(user=None)
#         res = self.client.get("http://127.0.0.1:8000/api/v1/works/")

#         self.assertEqual(res.status_code, 401)

#     def test_can_get_all_works_from_year_to_for_user(self):
#         res = self.client.get(
#             "http://127.0.0.1:8000/api/v1/works/", {"year_to": 1908}
#         )
#         works = Work.objects.filter(owner__username=self.user, year_to=1908)
#         serializer = WorkSerializerVersion1(works, many=True)

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res.data, serializer.data)

#     def test_cannot_get_works_from_non_existing_year_to(self):
#         res = self.client.get(
#             "http://127.0.0.1:8000/api/v1/works/", {"year_to": "not a year"}
#         )

#         self.assertEqual(res.status_code, 400)

#     def test_can_get_sorted_list_of_year_to_for_user(self):
#         res = self.client.get(
#             f"http://127.0.0.1:8000/api/v1/{self.user}/works/years/"
#         )

#         self.assertEqual(res.data, [1910, 1908])

#     def test_can_get_single_work_for_user(self):
#         # Get id from work title instead of hardcoding it in the request
#         # in case the database provides different id values on testruns.
#         work = Work.objects.get(owner__username=self.user, title="The Dream")
#         work_id = work.id
#         res = self.client.get(f"http://127.0.0.1:8000/api/v1/works/{work_id}/")
#         serializer = WorkSerializerVersion1(work)

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res.data, serializer.data)

#     def test_cannot_get_work_from_invalid_id(self):
#         res_int = self.client.get("http://127.0.0.1:8000/api/v1/works/9999/")
#         res_str = self.client.get("http://127.0.0.1:8000/api/v1/works/NaN/")

#         self.assertEqual(res_int.status_code, 404)
#         self.assertEqual(res_str.status_code, 404)


# class WorksPOSTTest(APITestCase):
#     def setUp(self):
#         user = CustomUser.objects.create(username="cecilybrown")
#         self.client.force_authenticate(user)

#     def test_can_create_work_for_user(self):
#         res = self.client.post(
#             "http://127.0.0.1:8000/api/v1/works/", test_data()[3]
#         )

#         self.assertEqual(res.status_code, 201)

#     def test_cannot_create_work_for_unauthorized_user(self):
#         self.client.force_authenticate(user=None)
#         res = self.client.post(
#             "http://127.0.0.1:8000/api/v1/works/", test_data()[3]
#         )

#         self.assertEqual(res.status_code, 401)

#     def test_cannot_create_work_from_invalid_payload(self):
#         res = self.client.post(
#             "http://127.0.0.1:8000/api/v1/works/", test_data()[4]
#         )

#         self.assertEqual(res.status_code, 400)

#     def test_cannot_create_work_from_non_selectable_year(self):
#         valid_payload = test_data()[3]
#         valid_payload["year_to"] = 1986
#         res = self.client.post(
#             "http://127.0.0.1:8000/api/v1/works/", valid_payload
#         )

#         self.assertEqual(res.status_code, 400)


# class WorksPATCHTest(APITestCase):
#     def setUp(self):
#         self.user = CustomUser.objects.create(username="cecilybrown")
#         self.client.force_authenticate(self.user)
#         work = Work.objects.create(owner=self.user, **test_data()[3])
#         self.work_id = work.id
#         self.updated_payload = {"year_from": 2003, "height": 203, "width": 229}

#     def test_can_update_work_for_user(self):
#         res = self.client.patch(
#             f"http://127.0.0.1:8000/api/v1/works/{self.work_id}/",
#             self.updated_payload,
#         )

#         self.assertEqual(res.status_code, 200)
#         self.assertTrue(res.data["year_from"])
#         self.assertTrue(res.data["height"])
#         self.assertTrue(res.data["width"])

#     def test_cannot_update_work_for_unauthorized_user(self):
#         self.client.force_authenticate(user=None)
#         res = self.client.patch(
#             f"http://127.0.0.1:8000/api/v1/works/{self.work_id}/",
#             self.updated_payload,
#         )

#         self.assertEqual(res.status_code, 401)

#     def test_cannot_update_work_from_invalid_id(self):
#         res_int = self.client.patch(
#             "http://127.0.0.1:8000/api/v1/works/9999/", self.updated_payload
#         )
#         res_str = self.client.patch(
#             "http://127.0.0.1:8000/api/v1/works/NaN/", self.updated_payload
#         )

#         self.assertEqual(res_int.status_code, 404)
#         self.assertEqual(res_str.status_code, 404)


# class WorksDELETETest(APITestCase):
#     def setUp(self):
#         user = CustomUser.objects.create(username="rousseau")
#         self.client.force_authenticate(user)
#         Work.objects.bulk_create(
#             [
#                 Work(owner=user, **test_data()[0]),
#                 Work(owner=user, **test_data()[1]),
#                 Work(owner=user, **test_data()[2]),
#             ]
#         )
#         work_to_delete = Work.objects.get(
#             owner__username=user, title="The Dream"
#         )
#         self.work_to_delete_id = work_to_delete.id

#     def test_can_delete_work_for_user(self):
#         res_delete = self.client.delete(
#             f"http://127.0.0.1:8000/api/v1/works/{self.work_to_delete_id}/"
#         )
#         res_get = self.client.get(
#             f"http://127.0.0.1:8000/api/v1/works/{self.work_to_delete_id}/"
#         )

#         self.assertEqual(res_delete.status_code, 204)
#         self.assertEqual(res_get.status_code, 404)

#     def test_cannot_delete_work_for_unauthorized_user(self):
#         self.client.force_authenticate(user=None)
#         res = self.client.delete(
#             f"http://127.0.0.1:8000/api/v1/works/{self.work_to_delete_id}/"
#         )

#         self.assertEqual(res.status_code, 401)

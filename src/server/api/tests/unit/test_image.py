import random
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

from api.tests.unit.utils import create_temporary_test_image, work_test_data
from api.v1.serializers import ImageSerializer
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


@override_settings(
    BASE_DIR=image_get_request_test_folder,
    MEDIA_URL="/",
    MEDIA_ROOT=image_get_request_test_folder,
)
class ImageGETTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = CustomUser.objects.create_user(
            username="get_image_testuser"
        )
        cls.work = Work.objects.create(owner=cls.user, **work_test_data()[0])
        cls.images_id = []

        for i in range(5):
            with create_temporary_test_image("JPEG") as test_image:
                image = Image.objects.create(
                    work=cls.work,
                    image=SimpleUploadedFile(
                        f"Black Square {i + 1}.JPEG", test_image.read()
                    ),
                )
                cls.images_id.append(image.id)
        super(ImageGETTest, cls).setUpClass()

    def test_can_get_all_images_for_work(self):
        res = self.client.get(
            f"http://127.0.0.1:8000/api/v1/works/{self.work.id}/images"
        )
        images = Image.objects.filter(
            work__owner__username=self.user, work__id=self.work.id
        )
        serializer = ImageSerializer(images, many=True)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)

    def test_cannot_get_all_images_from_invalid_work_id(self):
        res_invalid_id_int = self.client.get(
            "http://127.0.0.1:8000/api/v1/works/999/images"
        )
        res_invalid_id_str = self.client.get(
            "http://127.0.0.1:8000/api/v1/works/Nan/images"
        )

        self.assertEqual(res_invalid_id_int.status_code, 404)
        self.assertEqual(res_invalid_id_str.status_code, 404)

    def test_can_get_image_for_work(self):
        # Tests with a random image from
        # the test data on each test run.
        image_id = random.choice(self.images_id)
        res = self.client.get(
            f"http://127.0.0.1:8000/api/v1/works/{self.work.id}/images/{image_id}"
        )
        image = Image.objects.get(
            work__owner__username=self.user, work__id=self.work.id, id=image_id
        )
        serializer = ImageSerializer(image)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, serializer.data)

    def test_cannot_get_image_from_invalid_image_id(self):
        res_invalid_id_int = self.client.get(
            f"http://127.0.0.1:8000/api/v1/works/{self.work.id}/images/999"
        )
        res_invalid_id_str = self.client.get(
            f"http://127.0.0.1:8000/api/v1/works/{self.work.id}/images/NaN"
        )

        self.assertEqual(res_invalid_id_int.status_code, 404)
        self.assertEqual(res_invalid_id_str.status_code, 404)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(image_get_request_test_folder)
        super(ImageGETTest, cls).tearDownClass()


@override_settings(
    BASE_DIR=image_post_request_test_folder,
    MEDIA_URL="/",
    MEDIA_ROOT=image_post_request_test_folder,
)
class ImagePOSTTest(APITestCase):
    def setUp(self):
        user_one = CustomUser.objects.create_user(
            username="post_image_testuser_one"
        )
        self.work = Work.objects.create(owner=user_one, **work_test_data()[0])
        self.client.force_authenticate(user_one)

    def test_can_post_image_to_work_by_user(self):
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

    def test_cannot_post_image_to_work_by_other_user(self):
        user_two = CustomUser.objects.create_user(
            username="post_image_testuser_two"
        )
        work = Work.objects.create(owner=user_two, **work_test_data()[0])

        with create_temporary_test_image("JPEG") as test_image:
            res = self.client.post(
                f"http://127.0.0.1:8000/api/v1/works/{work.id}/images",
                {"image": test_image},
                format="multipart",
            )

            self.assertEqual(res.status_code, 400)

    def test_cannot_post_image_to_work_as_unauthorized_user(self):
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
        super(ImagePOSTTest, cls).tearDownClass()


@override_settings(
    BASE_DIR=image_delete_request_test_folder,
    MEDIA_URL="/",
    MEDIA_ROOT=image_delete_request_test_folder,
)
class ImageDELETETest(APITestCase):
    def setUp(self):
        pass

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(image_delete_request_test_folder)
        super(ImageDELETETest, cls).tearDownClass()

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

    def test_cannot_get_image_from_invalid_work_id(self):
        res_invalid_id_int = self.client.get(
            "http://127.0.0.1:8000/api/v1/works/999/images"
        )
        res_invalid_id_str = self.client.get(
            "http://127.0.0.1:8000/api/v1/works/Nan/images"
        )

        self.assertEqual(res_invalid_id_int.status_code, 404)
        self.assertEqual(res_invalid_id_str.status_code, 404)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(image_get_request_test_folder)
        super(ImageGETTest, cls).tearDownClass()

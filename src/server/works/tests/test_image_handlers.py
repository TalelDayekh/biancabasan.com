import shutil
import tempfile
from pathlib import Path

from django.test import TestCase, override_settings

from PIL import Image

from ..image_handlers import ImagePathHandler

image_path_handler_temp_media_directory = tempfile.mkdtemp(
    prefix="image_path_handler_test_directory"
)


@override_settings(MEDIA_ROOT=image_path_handler_temp_media_directory)
class ImagePathHandlerTest(TestCase):
    def setUp(self):
        self.image_file = Path(
            image_path_handler_temp_media_directory
        ).joinpath("black_square.jpg")
        test_image = Image.new("RGB", (500, 500))
        test_image.save(self.image_file)

    def test_can_format_work_title(self):
        work_title_directory_name = ImagePathHandler(
            "", "#sTAÄrry niGHT 1!8.,8?9;  "
        ).work_title_directory_name

        self.assertEqual(work_title_directory_name, "starry_night_1889__")

    def test_can_create_directory_from_work_title(self):
        image_path_handler_instance = ImagePathHandler("", "starry_night")
        image_path_handler_instance._create_directory_from_work_title()

        self.assertTrue(
            Path(
                image_path_handler_instance.work_title_directory_path
            ).exists()
        )

    def test_can_move_image_to_work_title_directory(self):
        ImagePathHandler(
            self.image_file, "blÄAck SQuaRE"
        ).move_image_to_work_title_directory()

        self.assertTrue(
            Path(image_path_handler_temp_media_directory)
            .joinpath("black_square/black_square.jpg")
            .exists()
        )
        self.assertFalse(self.image_file.exists())

    def test_can_not_move_image_to_non_existing_work_title_directory(self):
        ImagePathHandler(
            self.image_file, ""
        ).move_image_to_work_title_directory()

        self.assertTrue(self.image_file.exists())

    def test_can_delete_image(self):
        ImagePathHandler(self.image_file, "").delete_image()

        self.assertFalse(self.image_file.exists())

    def test_can_not_delete_image(self):
        image_file = Path("/path/to/non/existing/image")
        ImagePathHandler(image_file, "").delete_image()

        self.assertFalse(image_file.exists())

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(image_path_handler_temp_media_directory)

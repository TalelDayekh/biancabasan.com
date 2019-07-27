import shutil
import tempfile
from pathlib import Path

from django.test import TestCase, override_settings

from PIL import Image

from ..image_handlers import ImagePathHandler


class ImagePathHandlerTest(TestCase):
    def setUp(self):
        self.temp_media_directory = tempfile.mkdtemp(
            prefix="image_path_handler_test_directory"
        )

    def test_can_format_work_title(self):
        work_title_directory_name = ImagePathHandler(
            "", "#sTAÄrry niGHT 1!8.,8?9;  "
        ).work_title_directory_name

        self.assertEqual(work_title_directory_name, "starry_night_1889__")

    def test_can_create_directory_from_work_title(self):
        with override_settings(MEDIA_ROOT=self.temp_media_directory):
            image_path_handler_instance = ImagePathHandler("", "starry_night")
            image_path_handler_instance._create_directory_from_work_title()

            self.assertTrue(
                Path(
                    image_path_handler_instance.work_title_directory_path
                ).exists()
            )

    def test_can_move_image_to_work_title_directory(self):
        image_file = Path(self.temp_media_directory).joinpath(
            "black_square.jpg"
        )
        test_image = Image.new("RGB", (500, 500))
        test_image.save(image_file)

        with override_settings(MEDIA_ROOT=self.temp_media_directory):
            ImagePathHandler(
                image_file, "blÄAck SQuaRE"
            ).move_image_to_work_title_directory()

        self.assertTrue(
            Path(self.temp_media_directory)
            .joinpath("black_square/black_square.jpg")
            .exists()
        )
        self.assertFalse(image_file.exists())

    def tearDown(self):
        shutil.rmtree(self.temp_media_directory)

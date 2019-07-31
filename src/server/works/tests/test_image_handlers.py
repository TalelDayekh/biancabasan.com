import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.test import TestCase, override_settings

from PIL import Image

from ..image_handlers import ImageHandler

image_handler_temp_media_directory = tempfile.mkdtemp(
    prefix="image_path_handler_test_directory"
)


@override_settings(MEDIA_ROOT=image_handler_temp_media_directory)
class ImageHandlerTest(TestCase):
    def setUp(self):
        self.image_file = Path(image_handler_temp_media_directory).joinpath(
            "black_square.jpg"
        )
        test_image = Image.new("RGB", (500, 500))
        test_image.save(self.image_file)
        self.non_existing_image_file = Path("/path/to/non/existing/image")
        self.image_handler_inst = ImageHandler(
            self.image_file, "#bLAÄck SQuaRe, 20!.19;  "
        )

    def test_can_get_image_file_size(self):
        image_file_size = self.image_handler_inst.image_file_size
        self.assertEqual(image_file_size, 5)

    def test_can_not_get_image_file_size(self):
        image_file_size = ImageHandler(
            self.non_existing_image_file, ""
        ).image_file_size
        self.assertEqual(image_file_size, None)

    def test_can_format_work_title(self):
        self.image_handler_inst._format_work_title()
        self.assertEqual(
            self.image_handler_inst.work_title_directory_name,
            "black_square_2019__",
        )

    def test_can_create_directory_from_work_title(self):
        self.image_handler_inst._format_work_title()
        self.image_handler_inst._create_directory_from_work_title()
        self.assertTrue(
            Path(self.image_handler_inst.work_title_directory_path).exists()
        )

    def test_can_move_image_to_work_title_directory(self):
        self.image_handler_inst.move_image_to_work_title_directory()
        self.assertTrue(
            Path(image_handler_temp_media_directory)
            .joinpath("black_square_2019__/black_square.jpg")
            .exists()
        )
        self.assertFalse(self.image_file.exists())

    def test_can_not_move_image_to_non_existing_work_title_directory(self):
        ImageHandler(self.image_file).move_image_to_work_title_directory()
        self.assertTrue(self.image_file.exists())

    def test_can_delete_image(self):
        self.image_handler_inst.delete_image()
        self.assertFalse(self.image_file.exists())

    def test_can_not_delete_image(self):
        ImageHandler(self.non_existing_image_file).delete_image()
        self.assertFalse(self.non_existing_image_file.exists())

    def test_can_create_web_images_set_with_correct_sizes(self):
        web_image_set = ImageHandler.create_web_images_set(self.image_file)
        web_images = [
            Image.open(web_image.image_file) for web_image in web_image_set
        ]
        self.assertEqual(web_images[0].size, (1250, 1250))
        self.assertEqual(web_images[1].size, (2500, 2500))

    def test_can_not_create_web_images_set_from_non_existing_image(self):
        web_image_set = ImageHandler.create_web_images_set(
            self.non_existing_image_file
        )
        self.assertEqual(web_image_set, None)

    def test_can_create_unique_image_file_name(self):
        pass

    @classmethod
    def tearDownClass(cls):
        import time

        time.sleep(10)
        shutil.rmtree(image_handler_temp_media_directory)

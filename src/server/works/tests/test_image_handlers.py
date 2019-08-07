import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.test import TestCase, override_settings

from PIL import Image

from ..image_handlers import ImageDirectoryHandler, ImageFileHandler

image_directory_handler_test_folder = tempfile.mkdtemp(
    prefix="image_directory_handler_test_folder"
)
image_file_handler_test_folder = tempfile.mkdtemp(
    prefix="image_file_handler_test_folder"
)


@override_settings(MEDIA_ROOT=image_directory_handler_test_folder)
class ImageDirectoryHandlerTest(TestCase):
    def test_can_format_work_title(self):
        image_directory_handler_inst_one = ImageDirectoryHandler(
            "#bLAÄck SQuaRe, 20!.19;  "
        )
        image_directory_handler_inst_two = ImageDirectoryHandler(123)
        self.assertEqual(
            image_directory_handler_inst_one.formatted_work_title,
            "black_square_2019__",
        )
        self.assertEqual(
            image_directory_handler_inst_two.formatted_work_title, "123"
        )

    def test_can_create_directory_from_formatted_work_title(self):
        image_directory = ImageDirectoryHandler("White Square")
        image_directory.create_directory_from_formatted_work_title()
        self.assertTrue(image_directory.image_directory_path.exists())

    def test_can_not_create_directory_from_non_existing_work_title(self):
        image_directory = ImageDirectoryHandler("")
        image_directory.create_directory_from_formatted_work_title()
        self.assertEqual(
            image_directory.image_directory_path,
            Path(image_directory_handler_test_folder),
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(image_directory_handler_test_folder)


@override_settings(MEDIA_ROOT=image_file_handler_test_folder)
class ImageFileHandlerTest(TestCase):
    def setUp(self):
        self.image_file = Path(image_file_handler_test_folder).joinpath(
            "black_square.jpg"
        )
        test_image = Image.new("RGB", (500, 500))
        test_image.save(self.image_file)
        self.non_existing_image_file = Path("/path/to/non/existing/image")

    def test_can_get_image_file_type(self):
        image_file_type = ImageFileHandler(self.image_file).image_file_type
        self.assertEqual(image_file_type, "JPEG")

    def test_can_not_get_image_file_type_from_non_existing_image(self):
        with self.assertRaises(FileNotFoundError):
            ImageFileHandler(self.non_existing_image_file).image_file_type

    def test_can_not_get_image_file_type_from_non_image_file(self):
        with tempfile.NamedTemporaryFile(
            suffix=".pdf", dir=image_file_handler_test_folder
        ) as pdf_file:
            with self.assertRaises(OSError):
                ImageFileHandler(Path(pdf_file.name)).image_file_type

    def test_can_get_floor_image_file_size(self):
        image_file_size = ImageFileHandler(
            self.image_file
        ).floor_image_file_size
        self.assertEqual(image_file_size, 4)

    def test_can_not_get_floor_image_file_size_from_non_existing_image(self):
        with self.assertRaises(FileNotFoundError):
            ImageFileHandler(
                self.non_existing_image_file
            ).floor_image_file_size

    def test_can_move_image_to_work_title_directory(self):
        image_directory = ImageDirectoryHandler("Black Square")
        image_directory.create_directory_from_formatted_work_title()
        image_directory_path = image_directory.image_directory_path

        image_file_handler_inst = ImageFileHandler(
            self.image_file, image_directory_path
        )
        image_file_handler_inst.move_image_to_work_title_directory()
        self.assertTrue(
            image_directory_path.joinpath(self.image_file.name).exists()
        )
        self.assertFalse(self.image_file.exists())

    def test_can_not_move_image_to_non_existing_work_title_directory(self):
        non_existing_work_title_directory = Path(
            "path/to/non/existing/directory"
        )

        ImageFileHandler(
            self.image_file, non_existing_work_title_directory
        ).move_image_to_work_title_directory()
        self.assertTrue(self.image_file.exists())

    def test_can_delete_image(self):
        image_file_handler_inst = ImageFileHandler(self.image_file)
        image_file_handler_inst.delete_image()
        self.assertFalse(self.image_file.exists())

    def test_can_not_delete_image(self):
        image_file_handler_inst = ImageFileHandler(
            self.non_existing_image_file
        )
        image_file_handler_inst.delete_image()
        self.assertFalse(self.non_existing_image_file.exists())

    def test_can_create_web_images_set_with_correct_sizes(self):
        web_images_set = ImageFileHandler.create_web_images_set(
            self.image_file
        )
        web_images = [
            Image.open(web_image.image_file) for web_image in web_images_set
        ]
        self.assertEqual(web_images[0].size, (1250, 1250))
        self.assertEqual(web_images[1].size, (2500, 2500))

    def test_can_not_create_web_images_set_from_non_existing_image(self):
        pass

    @classmethod
    def tearDownClass(self):
        shutil.rmtree(image_file_handler_test_folder)

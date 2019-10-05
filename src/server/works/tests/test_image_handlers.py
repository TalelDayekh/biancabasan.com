import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase, override_settings

from PIL import Image

from ..image_handlers import (ImageDirectoryHandler, ImageFileHandler,
                              ImageValidationHandler)

image_directory_handler_test_folder = tempfile.mkdtemp(
    prefix="image_directory_handler_test_folder"
)
image_file_handler_test_folder = tempfile.mkdtemp(
    prefix="image_file_handler_test_folder"
)


@override_settings(MEDIA_ROOT=image_directory_handler_test_folder)
class ImageDirectoryHandlerTest(TestCase):
    def setUp(self):
        self.image_directory_handler = ImageDirectoryHandler(
            "#bLAÄck SQuaRe, 20!.19;  "
        )

    def test_can_format_work_title(self):
        formatted_work_title_one = (
            self.image_directory_handler.formatted_work_title
        )
        formatted_work_title_two = ImageDirectoryHandler(
            123
        ).formatted_work_title

        self.assertEqual(formatted_work_title_one, "black_square_2019__")
        self.assertEqual(formatted_work_title_two, "123")

    def test_can_create_directory_from_formatted_work_title(self):
        self.image_directory_handler.create_directory_from_formatted_work_title()

        self.assertTrue(
            self.image_directory_handler.image_directory_path.exists()
        )

    def test_cannot_create_directory_from_non_existing_work_title(self):
        image_directory = ImageDirectoryHandler("")
        image_directory.create_directory_from_formatted_work_title()

        self.assertEqual(
            image_directory.image_directory_path,
            Path(image_directory_handler_test_folder),
        )

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(image_directory_handler_test_folder)


class ImageValidationHandlerTest(TestCase):
    @contextmanager
    def create_temporary_in_memory_image_file(
        self, image_format: str, image_size: int
    ) -> None:
        try:
            test_image = Image.new("RGB", (500, 500))
            temporary_image_file = tempfile.NamedTemporaryFile(
                prefix="black_square"
            )
            test_image.save(temporary_image_file, image_format)
            temporary_image_file.seek(0)

            in_memory_image_file = InMemoryUploadedFile(
                file=temporary_image_file,
                field_name="image",
                name=f"black_square.{image_format}",
                content_type=f"image/{image_format}",
                size=image_size,
                charset=None,
            )
            yield in_memory_image_file
        finally:
            temporary_image_file.close()

    def test_can_validate_image_format_as_true_or_false(self):
        with self.create_temporary_in_memory_image_file(
            "JPEG", 2097152
        ) as temporary_in_memory_image:
            valid_image_format = ImageValidationHandler(
                temporary_in_memory_image
            )._validate_image_format()

            self.assertEqual(valid_image_format, True)

        with self.create_temporary_in_memory_image_file(
            "PNG", 2097152
        ) as temporary_in_memory_image:
            valid_image_format = ImageValidationHandler(
                temporary_in_memory_image
            )._validate_image_format()

            self.assertEqual(valid_image_format, False)

    def test_can_validate_image_size_as_true_or_false(self):
        with self.create_temporary_in_memory_image_file(
            "JPEG", 2097152
        ) as temporary_in_memory_image:
            valid_image_size = ImageValidationHandler(
                temporary_in_memory_image
            )._validate_image_size()

            self.assertEqual(valid_image_size, True)

        with self.create_temporary_in_memory_image_file(
            "JPEG", 2097153
        ) as temporary_in_memory_image:
            valid_image_size = ImageValidationHandler(
                temporary_in_memory_image
            )._validate_image_size()

            self.assertEqual(valid_image_size, False)

    def test_can_validate_image_as_true_or_false(self):
        with self.create_temporary_in_memory_image_file(
            "JPEG", 2097152
        ) as temporary_in_memory_image:
            valid_image = ImageValidationHandler(
                temporary_in_memory_image
            ).is_valid()

            self.assertEqual(valid_image, True)

        with self.create_temporary_in_memory_image_file(
            "PNG", 2097152
        ) as temporary_in_memory_image:
            valid_image = ImageValidationHandler(
                temporary_in_memory_image
            ).is_valid()

            self.assertEqual(valid_image, False)

        with self.create_temporary_in_memory_image_file(
            "JPEG", 2097153
        ) as temporary_in_memory_image:
            valid_image = ImageValidationHandler(
                temporary_in_memory_image
            ).is_valid()

            self.assertEqual(valid_image, False)


@override_settings(MEDIA_ROOT=image_file_handler_test_folder)
class ImageFileHandlerTest(TestCase):
    def setUp(self):
        self.image_file = Path(image_file_handler_test_folder).joinpath(
            "black_square.jpg"
        )
        test_image = Image.new("RGB", (500, 500))
        test_image.save(self.image_file)
        self.non_existing_image_file = Path("/path/to/non/existing/image")
        self.image_file_handler_valid_image = ImageFileHandler(self.image_file)
        self.image_file_handler_invalid_image = ImageFileHandler(
            self.non_existing_image_file
        )

    def test_can_get_image_file_type(self):
        image_file_type = self.image_file_handler_valid_image.image_file_type

        self.assertEqual(image_file_type, "JPEG")

    def test_cannot_get_image_file_type_from_non_existing_image(self):
        with self.assertRaises(FileNotFoundError):
            self.image_file_handler_invalid_image.image_file_type

    def test_cannot_get_image_file_type_from_non_image_file(self):
        with tempfile.NamedTemporaryFile(
            suffix=".pdf", dir=image_file_handler_test_folder
        ) as pdf_file:
            with self.assertRaises(OSError):
                ImageFileHandler(Path(pdf_file.name)).image_file_type

    def test_can_get_floor_image_file_size(self):
        image_file_size = (
            self.image_file_handler_valid_image.floor_image_file_size
        )

        self.assertEqual(image_file_size, 4)

    def test_cannot_get_floor_image_file_size_from_non_existing_image(self):
        with self.assertRaises(FileNotFoundError):
            self.image_file_handler_invalid_image.floor_image_file_size

    def test_can_move_image_to_work_title_directory(self):
        image_directory_handler = ImageDirectoryHandler("Black Square")
        image_directory_handler.create_directory_from_formatted_work_title()
        image_directory_path = image_directory_handler.image_directory_path

        image_file_handler = ImageFileHandler(
            self.image_file, image_directory_path
        )
        image_file_handler.move_image_to_work_title_directory()

        self.assertTrue(
            image_directory_path.joinpath(self.image_file.name).exists()
        )
        self.assertFalse(self.image_file.exists())

    def test_cannot_move_image_to_non_existing_work_title_directory(self):
        non_existing_work_title_directory = Path(
            "path/to/non/existing/directory"
        )

        ImageFileHandler(
            self.image_file, non_existing_work_title_directory
        ).move_image_to_work_title_directory()

        self.assertTrue(self.image_file.exists())

    def test_can_delete_image(self):
        self.image_file_handler_valid_image.delete_image()

        self.assertFalse(self.image_file.exists())

    def test_cannot_delete_image(self):
        self.image_file_handler_invalid_image.delete_image()

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

    def test_cannot_create_web_images_set_from_non_existing_image(self):
        web_images_set = ImageFileHandler.create_web_images_set(
            self.non_existing_image_file
        )

        self.assertEqual(web_images_set, None)

    @classmethod
    def tearDownClass(self):
        shutil.rmtree(image_file_handler_test_folder)

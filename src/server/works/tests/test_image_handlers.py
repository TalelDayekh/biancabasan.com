import shutil
import tempfile
from contextlib import contextmanager
from pathlib import Path

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase

from PIL import Image

from ..image_handlers import (
    ImageFileHandler,
    ImageValidationHandler,
    format_work_title,
)

image_file_handler_test_folder = tempfile.mkdtemp(
    prefix="image_file_handler_test_folder"
)


class FormatWorkTitleTest(TestCase):
    def test_can_format_work_title_str(self):
        work_title = "#bLAÄck SQuaRe, 20!.19;  "
        formatted_work_title = format_work_title(work_title)

        self.assertEqual(formatted_work_title, "black_square_2019__")

    def test_can_format_work_title_int(self):
        work_title = 123
        formatted_work_title = format_work_title(work_title)

        self.assertEqual(formatted_work_title, "123")


class ImageValidationHandlerTest(TestCase):
    @contextmanager
    def create_temporary_in_memory_image_file(
        self, image_format: str, image_size: int
    ) -> InMemoryUploadedFile:
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

    def image_format_validator(self, image_format: str) -> bool:
        with self.create_temporary_in_memory_image_file(
            image_format, 2097152
        ) as temporary_in_memory_image:
            valid_image_format = ImageValidationHandler(
                temporary_in_memory_image
            )._validate_image_format()
            return valid_image_format

    def image_size_validator(self, image_size: int) -> bool:
        with self.create_temporary_in_memory_image_file(
            "JPEG", image_size
        ) as temporary_in_memory_image:
            valid_image_size = ImageValidationHandler(
                temporary_in_memory_image
            )._validate_image_size()
            return valid_image_size

    def image_validator(self, image_format: str, image_size: int) -> bool:
        with self.create_temporary_in_memory_image_file(
            image_format, image_size
        ) as temporary_in_memory_image:
            valid_image = ImageValidationHandler(
                temporary_in_memory_image
            ).is_valid()
            return valid_image

    def test_can_validate_image_format_as_true_or_false(self):
        valid_image_format = self.image_format_validator("JPEG")
        invalid_image_format = self.image_format_validator("PNG")

        self.assertEqual(valid_image_format, True)
        self.assertEqual(invalid_image_format, False)

    def test_can_validate_image_size_as_true_or_false(self):
        valid_image_size = self.image_size_validator(2097152)
        invalid_image_size = self.image_size_validator(2097153)

        self.assertEqual(valid_image_size, True)
        self.assertEqual(invalid_image_size, False)

    def test_can_validate_image_as_true_or_false(self):
        invalid_image_one = self.image_validator("PNG", 2097152)
        invalid_image_two = self.image_validator("JPEG", 2097153)
        valid_image = self.image_validator("JPEG", 2097152)

        self.assertEqual(invalid_image_one, False)
        self.assertEqual(invalid_image_two, False)
        self.assertEqual(valid_image, True)


class ImageFileHandlerTest(TestCase):
    def setUp(self):
        self.nonexistent_image_file = Path("/path/to/nonexistent/image")
        self.image_file = Path(image_file_handler_test_folder).joinpath(
            "black_square.jpg"
        )
        test_image = Image.new("RGB", (500, 500))
        test_image.save(self.image_file)

        self.web_image_set = ImageFileHandler.create_web_image_set(
            self.image_file
        )

    def test_can_create_web_image_set_with_correct_sizes(self):
        web_images = [
            Image.open(web_image.image_file)
            for web_image in self.web_image_set
        ]

        self.assertEqual(web_images[0].size, (1250, 1250))
        self.assertEqual(web_images[1].size, (2500, 2500))

    def test_cannot_create_web_image_set_from_nonexistent_image(self):
        web_image_set = ImageFileHandler.create_web_image_set(
            self.nonexistent_image_file
        )

        self.assertEqual(web_image_set, None)

    def test_can_delete_image_set(self):
        image_file_1250 = Path(image_file_handler_test_folder).joinpath(
            "black_square_1250.jpg"
        )
        image_file_2500 = Path(image_file_handler_test_folder).joinpath(
            "black_square_2500.jpg"
        )

        ImageFileHandler(self.image_file).delete_image_set()

        self.assertEqual(self.image_file.exists(), False)
        self.assertEqual(image_file_1250.exists(), False)
        self.assertEqual(image_file_2500.exists(), False)

    def test_cannot_delete_nonexistent_image_file(self):
        with self.assertRaises(FileNotFoundError):
            ImageFileHandler(self.nonexistent_image_file).delete_image_set()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(image_file_handler_test_folder)

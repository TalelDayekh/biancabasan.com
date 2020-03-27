import shutil
import tempfile
import uuid
from pathlib import Path
from unittest.mock import Mock, PropertyMock, patch

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase

from PIL import Image
from tests.utils import create_temporary_test_image

from works.image_handlers import (
    ImageFileHandler,
    ImageValidationHandler,
    format_work_title,
    image_upload_handler,
)

image_file_handler_test_folder = tempfile.mkdtemp(
    prefix="image_file_handler_test_folder"
)


class ImageUploadHandlerTest(TestCase):
    @patch("uuid.uuid4")
    def test_outputs_correct_str_for_upload_to(self, mock_uuid):
        mock_image_instance = Mock()
        mock_image_instance.work = "Black Square"
        type(mock_uuid.return_value).hex = PropertyMock(
            return_value="mock_uuid_hex"
        )
        upload_to = image_upload_handler(
            mock_image_instance, "black_square.jpg"
        )

        self.assertEqual(
            upload_to, "images/black_square/black_square_mock_uuid_hex.jpg"
        )


class FormatWorkTitleTest(TestCase):
    def test_outputs_correctly_formatted_work_title_str(self):
        work_title = "#bLAÄck SQuaRe, 20!.19;  "
        formatted_work_title = format_work_title(work_title)

        self.assertEqual(formatted_work_title, "black_square_2019__")

    def test_can_format_work_title_int(self):
        work_title = 123
        formatted_work_title = format_work_title(work_title)

        self.assertEqual(formatted_work_title, "123")


class ImageValidationHandlerTest(TestCase):
    def image_validator(
        self, image_format: str, validator: str, image_file_size: int = 2097152
    ) -> bool:
        with create_temporary_test_image(image_format) as test_image:
            in_memory_image_file = InMemoryUploadedFile(
                file=test_image,
                field_name="image",
                name=Path(test_image.name).name,
                content_type=f"image/{Path(test_image.name).suffix.rsplit('.')[1]}",
                size=image_file_size,
                charset=None,
            )

            return {
                "image_format_validation": ImageValidationHandler(
                    in_memory_image_file
                )._validate_image_format(),
                "image_file_size_validator": ImageValidationHandler(
                    in_memory_image_file
                )._validate_image_size(),
                "image_validation": ImageValidationHandler(
                    in_memory_image_file
                ).is_valid(),
            }[validator]

    def test_cannot_validate_none_image_file(self):
        text_file = tempfile.NamedTemporaryFile(
            suffix=".txt", prefix="document"
        )
        invalid_file_type = ImageValidationHandler(text_file).is_valid()

        self.assertEqual(invalid_file_type, False)

    def test_can_validate_correct_image_format_as_true_or_false(self):
        valid_image_format = self.image_validator(
            "JPEG", "image_format_validation"
        )
        invalid_image_format = self.image_validator(
            "PNG", "image_format_validation"
        )

        self.assertEqual(valid_image_format, True)
        self.assertEqual(invalid_image_format, False)

    def test_can_validate_correct_image_file_size_as_true_or_false(self):
        valid_image_file_size = self.image_validator(
            "JPEG", "image_file_size_validator"
        )
        invalid_image_file_size = self.image_validator(
            "JPEG", "image_file_size_validator", 2097153
        )

        self.assertEqual(valid_image_file_size, True)
        self.assertEqual(invalid_image_file_size, False)

    def test_can_validate_image_as_true_or_false(self):
        invalid_image_one = self.image_validator(
            "PNG", "image_validation", 2097152
        )
        invalid_image_two = self.image_validator(
            "JPEG", "image_validation", 2097153
        )
        valid_image = self.image_validator("JPEG", "image_validation", 2097152)

        self.assertEqual(invalid_image_one, False)
        self.assertEqual(invalid_image_two, False)
        self.assertEqual(valid_image, True)


class ImageFileHandlerTest(TestCase):
    def setUp(self):
        self.none_image_file = Path("/path/to/nonexistent/image")
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

    def test_cannot_create_web_image_set_from_none_image_file(self):
        web_image_set = ImageFileHandler.create_web_image_set(
            self.none_image_file
        )

        self.assertEqual(web_image_set, None)

    def test_can_delete_web_image_set(self):
        image_file_1250 = Path(image_file_handler_test_folder).joinpath(
            "black_square_1250.jpg"
        )
        image_file_2500 = Path(image_file_handler_test_folder).joinpath(
            "black_square_2500.jpg"
        )

        self.assertEqual(self.image_file.exists(), True)
        self.assertEqual(image_file_1250.exists(), True)
        self.assertEqual(image_file_2500.exists(), True)

        ImageFileHandler(self.image_file).delete_image_set()

        self.assertEqual(self.image_file.exists(), False)
        self.assertEqual(image_file_1250.exists(), False)
        self.assertEqual(image_file_2500.exists(), False)

    def test_cannot_delete_none_image_file(self):
        with self.assertRaises(FileNotFoundError):
            ImageFileHandler(self.none_image_file).delete_image_set()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(image_file_handler_test_folder)

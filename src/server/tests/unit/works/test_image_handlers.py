import uuid
from unittest.mock import Mock, PropertyMock, patch

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase

from tests.utils import create_temporary_test_image

from works.image_handlers import (
    ImageValidationHandler,
    format_work_title,
    image_upload_handler,
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
    def image_format_validator(self, image_format: str) -> bool:
        with create_temporary_test_image(image_format) as test_image:
            valid_image_format = ImageValidationHandler(
                test_image
            )._validate_image_format()
            return valid_image_format

    def image_size_validator(self) -> bool:
        pass

    def test_can_validate_correct_image_format_as_true_or_false(self):
        valid_image_format = self.image_format_validator("JPEG")
        invalid_image_format = self.image_format_validator("PNG")

        self.assertEqual(valid_image_format, True)
        self.assertEqual(invalid_image_format, False)

import uuid
from unittest.mock import Mock, PropertyMock, patch

from django.test import TestCase

from works.image_handlers import image_upload_handler


class ImageUploadHandlerTest(TestCase):
    @patch('uuid.uuid4')
    def test_outputs_correct_string_for_upload_to(self, mock_uuid):
        mock_image_instance = Mock()
        mock_image_instance.work = 'Black Square'
        type(mock_uuid.return_value).hex = PropertyMock(return_value='mock_uuid_hex')
        upload_to = image_upload_handler(mock_image_instance, 'black_square.jpg')

        self.assertEqual(upload_to, 'images/black_square/black_square_mock_uuid_hex.jpg')

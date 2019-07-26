import shutil
import tempfile
from pathlib import Path

from django.test import TestCase, override_settings

from ..image_handlers import ImagePathHandler


class ImagePathHandlerTest(TestCase):
    def setUp(self):
        self.temp_media_directory = tempfile.mkdtemp(
            prefix="image_path_handler_test_directory"
        )

    def test_create_directory_from_work_title(self):
        with override_settings(MEDIA_ROOT=self.temp_media_directory):
            work_title_directory = ImagePathHandler(
                "starry_night"
            )._create_directory_from_work_title()

            self.assertTrue(Path(work_title_directory).exists())

    def tearDown(self):
        shutil.rmtree(self.temp_media_directory)

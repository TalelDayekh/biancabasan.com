import tempfile
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from ..models import ArtworkImages


def create_temp_test_img_file(img_name, img_file_format):
    temp_img_file = tempfile.NamedTemporaryFile()
    image = Image.new('RGB', size=(1200, 1200), color=0)
    image.save(temp_img_file, format=f'{img_file_format}')
    temp_img_file.name = f'{img_name}' + '.' + f'{img_file_format}'
    temp_img_file.seek(0)
    return temp_img_file

def create_artwork_img_instance(img_file):
    artwork_image = ArtworkImages.objects.create(
        image=SimpleUploadedFile(
            name=img_file.name,
            content=img_file.read()
        )
    )
    uploaded_image = ArtworkImages.objects.get(id=1).image
    return uploaded_image


@override_settings(
    MEDIA_ROOT=tempfile.TemporaryDirectory(
        prefix='biancabasan_test_files_').name
)
class TestArtworkImagesHandler(TestCase):
    def setUp(self):
        test_img = create_temp_test_img_file('starry_night', 'jpeg')
        self.uploaded_image = create_artwork_img_instance(test_img)
    
    def test_(self):
        pass
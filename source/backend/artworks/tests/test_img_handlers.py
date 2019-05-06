import os
import tempfile
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import(
    SimpleUploadedFile,
    InMemoryUploadedFile
)
from PIL import Image
from ..models import ArtworkDetails, ArtworkImages
from ..img_handlers import ImgPathHandler, ImgManipulationHandler


def create_temp_test_img_file(img_name, img_file_format):
    temp_img_file = tempfile.NamedTemporaryFile()
    img = Image.new('RGB', size=(1200, 950), color=0)
    img.save(temp_img_file, format=f'{img_file_format}')
    temp_img_file.name = f'{img_name}' + '.' + f'{img_file_format}'
    temp_img_file.seek(0)
    return temp_img_file

def create_artwork_test_obj(img_file):
    artwork_details = ArtworkDetails.objects.create(
        title='#sTArry niGHT 1!8.,8?9;  (vInCEnt: vAN GÖogH)'
    )

    artwork_img = ArtworkImages.objects.create(
        artwork_details=artwork_details,
        img=SimpleUploadedFile(
            name=img_file.name,
            content=img_file.read()
        )
    )

    uploaded_artwork = []
    uploaded_artwork.append(artwork_details)
    uploaded_artwork.append(artwork_img)
    return uploaded_artwork


@override_settings(
    # os.path.realpath returns the absolute path,
    # not just the path prefixed with a symlink.
    MEDIA_ROOT=os.path.realpath(tempfile.TemporaryDirectory(
        prefix='biancabasan_test_files').name))
class TestImgPathHandler(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_img = create_temp_test_img_file('starry_night', 'jpeg')
        artwork_test_obj = create_artwork_test_obj(test_img)
        uploaded_artwork_img = artwork_test_obj[1]
        cls.img_path_handler_obj = ImgPathHandler(uploaded_artwork_img)

        print('\nTemp test directories and files are being created at path:\n'
            + uploaded_artwork_img.img.path)
    
    def test_artwork_title_formatting(self):
        formatted_title = self.img_path_handler_obj.artwork_title

        self.assertEqual(formatted_title, 'starry_night_1889__vincent_van_gogh')

    def test_mkdir_from_artwork_title(self):
        new_dir = self.img_path_handler_obj.mkdir_from_artwork_title()
        os.chdir(new_dir)

        self.assertEqual(os.getcwd(), new_dir)

    def test_mv_img_to_new_dir(self):
        # Create an alternative artwork title dir for this test
        # to be independent from the tests that runs before it.
        initial_img_path = os.path.dirname(
            self.img_path_handler_obj.artwork_images_obj.img.path
        )
        os.chdir(initial_img_path)
        os.mkdir('alt_artwork_title_dir')
        new_img_path = os.path.join(initial_img_path, 'alt_artwork_title_dir')

        self.img_path_handler_obj.mv_img_to_new_dir(new_img_path)


class TestImgManipulationsHandler(TestCase):
    @classmethod
    def setUpTestData(cls):
        created_test_img = create_temp_test_img_file('starry_night', 'jpeg')
        test_img = Image.open(created_test_img)
        cls.img_manipulation_handler_obj = ImgManipulationHandler(test_img)

    def test_resize_img_proportionally(self):
        resized_img = (
            self.img_manipulation_handler_obj.resize_img_proportionally(1024)
        )

        self.assertEqual(resized_img.width, 1024)
        self.assertEqual(resized_img.height, 811)

    def test_upload_img_to_memory(self):
        in_memory_uploaded_img = (
            self.img_manipulation_handler_obj.upload_img_to_memory(
                'starry_night',
                'JPEG'
            )
        )
        in_memory_img = type(in_memory_uploaded_img) is InMemoryUploadedFile

        self.assertEqual(in_memory_uploaded_img.name, 'starry_night.JPEG')
        self.assertEqual(in_memory_img, True)
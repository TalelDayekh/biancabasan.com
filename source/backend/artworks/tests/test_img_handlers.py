import os
import tempfile
from django.test import TestCase, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from ..models import ArtworkImages
from ..img_handlers import ImgPathHandler, ImgManipulationsHandler


def create_temp_test_img_file(img_name, img_file_format):
    temp_img_file = tempfile.NamedTemporaryFile()
    img = Image.new('RGB', size=(1200, 950), color=0)
    img.save(temp_img_file, format=f'{img_file_format}')
    temp_img_file.name = f'{img_name}' + '.' + f'{img_file_format}'
    temp_img_file.seek(0)
    return temp_img_file


def create_artwork_img_obj(img_file):
    artwork_image = ArtworkImages.objects.create(
        image=SimpleUploadedFile(
            name=img_file.name,
            content=img_file.read()
        )
    )
    uploaded_img = ArtworkImages.objects.get(id=1).image
    return uploaded_img


@override_settings(
    # os.path.realpath returns the absolute path,
    # not just the path prefixed with a symlink.
    MEDIA_ROOT=os.path.realpath(tempfile.TemporaryDirectory(
        prefix='biancabasan_test_files_').name)
)
class TestImgPathHandler(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_img = create_temp_test_img_file('starry_night', 'jpeg')
        artwork_img_obj = create_artwork_img_obj(test_img)

        cls.img_path_handler_obj = ImgPathHandler(
            artwork_img_obj,
            '#sTArrY niGHT 1!8.,8?9;  (vInCEnt: vAN GÖogH)'
        )
        cls.artwork_title = cls.img_path_handler_obj.artwork_title
        cls.initial_img_path = cls.img_path_handler_obj.initial_img_path
        cls.new_img_path = cls.img_path_handler_obj.new_img_path

        print('\nTemporary test directories and files are being created at path:\n' 
            + artwork_img_obj.path)
    
    def test_artwork_title_formatting(self):
        self.assertEqual(
            self.artwork_title, 
            'starry_night_1889__vincent_van_gogh')

    def test_new_img_path(self):
        self.assertEqual(
            self.new_img_path,
            (self.initial_img_path + '/' + self.artwork_title)
        )
    
    def test_mkdir_from_artwork_title(self):
        new_dir_path = self.img_path_handler_obj.mkdir_from_artwork_title()
        os.chdir(new_dir_path)

        self.assertEqual(os.getcwd(), self.new_img_path)


class TestImgManipulationsHandler(TestCase):
    @classmethod
    def setUpTestData(cls):
        created_test_img = create_temp_test_img_file('starry_night', 'jpeg')
        cls.test_img = Image.open(created_test_img)

    def test_resize_img_proportionally(self):
        resized_img = ImgManipulationsHandler(
            self.test_img,
            1024
        ).resize_img_proportionally()

        self.assertEqual(resized_img.width, 1024)
        self.assertEqual(resized_img.height, 811)
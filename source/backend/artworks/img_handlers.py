import os
import re
import uuid
import shutil
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image


class ImgPathHandler():
    def __init__(self, artwork_images_obj):
        self.artwork_images_obj = artwork_images_obj

        try:
            self.artwork_images_obj.img
        except AttributeError as err:
            print(str(err) + ', ImgPathHandler needs to be passed an instance '
                + 'of the ArtworkImages model')
        else:
            # Remove characters that are not letters or numbers from
            # artwork_title, convert remaining ones to lowercase and
            # replace whitespaces with underscores.
            self.artwork_title = str(
                self.artwork_images_obj.artwork_details.title)
            self.artwork_title = re.sub(
                '[^A-Za-z0-9\s]{1}', '', self.artwork_title).replace(
                ' ', '_').lower()

            self.initial_img_dir = os.path.dirname(
                self.artwork_images_obj.img.path
            )

    def mkdir_from_artwork_title(self):
        os.chdir(self.initial_img_dir)

        new_img_dir = os.path.join(
            self.initial_img_dir, self.artwork_title
        )

        try:
            os.mkdir(self.artwork_title)
        except FileExistsError as err:
            print(str(err)
                + ', a image directory already exists for this artwork')
            return new_img_dir
        else:
            return new_img_dir

    def change_duplicate_img_file_name(self):
        pass

    def mv_img_to_new_dir(self, new_img_dir):
        try:
            if not os.path.isdir(new_img_dir):
                raise Exception
        except Exception:
            print('The directory "' + new_img_dir + '" does not exist, it '
                + 'needs to be created before attempting to move any image')
        else:
            pass


class ImgManipulationHandler():
    def __init__(self, open_img_file):
        self.open_img_file = open_img_file

        try:
            self.open_img_file.verify
        except Exception:
            print('Not a valid image file')

    def resize_img_proportionally(self, new_img_width):
        new_img_width = int(new_img_width)
        img_width, img_height = self.open_img_file.size
        new_img_height = (img_height/img_width) * new_img_width
        resized_img = self.open_img_file.resize(
            (new_img_width, int(round(new_img_height)))
        )
        return resized_img

    def upload_img_to_memory(self, img_file_name, img_file_format):
        allowed_file_formats = ['jpeg', 'jpg', 'png']

        try:
            if img_file_format.lower() not in allowed_file_formats:
                raise Exception
        except Exception:
            print('Image format has to be jpeg, jpg or png')
        else:
            memory_buffer = BytesIO()
            self.open_img_file.save(
                memory_buffer,
                format=img_file_format,
                quality=10
            )

            in_memory_img = InMemoryUploadedFile(
                memory_buffer,
                None,
                img_file_name + '.' + img_file_format,
                img_file_format,
                None,
                None
            )
            return in_memory_img
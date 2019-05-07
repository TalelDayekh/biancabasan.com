import os
import re
import uuid
import shutil
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image


class ImgPathHandler():
    def __init__(self, img_file_path, artwork_title):
        self.img_file_path = img_file_path
        self.artwork_title = str(artwork_title)

        try:
            if not os.path.isfile(img_file_path):
                raise Exception
        except Exception:
            print(
                'ImgPathHandler needs to be passed path of existing image file'
            )
        else:
            self.initial_img_dir_path = os.path.dirname(self.img_file_path)
            # Remove characters that are not letters or numbers from
            # artwork_title, convert remaining ones to lowercase and
            # replace whitespaces with underscores.
            self.artwork_title = re.sub(
                '[^A-Za-z0-9\s]{1}', '', self.artwork_title
            ).replace(' ', '_').lower()

    def mkdir_from_artwork_title(self):
        os.chdir(self.initial_img_dir_path)
        new_img_dir_path = os.path.join(
            self.initial_img_dir_path,
            self.artwork_title
        )

        try:
            os.mkdir(self.artwork_title)
            return new_img_dir_path
        except FileExistsError as err:
            print(
                str(err) + ', a image directory already exists for this artwork'
            )
            return new_img_dir_path

    def add_uuid_to_duplicate_img_names(self, destination_dir_path):
        # Specify a destination path for the image file to check whether
        # an image with the same name already exists in that location.
        img_file = os.path.basename(self.img_file_path)
        img_file_destination_path = os.path.join(destination_dir_path, img_file)

        try:
            if os.path.isfile(img_file_destination_path):
                img_file_name, img_file_extension = os.path.splitext(img_file)
                unique_file_identifier = str(uuid.uuid4().hex)
                new_img_file = (
                    img_file_name
                    + '_' 
                    + unique_file_identifier 
                    + img_file_extension
                )

                old_img_file_path = self.img_file_path
                self.img_file_path = os.path.join(
                    os.path.dirname(self.img_file_path), new_img_file
                )

                # Update path with the old image file name
                # to the path with the new image file name.
                os.rename(old_img_file_path, self.img_file_path)
                return self.img_file_path
            else:
                raise Exception
        except Exception:
            return self.img_file_path

    def mv_img_to_new_dir(self):
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
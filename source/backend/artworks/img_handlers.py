import os
import re
from PIL import Image


class ImgPathHandler():
    def __init__(self, artwork_img_obj, artwork_title):
        self.artwork_img_obj = artwork_img_obj
        self.artwork_title = str(artwork_title)

        try:
            self.artwork_img_obj.path
        except AttributeError as err:
            print(err)
        else:
            # Remove characters that are not letters or numbers from
            # artwork_title, convert remaining ones to lowercase and
            # replace whitespaces with underscores.
            self.artwork_title = re.sub(
                '[^A-Za-z0-9\s]{1}', '', self.artwork_title).replace(
                ' ', '_').lower()
            
            self.initial_img_path = os.path.dirname(self.artwork_img_obj.path)
            self.new_img_path = os.path.join(
                self.initial_img_path, self.artwork_title
            )

    def mkdir_from_artwork_title(self):
        os.chdir(self.initial_img_path)
        try:
            os.mkdir(self.artwork_title)
        except FileExistsError as err:
            print(err)
        else:
            return(self.new_img_path)


class ImgManipulationsHandler():
    def __init__(self, img_file, new_img_width):
        self.img_file = img_file
        self.new_img_width = int(new_img_width)

    def resize_img_proportionally(self):
        try:
            self.img_file.verify
        except Exception:
            print('Not a valid image file')
        else:
            img_width, img_height = self.img_file.size
            new_img_height = (img_height/img_width) * self.new_img_width
            resized_img = self.img_file.resize(
                (self.new_img_width, int(round(new_img_height)))
            )
            return resized_img
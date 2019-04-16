import re
import os


class ImgPathHandler():
    def __init__(self, img_file, artwork_title):
        self.img_file = img_file
        self.artwork_title = artwork_title

        try:
            self.img_file.path
        except AttributeError as err:
            print(err)
        else:
            # Remove characters that are not letters or numbers from
            # artwork_title, convert remaining ones to lowercase and
            # replace whitespaces with underscores.
            self.artwork_title = re.sub(
                '[^A-Za-z0-9\s]{1}', '', self.artwork_title).replace(
                ' ', '_').lower()
            
            self.initial_img_path = os.path.dirname(self.img_file.path)
            self.new_img_path = os.path.join(
                self.initial_img_path, self.artwork_title
            )
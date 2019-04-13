# os
import os


class ArtworkImagesHandler():
    """
    Handles image paths and image manipulations
    """
    def __init__(self, img_file, artwork_title):
        self.img_file = img_file
        self.artwork_title = artwork_title

        try:
            self.img_file.path
        except AttributeError as err:
            print(err)
        else:
            # Convert artwork_title to all lowercase
            # and replace whitespace with underscore.
            self.artwork_title = self.artwork_title.lower()
            self.artwork_title = self.artwork_title.replace(' ', '_')

            self.initial_img_path = os.path.dirname(self.img_file.path)
            self.new_img_path = os.path.join(
                self.initial_img_path, self.artwork_title)

    def mkdir_from_artwork_title(self):
        if os.path.exists(self.new_img_path):
            pass
        else:
            os.chdir(self.initial_img_path)
            os.mkdir(self.artwork_title)
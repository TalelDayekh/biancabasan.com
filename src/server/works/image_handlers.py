from __future__ import annotations

import os
import re
import shutil
import uuid
from pathlib import Path
from typing import Optional

from django.conf import settings

from PIL import Image


class ImageHandler:
    image_widths = [1250, 2500]
    image_quality = 10

    def __init__(
        self, image_file: Path, work_title: Optional[str] = None
    ) -> None:
        self.media_root = settings.MEDIA_ROOT
        self.image_file = image_file
        self.work_title_directory_name = work_title
        self.work_title_directory_path = None

    @property
    def image_file_size(self) -> int:
        pass

    def _format_work_title(self) -> str:
        # Removes characters which are not letters or numbers
        # from a work title and replaces all whitespaces with
        # underscores and converts the string into lowercase.
        formatted_work_title = (
            re.sub("[^A-Za-z0-9\s]{1}", "", self.work_title_directory_name)
            .replace(" ", "_")
            .lower()
        )
        self.work_title_directory_name = formatted_work_title

    def _create_directory_from_work_title(self) -> None:
        work_title_directory_path = Path(self.media_root).joinpath(
            self.work_title_directory_name
        )
        work_title_directory_path.mkdir(parents=True, exist_ok=True)
        self.work_title_directory_path = work_title_directory_path

    def move_image_to_work_title_directory(self) -> None:
        try:
            if not self.work_title_directory_name:
                raise ValueError(
                    "A work title has to be provided for moving images to a new directory"
                )
            elif not self.image_file.is_file():
                raise OSError("Path is not a valid image file")
            else:
                self._format_work_title()
                self._create_directory_from_work_title()
                shutil.move(
                    str(self.image_file), str(self.work_title_directory_path)
                )
        except Exception as err:
            print(err)

    def delete_image(self) -> None:
        try:
            os.remove(self.image_file)
        except FileNotFoundError as err:
            print("No such image file to delete")

    @classmethod
    def create_web_images_set(
        cls, image_file: Path, work_title: Optional[str] = None
    ) -> List[ImageHandler]:
        try:
            if not image_file.is_file():
                raise OSError("Path is not a valid image file")
            else:
                uid = str(uuid.uuid4().hex)
                web_images = [
                    image_file.parent.joinpath(
                        "_".join([str(image_file.stem), uid, str(image_width)])
                        + str(image_file.suffix)
                    )
                    for image_width in cls.image_widths
                ]

                for web_image_file, image_width in zip(
                    web_images, cls.image_widths
                ):
                    shutil.copyfile(image_file, web_image_file)

                    # Resizes image proportionally to new widths
                    image_file_width, image_file_height = Image.open(
                        image_file
                    ).size
                    resized_image_height = (
                        image_file_height / image_file_width
                    ) * image_width
                    resized_image_file = Image.open(web_image_file).resize(
                        (image_width, int(round(resized_image_height)))
                    )
                    resized_image_file.save(
                        web_image_file, quality=cls.image_quality
                    )

                os.remove(image_file)

                return [cls(web_image, work_title) for web_image in web_images]
        except Exception as err:
            print(err)

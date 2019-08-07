from __future__ import annotations

import os
import re
import shutil
import uuid
from math import floor
from pathlib import Path
from typing import Optional

from django.conf import settings

from PIL import Image


class ImageDirectoryHandler:
    def __init__(self, work_title: str) -> None:
        self.work_title = str(work_title)
        self.formatted_work_title = self._format_work_title()
        self.image_directory_path = Path(settings.MEDIA_ROOT).joinpath(
            self.formatted_work_title
        )

    def _format_work_title(self) -> str:
        # Removes characters which are not letters or numbers
        # from a work title and replaces all whitespaces with
        # underscores and converts the string into lowercase.
        formatted_work_title = (
            re.sub("[^A-Za-z0-9\s]{1}", "", self.work_title)
            .replace(" ", "_")
            .lower()
        )
        return formatted_work_title

    def create_directory_from_formatted_work_title(self) -> None:
        try:
            if not self.work_title:
                raise ValueError(
                    "A work title has to be provided for creating a directory"
                )
            else:
                work_title_directory = self.image_directory_path
                work_title_directory.mkdir(parents=True, exist_ok=True)
        except Exception as err:
            print(err)


class ImageFileHandler:
    image_widths = [1250, 2500]
    image_quality = 20

    def __init__(
        self, image_file: Path, work_title_directory: Optional[Path] = None
    ) -> None:
        self.image_file = image_file
        self.work_title_directory = work_title_directory

    @property
    def image_file_type(self) -> str:
        return Image.open(self.image_file).format

    @property
    def floor_image_file_size(self) -> int:
        # Returns size in byte
        return floor(self.image_file.stat().st_size / 1024)

    def move_image_to_work_title_directory(self) -> None:
        try:
            if (
                not self.image_file.exists()
                or not self.work_title_directory.exists()
            ):
                raise Exception(
                    "A valid image file path and work title directory path has to be provided"
                )
            else:
                shutil.move(
                    str(self.image_file), str(self.work_title_directory)
                )
        except Exception as err:
            print(err)

    def delete_image(self) -> None:
        try:
            os.remove(self.image_file)
        except OSError as err:
            print("No image file to delete")

    @classmethod
    def create_web_images_set(
        cls, image_file: Path, work_title_directory: Optional[Path] = None
    ) -> List[ImageFileHandler]:
        try:
            Image.open(image_file)
        except OSError as err:
            print("A valid image file path has to be provided")
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

                # Resize image proportionally to new widths
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
            return [
                cls(web_image, work_title_directory)
                for web_image in web_images
            ]

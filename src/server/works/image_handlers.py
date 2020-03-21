from __future__ import annotations

import os
import re
import shutil
import uuid
from pathlib import Path
from typing import Type

from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image


def image_upload_handler(instance: Type[ImageModel], filename: str) -> str:
    uid = str(uuid.uuid4().hex)
    image_name = Path(filename).stem
    image_type = Path(filename).suffix
    image_file = image_name + "_" + uid + image_type

    formatted_work_title = format_work_title(instance.work)
    image_directory = "images/" + formatted_work_title + "/"

    upload_to = image_directory + image_file
    return upload_to


def format_work_title(work_title: str) -> str:
    # Removes characters which are not letters or numbers
    # from a work title and replaces all whitespaces with
    # underscores and converts the string into lowercase.
    formatted_work_title = (
        re.sub("[^A-Za-z0-9\s]{1}", "", str(work_title))
        .replace(" ", "_")
        .lower()
    )
    return formatted_work_title


class ImageValidationHandler:
    def __init__(self, image_file: InMemoryUploadedFile) -> None:
        self.image_file = image_file

    def _validate_image_format(self) -> bool:
        allowed_image_format = ["JPEG"]

        try:
            image = Image.open(self.image_file)
            return True if image.format in allowed_image_format else False
        except IOError:
            return False

    def _validate_image_size(self) -> bool:
        maximum_image_size = 2097152
        return True if self.image_file.size <= maximum_image_size else False

    def is_valid(self) -> bool:
        return self._validate_image_format() and self._validate_image_size()


class ImageFileHandler:
    def __init__(self, image_file: Path) -> None:
        self.image_file = image_file

    def delete_image_set(self):
        image_file_directory = self.image_file.parent
        image_name = self.image_file.stem
        images = os.listdir(image_file_directory)

        for image in images:
            if image_name in image:
                os.remove(image_file_directory.joinpath(image))

    @classmethod
    def create_web_image_set(
        cls, image_file: Path
    ) -> List[Type[ImageFileHandler]]:
        image_widths = [1250, 2500]
        image_quality = 20

        try:
            Image.open(image_file)
        except OSError as err:
            print("A valid image file path has to be provided")
        else:
            web_image_files = [
                image_file.parent.joinpath(
                    "_".join([image_file.stem, str(image_width)])
                    + image_file.suffix
                )
                for image_width in image_widths
            ]

            for web_image_file, image_width in zip(
                web_image_files, image_widths
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

                resized_image_file.save(web_image_file, quality=image_quality)
            return [cls(web_image) for web_image in web_image_files]

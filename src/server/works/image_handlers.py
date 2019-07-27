import re
import shutil
from pathlib import Path

from django.conf import settings


class ImagePathHandler:
    def __init__(self, image_file: Path, work_title: str) -> None:
        self.media_root = settings.MEDIA_ROOT
        self.image_file = image_file
        self.work_title_directory_name = self._format_work_title(work_title)
        self.work_title_directory_path = None

    def _format_work_title(self, work_title) -> str:
        # Removes characters which are not letters or numbers
        # from a work title and replaces all whitespaces with
        # underscores and converts the string into lowercase.
        formatted_work_title = (
            re.sub("[^A-Za-z0-9\s]{1}", "", work_title)
            .replace(" ", "_")
            .lower()
        )
        return formatted_work_title

    def _create_directory_from_work_title(self) -> Path:
        work_title_directory_path = Path(self.media_root).joinpath(
            self.work_title_directory_name
        )
        work_title_directory_path.mkdir(parents=True, exist_ok=True)
        self.work_title_directory_path = work_title_directory_path

    def move_image_to_work_title_directory(self):
        self._create_directory_from_work_title()
        shutil.move(str(self.image_file), str(self.work_title_directory_path))

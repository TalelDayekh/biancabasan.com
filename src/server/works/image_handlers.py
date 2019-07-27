import re
from pathlib import Path

from django.conf import settings


class ImagePathHandler:
    def __init__(self, work_title: str) -> None:
        self.media_root = settings.MEDIA_ROOT
        self.work_title = work_title
        self.formatted_work_title = self._format_work_title()

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

    def _create_directory_from_work_title(self) -> Path:
        work_title_directory = Path(self.media_root).joinpath(
            self.formatted_work_title
        )
        work_title_directory.mkdir(parents=True, exist_ok=True)
        return work_title_directory

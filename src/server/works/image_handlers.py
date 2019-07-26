from pathlib import Path

from django.conf import settings


class ImagePathHandler:
    def __init__(self, work_title: str) -> None:
        self.media_root = settings.MEDIA_ROOT
        self.work_title = work_title

    def _create_directory_from_work_title(self) -> Path:
        work_title_directory = Path(self.media_root).joinpath(self.work_title)
        work_title_directory.mkdir(parents=True, exist_ok=True)
        return work_title_directory

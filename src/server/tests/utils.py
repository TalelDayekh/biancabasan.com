import tempfile
from contextlib import contextmanager
from typing import Dict, List

from PIL import Image


def work_test_data() -> List[Dict]:
    return [
        {
            "title": "Black Square",
            "year_from": 2019,
            "year_to": 2019,
            "technique": "Oil on canvas",
            "height": 200.00,
            "width": 200.00,
            "depth": 3.5,
            "description": "A painting of a black square.",
        },
        {
            "title": "Black Square #2",
            "year_from": 2019,
            "year_to": 2019,
            "technique": "Oil on canvas",
            "height": 200.00,
            "width": 200.00,
            "depth": 3.5,
            "description": "A painting of a black square.",
        },
        {
            "title": "Black Square #3",
            "year_from": 2018,
            "year_to": 2018,
            "technique": "Oil on canvas",
            "height": 200.00,
            "width": 200.00,
            "depth": 3.5,
            "description": "A painting of a black square.",
        },
        {
            "title": "Black Square #4",
            "year_from": 1986,
            "year_to": 1986,
            "technique": "Oil on canvas",
            "height": 200.00,
            "width": 200.00,
            "depth": 3.5,
            "description": "A painting of a black square.",
        },
        {
            "title": "",
            "year_from": "",
            "year_to": "",
            "technique": "",
            "height": "",
            "width": "",
            "depth": "",
            "description": "",
        },
    ]


def authorization_test_data() -> Dict[str, str]:
    return {
        "old_password": "OldPassword123",
        "new_password": "NewPassword123",
        "new_password_confirm": "NewPassword123",
    }


@contextmanager
def create_temporary_test_image(
    image_format: str
) -> tempfile.NamedTemporaryFile:
    try:
        test_image = Image.new("RGB", (500, 500))
        temporary_image_file = tempfile.NamedTemporaryFile(
            suffix=f".{image_format}", prefix="black_square"
        )
        test_image.save(temporary_image_file)
        temporary_image_file.seek(0)
        yield temporary_image_file
    finally:
        temporary_image_file.close()

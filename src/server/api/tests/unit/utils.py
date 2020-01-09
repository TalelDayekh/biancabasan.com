from typing import Dict, List


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

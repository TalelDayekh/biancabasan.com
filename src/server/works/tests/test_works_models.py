from django.test import TestCase

from ..models import Work


class WorkModelsTest(TestCase):
    def test_default_work(self):
        work = Work()

        self.assertEqual(work.title, "")
        self.assertEqual(work.year_from, None)
        self.assertEqual(work.year_to, None)
        self.assertEqual(work.technique, "")
        self.assertEqual(work.height, None)
        self.assertEqual(work.width, None)
        self.assertEqual(work.depth, None)
        self.assertEqual(work.description, "")
        self.assertEqual(work.date_added, None)

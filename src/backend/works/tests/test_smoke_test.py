from django.test import TestCase
from ..image_handler import smoke_test


class InitialTest(TestCase):
    def test_smoke_test(self):
        hello_world = smoke_test()
        self.assertEqual(hello_world, 'Failed Test')
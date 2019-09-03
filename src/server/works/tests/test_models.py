# from django.test import TestCase

# from ..models import Image, Work


# class WorkModelTest(TestCase):
#     def test_default_work(self):
#         work = Work()

#         self.assertEqual(work.title, "")
#         self.assertEqual(work.year_from, None)
#         self.assertEqual(work.year_to, None)
#         self.assertEqual(work.technique, "")
#         self.assertEqual(work.height, None)
#         self.assertEqual(work.width, None)
#         self.assertEqual(work.depth, None)
#         self.assertEqual(work.description, "")
#         self.assertEqual(work.date_added, None)


# class ImageModelTest(TestCase):
#     def test_image_is_related_to_work(self):
#         work = Work(
#             title="Black Square",
#             year_to=2019,
#             technique="Oil on canvas",
#             description="A painting of a black square",
#         )
#         work.save()
#         image = Image()
#         image.work = work
#         image.save()

#         self.assertIn(image, work.images.all())

# import random
# import shutil
# import tempfile
# from contextlib import contextmanager
# from pathlib import Path

# from django.core.files.uploadedfile import SimpleUploadedFile
# from django.test import override_settings

# from api.v1.serializers import ImageSerializerVersion1, WorkSerializerVersion1
# from PIL import Image as pil_image
# from rest_framework.test import APITestCase
# from users.models import CustomUser

# from works.models import Image, Work

# image_get_request_test_folder = tempfile.mkdtemp(
#     prefix="image_get_request_test_folder"
# )
# image_post_request_test_folder = tempfile.mkdtemp(
#     prefix="image_post_request_test_folder"
# )
# image_delete_request_test_folder = tempfile.mkdtemp(
#     prefix="image_delete_request_test_folder"
# )


# @override_settings(
#     BASE_DIR=image_get_request_test_folder,
#     MEDIA_URL="/",
#     MEDIA_ROOT=image_get_request_test_folder,
# )
# class ImageGETTest(APITestCase):
#     @classmethod
#     def setUpTestData(cls):
#         cls.user = CustomUser.objects.create(username="get_image_user")
#         work = Work.objects.create(owner=cls.user, **test_data()[0])
#         cls.work_id = work.id
#         cls.images_id = []

#         # Uploads 5 images to user's work as test data
#         for i in range(5):
#             with create_temporary_test_image("JPEG") as test_image:
#                 image = Image.objects.create(
#                     work=work,
#                     image=SimpleUploadedFile(
#                         f"Black Square {i + 1}.JPEG", test_image.read()
#                     ),
#                 )
#                 cls.images_id.append(image.id)

#     def test_can_get_all_images_for_work(self):
#         res = self.client.get(
#             f"http://127.0.0.1:8000/api/v1/works/{self.work_id}/images"
#         )
#         images = Image.objects.filter(
#             work__owner__username=self.user, work__id=self.work_id
#         )
#         serializer = ImageSerializerVersion1(images, many=True)

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res.data, serializer.data)

#     def test_cannot_get_images_from_invalid_work_id(self):
#         res_invalid_work_id_int = self.client.get(
#             "http://127.0.0.1:8000/api/v1/works/9999/images"
#         )
#         res_invalid_work_id_str = self.client.get(
#             "http://127.0.0.1:8000/api/v1/works/NaN/images"
#         )

#         self.assertEqual(res_invalid_work_id_int.status_code, 404)
#         self.assertEqual(res_invalid_work_id_str.status_code, 404)

#     def test_can_get_image_for_work(self):
#         # Tests with a random image from
#         # the test data on each test run.
#         image_id = random.choice(self.images_id)
#         res = self.client.get(
#             f"http://127.0.0.1:8000/api/v1/works/{self.work_id}/images/{image_id}"
#         )
#         image = Image.objects.get(
#             work__owner__username=self.user, work__id=self.work_id, id=image_id
#         )
#         serializer = ImageSerializerVersion1(image)

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res.data, serializer.data)

#     def test_cannot_get_image_from_invalid_image_or_work_id(self):
#         image_id = random.choice(self.images_id)
#         res_invalid_image_id_int = self.client.get(
#             f"http://127.0.0.1:8000/api/v1/works/{self.work_id}/images/9999"
#         )
#         res_invalid_image_id_str = self.client.get(
#             f"http://127.0.0.1:8000/api/v1/works/{self.work_id}/images/NaN"
#         )
#         res_invalid_work_id_int = self.client.get(
#             f"http://127.0.0.1:8000/api/v1/works/9999/images/{image_id}"
#         )
#         res_invalid_work_id_str = self.client.get(
#             f"http://127.0.0.1:8000/api/v1/works/NaN/images/{image_id}"
#         )

#         self.assertEqual(res_invalid_image_id_int.status_code, 404)
#         self.assertEqual(res_invalid_image_id_str.status_code, 404)
#         self.assertEqual(res_invalid_work_id_int.status_code, 404)
#         self.assertEqual(res_invalid_work_id_str.status_code, 404)

#     @classmethod
#     def tearDownClass(cls):
#         shutil.rmtree(image_get_request_test_folder)


# @override_settings(
#     BASE_DIR=image_post_request_test_folder,
#     MEDIA_URL="/",
#     MEDIA_ROOT=image_post_request_test_folder,
# )
# class ImagePOSTTest(APITestCase):
#     def setUp(self):
#         user_one = CustomUser.objects.create(username="post_image_user_one")
#         self.work = Work.objects.create(owner=user_one, **test_data()[0])
#         self.client.force_authenticate(user_one)

#     def test_can_post_valid_image_to_work_by_user(self):
#         with create_temporary_test_image("JPEG") as test_image:
#             res = self.client.post(
#                 f"http://127.0.0.1:8000/api/v1/works/{self.work.id}/images",
#                 {"image": test_image},
#                 format="multipart",
#             )

#             self.assertEqual(res.status_code, 201)

#     def test_cannot_post_invalid_image_to_work_by_user(self):
#         with create_temporary_test_image("PNG") as test_image:
#             res = self.client.post(
#                 f"http://127.0.0.1:8000/api/v1/works/{self.work.id}/images",
#                 {"image": test_image},
#                 format="multipart",
#             )

#             self.assertEqual(res.status_code, 400)

#     def test_cannot_post_valid_image_to_work_by_other_user(self):
#         user_two = CustomUser.objects.create(username="post_image_user_two")
#         work = Work.objects.create(owner=user_two, **test_data()[0])

#         with create_temporary_test_image("JPEG") as test_image:
#             res = self.client.post(
#                 f"http://127.0.0.1:8000/api/v1/works/{work.id}/images",
#                 {"image": test_image},
#                 format="multipart",
#             )

#             self.assertEqual(res.status_code, 400)

#     def test_cannot_post_valid_image_to_work_as_unauthorized_user(self):
#         self.client.force_authenticate(user=None)

#         with create_temporary_test_image("JPEG") as test_image:
#             res = self.client.post(
#                 f"http://127.0.0.1:8000/api/v1/works/{self.work.id}/images",
#                 {"image": test_image},
#                 format="multipart",
#             )

#             self.assertEqual(res.status_code, 401)

#     @classmethod
#     def tearDownClass(cls):
#         shutil.rmtree(image_post_request_test_folder)


# @override_settings(
#     BASE_DIR=image_delete_request_test_folder,
#     MEDIA_URL="/",
#     MEDIA_ROOT=image_delete_request_test_folder,
# )
# class ImageDELETETest(APITestCase):
#     def setUp(self):
#         user_one = CustomUser.objects.create(username="delete_image_user_one")
#         user_two = CustomUser.objects.create(username="delete_image_user_two")
#         user_one_work = Work.objects.create(owner=user_one, **test_data()[0])
#         user_two_work = Work.objects.create(owner=user_two, **test_data()[0])
#         self.user_one_work_id = user_one_work.id
#         self.user_two_work_id = user_two_work.id
#         self.client.force_authenticate(user_one)

#         with create_temporary_test_image("JPEG") as test_image:
#             user_one_image = Image.objects.create(
#                 work=user_one_work,
#                 image=SimpleUploadedFile(test_image.name, test_image.read()),
#             )
#             self.user_one_image_id = user_one_image.id

#         with create_temporary_test_image("JPEG") as test_image:
#             user_two_image = Image.objects.create(
#                 work=user_two_work,
#                 image=SimpleUploadedFile(test_image.name, test_image.read()),
#             )
#             self.user_two_image_id = user_two_image.id

#     def test_can_delete_image_for_work_by_user(self):
#         res = self.client.delete(
#             f"http://127.0.0.1:8000/api/v1/works/{self.user_one_work_id}/images/{self.user_one_image_id}"
#         )

#         self.assertEqual(res.status_code, 204)

#     def test_cannot_delete_image_for_work_by_other_user(self):
#         res = self.client.delete(
#             f"http://127.0.0.1:8000/api/v1/works/{self.user_two_work_id}/images/{self.user_two_image_id}"
#         )

#         self.assertEqual(res.status_code, 404)

#     def test_cannot_delete_image_for_work_as_unauthorized_user(self):
#         self.client.force_authenticate(user=None)
#         res = self.client.delete(
#             f"http://127.0.0.1:8000/api/v1/works/{self.user_one_work_id}/images/{self.user_one_image_id}"
#         )

#         self.assertEqual(res.status_code, 401)

#     @classmethod
#     def tearDownClass(cls):
#         shutil.rmtree(image_delete_request_test_folder)

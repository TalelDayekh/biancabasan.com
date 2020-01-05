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
# work_delete_request_test_folder = tempfile.mkdtemp(
#     prefix="work_delete_request_test_folder"
# )


# def test_data() -> list:
#     return [
#         {
#             "title": "Black Square",
#             "year_to": 2019,
#             "technique": "Oil on canvas",
#             "description": "A painting of a black square.",
#         },
#         {
#             "title": "Black Square #2",
#             "year_to": 2019,
#             "technique": "Oil on canvas",
#             "description": "A painting of a black square",
#         },
#         {
#             "title": "Black Square #3",
#             "year_to": 2018,
#             "technique": "Oil on canvas",
#             "description": "A painting of a black square",
#         },
#         {
#             "title": "Black Square #4",
#             "year_to": 1986,
#             "technique": "Oil on canvas",
#             "description": "A painting of a black square",
#         },
#         {"title": "", "year_to": "", "technique": "", "description": ""},
#     ]


# @contextmanager
# def create_temporary_test_image(
#     image_format: str
# ) -> tempfile.NamedTemporaryFile:
#     try:
#         test_image = pil_image.new("RGB", (500, 500))
#         temporary_image_file = tempfile.NamedTemporaryFile(
#             suffix=f".{image_format}", prefix="black_square"
#         )
#         test_image.save(temporary_image_file)
#         temporary_image_file.seek(0)
#         yield temporary_image_file
#     finally:
#         temporary_image_file.close()


# class WorkGETTest(APITestCase):
#     @classmethod
#     def setUpTestData(cls):
#         user = CustomUser.objects.create(username="get_work_user")
#         Work.objects.bulk_create(
#             [
#                 Work(owner=user, **test_data()[0]),
#                 Work(owner=user, **test_data()[1]),
#                 Work(owner=user, **test_data()[2]),
#             ]
#         )

#     def test_can_get_all_works(self):
#         res = self.client.get("http://127.0.0.1:8000/api/v1/works")
#         works = Work.objects.all()
#         serializer = WorkSerializerVersion1(works, many=True)

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res.data, serializer.data)

#     def test_can_get_all_works_from_year_to(self):
#         res = self.client.get(
#             "http://127.0.0.1:8000/api/v1/works", {"year_to": 2019}
#         )
#         works = Work.objects.filter(year_to=2019)
#         serializer = WorkSerializerVersion1(works, many=True)

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res.data, serializer.data)

#     def test_cannot_get_works_from_invalid_year_to(self):
#         res_invalid_year_to_int = self.client.get(
#             "http://127.0.0.1:8000/api/v1/works", {"year_to": 2020}
#         )
#         res_invalid_year_to_str = self.client.get(
#             "http://127.0.0.1:8000/api/v1/works", {"year_to": "NaN"}
#         )

#         self.assertEqual(res_invalid_year_to_int.data, [])
#         self.assertEqual(res_invalid_year_to_str.status_code, 400)

#     def test_can_get_sorted_list_of_years(self):
#         res = self.client.get(f"http://127.0.0.1:8000/api/v1/works/years")

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res.data, [2019, 2018])

#     def test_can_get_work_from_work_id(self):
#         work = Work.objects.get(title="Black Square #3")
#         res = self.client.get(f"http://127.0.0.1:8000/api/v1/works/{work.id}")
#         serializer = WorkSerializerVersion1(work)

#         self.assertEqual(res.status_code, 200)
#         self.assertEqual(res.data, serializer.data)

#     def test_cannot_get_work_from_invalid_work_id(self):
#         res_invalid_work_id_int = self.client.get(
#             "http://127.0.0.1:8000/api/v1/works/9999"
#         )
#         res_invalid_work_id_str = self.client.get(
#             "http://127.0.0.1:8000/api/v1/works/Nan"
#         )

#         self.assertEqual(res_invalid_work_id_int.status_code, 404)
#         self.assertEqual(res_invalid_work_id_str.status_code, 404)

#     @classmethod
#     def tearDownClass(cls):
#         # Adding the tearDownClass seems to prevent
#         # connection already closed InterfaceError.
#         pass


# class WorkPOSTTest(APITestCase):
#     def setUp(self):
#         user = CustomUser.objects.create(username="post_work_user")
#         self.client.force_authenticate(user)

#     def test_can_create_work_for_user(self):
#         res = self.client.post(
#             "http://127.0.0.1:8000/api/v1/works", test_data()[0]
#         )

#         self.assertEqual(res.status_code, 201)

#     def test_cannot_create_work_for_unauthorized_user(self):
#         self.client.force_authenticate(user=None)
#         res = self.client.post(
#             "http://127.0.0.1:8000/api/v1/works", test_data()[0]
#         )

#         self.assertEqual(res.status_code, 401)

#     def test_cannot_create_work_from_invalid_payload(self):
#         res = self.client.post(
#             "http://127.0.0.1:8000/api/v1/works", test_data()[4]
#         )

#         self.assertEqual(res.status_code, 400)

#     def test_cannot_create_work_with_out_of_range_year(self):
#         res = self.client.post(
#             "http://127.0.0.1:8000/api/v1/works", test_data()[3]
#         )

#         self.assertEqual(res.status_code, 400)

#     @classmethod
#     def tearDownClass(cls):
#         # Adding the tearDownClass seems to prevent
#         # connection already closed InterfaceError.
#         pass


# class WorkPATCHTest(APITestCase):
#     def setUp(self):
#         user_one = CustomUser.objects.create(username="patch_work_user_one")
#         user_two = CustomUser.objects.create(username="patch_work_user_two")
#         user_one_work = Work.objects.create(owner=user_one, **test_data()[0])
#         user_two_work = Work.objects.create(owner=user_two, **test_data()[0])
#         self.user_one_work_id = user_one_work.id
#         self.user_two_work_id = user_two_work.id
#         self.updated_payload = {"year_to": 2020, "height": 150, "width": 200}
#         self.client.force_authenticate(user_one)

#     def test_can_update_work_for_user(self):
#         res = self.client.patch(
#             f"http://127.0.0.1:8000/api/v1/works/{self.user_one_work_id}",
#             self.updated_payload,
#         )

#         self.assertEqual(res.status_code, 200)
#         self.assertTrue(res.data["year_to"] == 2020)
#         self.assertTrue(res.data["height"] == 150)
#         self.assertTrue(res.data["width"] == 200)

#     def test_cannot_update_work_for_other_user(self):
#         res = self.client.patch(
#             f"http://127.0.0.1:8000/api/v1/works/{self.user_two_work_id}",
#             self.updated_payload,
#         )

#         self.assertEqual(res.status_code, 404)

#     def test_cannot_update_work_as_unauthorized_user(self):
#         self.client.force_authenticate(user=None)
#         res = self.client.patch(
#             f"http://127.0.0.1:8000/api/v1/works/{self.user_one_work_id}",
#             self.updated_payload,
#         )

#         self.assertEqual(res.status_code, 401)

#     def test_cannot_update_work_from_invalid_work_id(self):
#         res_invalid_work_id_int = self.client.patch(
#             "http://127.0.0.1:8000/api/v1/works/9999", self.updated_payload
#         )
#         res_invalid_work_id_str = self.client.patch(
#             "http://127.0.0.1:8000/api/v1/works/NaN", self.updated_payload
#         )

#         self.assertEqual(res_invalid_work_id_int.status_code, 404)
#         self.assertEqual(res_invalid_work_id_str.status_code, 404)

#     @classmethod
#     def tearDownClass(cls):
#         # Adding the tearDownClass seems to prevent
#         # connection already closed InterfaceError.
#         pass


# @override_settings(
#     BASE_DIR=work_delete_request_test_folder,
#     MEDIA_URL="/",
#     MEDIA_ROOT=work_delete_request_test_folder,
# )
# class WorkDELETETest(APITestCase):
#     def setUp(self):
#         user_one = CustomUser.objects.create(username="delete_work_user_one")
#         user_two = CustomUser.objects.create(username="delete_work_user_two")
#         self.user_one_work = Work.objects.create(
#             owner=user_one, **test_data()[0]
#         )
#         user_two_work = Work.objects.create(owner=user_two, **test_data()[0])
#         self.user_one_work_id = self.user_one_work.id
#         self.user_two_work_id = user_two_work.id
#         self.uploaded_images_paths = []
#         self.client.force_authenticate(user_one)

#         for i in range(5):
#             with create_temporary_test_image("JPEG") as test_image:
#                 image = Image.objects.create(
#                     work=self.user_one_work,
#                     image=SimpleUploadedFile(
#                         f"Black Square {i + 1}.JPEG", test_image.read()
#                     ),
#                 )
#                 self.uploaded_images_paths.append(Path(image.image.path))

#         with create_temporary_test_image("JPEG") as test_image:
#             Image.objects.create(
#                 work=user_two_work,
#                 image=SimpleUploadedFile(test_image.name, test_image.read()),
#             )

#     def test_can_delete_work_for_user(self):
#         res = self.client.delete(
#             f"http://127.0.0.1:8000/api/v1/works/{self.user_one_work_id}"
#         )

#         for image in self.uploaded_images_paths:
#             self.assertFalse(image.exists())
#         self.assertEqual(res.status_code, 204)

#     def test_cannot_delete_work_by_other_user(self):
#         res = self.client.delete(
#             f"http://127.0.0.1:8000/api/v1/works/{self.user_two_work_id}"
#         )

#         self.assertEqual(res.status_code, 404)

#     def test_cannot_delete_work_as_unauthorized_user(self):
#         self.client.force_authenticate(user=None)
#         res = self.client.delete(
#             f"http://127.0.0.1:8000/api/v1/works/{self.user_one_work_id}"
#         )

#         self.assertEqual(res.status_code, 401)

#     @classmethod
#     def tearDownClass(cls):
#         shutil.rmtree(work_delete_request_test_folder)


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

from django.test import TestCase

from api.views import GetSerializerClasses


class SerializerRetrievalTest(TestCase):
    def test_can_get_correct_serializers_for_api_version(self):
        work_serializer = GetSerializerClasses("v1").work_serializer
        image_serializer = GetSerializerClasses("v1").image_serializer

        self.assertEqual(work_serializer.__name__, "WorkSerializerVersion1")
        self.assertEqual(image_serializer.__name__, "ImageSerializerVersion1")

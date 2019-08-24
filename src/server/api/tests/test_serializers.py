from django.test import TestCase

from api.serializers import get_serializer_classes


class SerializersTest(TestCase):
    def test_can_get_correct_serializers_for_api_version(self):
        work_serializer, image_serializer = get_serializer_classes("v1")

        self.assertEqual(work_serializer.__name__, "WorkSerializerVersion1")
        self.assertEqual(image_serializer.__name__, "ImageSerializerVersion1")

    def test_cannot_get_serializers_for_invalid_api_version(self):
        with self.assertRaises(TypeError):
            work_serializer, image_serializer = get_serializer_classes(
                "invalid_api_version"
            )

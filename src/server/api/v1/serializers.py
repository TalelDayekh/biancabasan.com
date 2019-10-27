from rest_framework import serializers
from users.models import CustomUser

from works.models import Image, Work


class OwnerSerializerVersion1(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "id"]


class ImageSerializerVersion1(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["work_id", "id", "image"]


class WorkSerializerVersion1(serializers.ModelSerializer):
    owner = OwnerSerializerVersion1(read_only=True)
    images = ImageSerializerVersion1(many=True, read_only=True)

    class Meta:
        model = Work
        fields = [
            "owner",
            "id",
            "title",
            "year_from",
            "year_to",
            "technique",
            "height",
            "width",
            "depth",
            "description",
            "created_at",
            "images",
        ]

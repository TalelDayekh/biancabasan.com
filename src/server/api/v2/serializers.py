from rest_framework import serializers
from users.models import CustomUser

from works.models import Image, Work


class PasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)


class PasswordUpdateSerializer(PasswordResetSerializer):
    old_password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "id"]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["work_id", "id", "image"]


class WorkSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Work
        fields = [
            "user",
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

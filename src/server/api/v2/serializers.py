from rest_framework import serializers


class PasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)


class PasswordUpdateSerializer(PasswordResetSerializer):
    old_password = serializers.CharField(required=True)

from rest_framework import serializers


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)


class PasswordUpdateSerializer(PasswordResetSerializer):
    old_password = serializers.CharField(required=True)

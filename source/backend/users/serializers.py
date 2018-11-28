"""
users serializers
"""
from rest_framework import serializers

from django.contrib.auth.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    # Set password field to write only
    password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user_object = User(
            username = validated_data['username'],
            email = validated_data['email']
        )
        user_object.set_password(validated_data['password'])
        user_object.save()

        return validated_data
from rest_framework import serializers

from .models import ArtworkTitle, ArtworkDetails


class ArtworkTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtworkTitle
        fields = ('id', 'title')


class ArtworkDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtworkDetails
        fields = ('id', 'title', 'height', 'width', 'description')
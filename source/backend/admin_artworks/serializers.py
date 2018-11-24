from rest_framework import serializers

from .models import ArtworkTitle, ArtworkDetails, ArtworkImages


class ArtworkTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtworkTitle
        fields = ('id', 'title')


class ArtworkDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtworkDetails
        fields = ('id', 'title_id', 'height', 'width', 'description')


class ArtworkImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtworkImages
        fields = ('id', 'title_id', 'images')
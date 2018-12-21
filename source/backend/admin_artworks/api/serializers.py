"""
admin_artworks serializers
"""
from rest_framework import serializers

from ..models import (
    ArtworkTitles,
    ArtworkDetails,
    ArtworkImages,
)


# Artwork images
class ArtworkImagesListSerializer(serializers.RelatedField):

    def to_representation(self, value):

        image = '%s' % (value.image)

        return image


class ArtworkImagesCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArtworkImages
        fields = (
            'id',
            'title',
            'image',
        )


# Artwork details
class ArtworkDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArtworkDetails
        fields = (
            'id',
            'title',
            'year_from',
            'year_to',
            'material',
            'height',
            'width',
            'depth',
            'description',
        )


# Artwork titles
class ArtworkTitlesSerializer(serializers.ModelSerializer):

    # Nest serializers as fields
    details = ArtworkDetailsSerializer()
    images_list = ArtworkImagesListSerializer(many = True, read_only = True)

    class Meta:
        model = ArtworkTitles
        fields = (
            'id',
            'owner',
            'title',
            # Nested fields
            'details',
            'images_list',
        )
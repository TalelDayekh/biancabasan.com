"""
admin_artworks serializers
"""
from rest_framework import serializers

from ..models import (
    ArtworkTitles,
    ArtworkDetails,
    ArtworkImages,
)


# Artwork details
class ArtworkDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArtworkDetails
        fields = (
            'id',
            'title_id',
            'height',
            'width',
            'description',
        )


# Artwork images
class ArtworkImagesSerializer(serializers.RelatedField):

    def to_representation(self, value):
        # Add id and image as key-value pair in dictionary
        image_dict = {}
        image_dict['id: ' '%d' % (value.id)] = '%s' % (value.image)

        return image_dict


# Artwork titles
class ArtworkTitlesSerializer(serializers.ModelSerializer):

    # Nesting serializers as fields
    details = ArtworkDetailsSerializer(many = True, read_only = True)
    images_list = ArtworkImagesSerializer(many = True, read_only = True)

    class Meta:
        model = ArtworkTitles
        fields = (
            'id',
            'owner',
            'title',
            'details',
            'images_list',
        )
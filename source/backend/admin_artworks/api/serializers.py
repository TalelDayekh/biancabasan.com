from rest_framework import serializers
from ..models import(
    ArtworkInfo,
    ArtworkImages
)


"""
admin_artworks serializers
"""
# Artwork images
# Serialize a list with image titles
# to nest in artwork info serializer
class ArtworkImagesListSerializer(serializers.RelatedField):
    def to_representation(self, value):
        image = "{}".format(value.image)
        return image

class ArtworkImagesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtworkImages
        fields = (
            'id',
            'artwork_info',
            'image'
        )


# Artwork
# Serialize all info together with
# all images for an artwork object
class ArtworkSerializer(serializers.ModelSerializer):
    # Nest images serializer as field
    images_list = ArtworkImagesListSerializer(many=True, read_only=True)
    # Display owner with username instead of id
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = ArtworkInfo
        fields = (
            'id',
            'owner',
            'title',
            'year_from',
            'year_to',
            'material',
            'height',
            'width',
            'depth',
            'description',
            # Nested field
            'images_list'
        )
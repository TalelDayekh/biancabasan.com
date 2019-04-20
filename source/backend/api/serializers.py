from rest_framework import serializers
from artworks.models import ArtworkDetails, ArtworkImages


class ArtworkImagesSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    img = serializers.ImageField()

    def create(self, validated_data):
        return ArtworkImages.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.img = validated_data.get('img', instance.img)
        return instance


class ArtworkDetailsSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=200)
    images = ArtworkImagesSerializer(many=True)

    def create(self, validated_data):
        return ArtworkDetails.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.images = validated_data.get('images', instance.images)
        instance.save()
        return instance
from django.db import models


class ArtworkDetails(models.Model):
    title = models.CharField(max_length=200)


class ArtworkImages(models.Model):
    artwork_details = models.ForeignKey(
        ArtworkDetails,
        related_name='images',
        on_delete=models.CASCADE
    )
    img = models.ImageField(upload_to='images')
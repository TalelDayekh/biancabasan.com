from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


"""
Artwork info
"""
class ArtworkInfo(models.Model):
    title = models.CharField(max_length=200)
    year_from = models.IntegerField(blank=True, null=True)
    year_to = models.IntegerField()
    material = models.CharField(max_length=500)
    height = models.FloatField()
    width = models.FloatField()
    depth = models.FloatField(blank=True, null=True)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    # ForeignKey relation to user
    owner = models.ForeignKey(
        User,
        related_name="artworks",
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = 'Artwork Info'

    def __str__(self):
        return(
            'ID: '
            + str(self.id)
            + ' ARTWORK TITLE: '
            + self.title
            + ' USER: '
            + str(self.owner)
        )


"""
Artwork images
"""
class ArtworkImages(models.Model):
    image = models.ImageField(upload_to='images')
    date_added = models.DateTimeField(auto_now_add=True)

    # ForeignKey relation to artwork info
    artwork_info = models.ForeignKey(
        ArtworkInfo,
        related_name="images_list",
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = 'Images'
    
    def __str__(self):
        return(
            'FOREIGN KEY ID: '
            + str(self.artwork_info.id)
            + ' ID: '
            + str(self.id)
            + ' IMAGE: '
            + str(self.image)
        )
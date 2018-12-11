from django.db import models
from django.conf import settings


"""
Artwork title
"""
class ArtworkTitles(models.Model):
    title = models.CharField(max_length = 200)
    date_added = models.DateTimeField(auto_now_add = True)

    # ForeignKey relation
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
    )

    class Meta:
        verbose_name_plural = 'titles'

    def __str__(self):
        return (
            'ID: '
            + str(self.id)
            + ' Title: '
            + self.title
            + ' Owner: '
            + str(self.owner)
        )


"""
Artwork details
"""
class ArtworkDetails(models.Model):
    height = models.FloatField()
    width = models.FloatField()
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add = True)

    # OneToOne relation
    title = models.OneToOneField(
        ArtworkTitles,
        related_name = 'details',
        on_delete = models.CASCADE,
    )

    class Meta:
        verbose_name_plural = 'details'

    def __str__(self):
        return (
            'ID: '
            + str(self.id)
            + ' Title-ID: '
            + str(self.title.id)
            + ' Description: '
            + self.description
        )


"""
Artwork Images
"""
class ArtworkImages(models.Model):
    image = models.ImageField(upload_to = 'images')
    date_added = models.DateTimeField(auto_now_add = True)

    # ForeignKey relation
    title = models.ForeignKey(
        ArtworkTitles,
        related_name = 'images_list',
        on_delete = models.CASCADE,
    )

    class Meta:
        verbose_name_plural = 'images'
    
    def __str__(self):
        return (
            'ID: '
            + str(self.id)
            + ' Title-ID: '
            + str(self.title.id)
            + ' Image: '
            + str(self.image)
        )
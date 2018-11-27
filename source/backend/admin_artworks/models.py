from django.db import models

from django.contrib.auth.models import User


"""
Artwork title
"""
class ArtworkTitle(models.Model):
    title = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    # Connect data to user
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + str(' ') + str(self.id)


"""
Artwork details
"""
class ArtworkDetails(models.Model):
    title_id = models.ForeignKey(ArtworkTitle, on_delete=models.CASCADE)
    height = models.FloatField()
    width = models.FloatField()
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


"""
Artwork images
"""
class ArtworkImages(models.Model):
    title_id = models.ForeignKey(ArtworkTitle, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='images')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.images)
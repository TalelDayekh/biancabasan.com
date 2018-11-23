from django.db import models


"""
Artwork title
"""
class ArtworkTitle(models.Model):
    title = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + str(' ') + str(self.id)


"""
Artwork details
"""
class ArtworkDetails(models.Model):
    title = models.ForeignKey(ArtworkTitle, on_delete=models.CASCADE)
    height = models.FloatField()
    width = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return self.description
# Models
from django.db import models
from django.conf import settings


class ArtworkDetails(models.Model):
    """
    Provide all details for an artwork
    """
    title = models.CharField(max_length=200)
    from_year = models.IntegerField()
    to_year = models.IntegerField()
    materials = models.CharField(max_length=500)
    height = models.FloatField()
    width = models.FloatField()
    depth = models.FloatField(null=True, blank=True)
    description = models.TextField()
from django.db import models


class WorksImages(models.Model):
    image = models.ImageField(upload_to="images")

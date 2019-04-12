# Django admin
from django.contrib import admin
# Local imports
# Models
from .models import(
    ArtworkDetails,
    ArtworkImages
)


"""
Registered models
"""
admin.site.register(ArtworkDetails)
admin.site.register(ArtworkImages)
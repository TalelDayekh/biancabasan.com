# Django admin
from django.contrib import admin
# Local imports
# Models
from .models import(
    ArtworkDetails
)


"""
Registered models
"""
admin.site.register(ArtworkDetails)
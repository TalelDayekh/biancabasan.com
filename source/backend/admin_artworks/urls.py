from django.urls import path, include
from . import views


app_name = 'admin_artworks'

urlpatterns = [
    # List artworks
    path('all_artworks/', views.artworks_list),

    # Add artworks
    # Add info
    path('add_artwork_info/', views.create_artwork_info),
    # Add images
    path('add_artwork_images/', views.add_artwork_images)
]
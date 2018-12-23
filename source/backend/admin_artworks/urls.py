from django.urls import path, include

from . import views


app_name = 'admin_artworks'


urlpatterns = [
    # List artworks
    path('artworks_list/', views.artworks_list),

    # Create artworks
    path('add_title/', views.artwork_create_title),
    path('add_details/', views.artwork_create_details),
    # ADD ID TO IMAGES PATH #
    path('add_images/', views.artwork_add_images),

    # Edit artworks
    path('edit_title/<int:id>', views.artwork_edit_title),
    path('edit_details/<int:id>', views.artwork_edit_details),
]
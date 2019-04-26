from django.urls import path
from . import views


urlpatterns = [
    path('api/artworks_list/', views.artworks_list),
    path('api/artworks_add_details/', views.create_artwork_details),
    path('api/artworks_add_images/', views.create_artwork_images)
]
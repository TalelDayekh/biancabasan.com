from django.urls import path
from . import views


urlpatterns = [
    path('artworks_list/', views.artworks_list)
]
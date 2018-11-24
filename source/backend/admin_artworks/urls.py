from django.urls import path, include

from rest_framework import routers

from . import views


app_name = 'admin_artworks'


router = routers.DefaultRouter()
router.register('artwork_titles', views.ArtworkTitleViewSet)
router.register('artworks_details', views.ArtworkDetailsViewSet)
router.register('artworks_images', views.ArtworkImagesViewSet)

urlpatterns = [
    path('', include(router.urls))
]
from django.urls import path, include

from rest_framework import routers

from . import views


app_name = 'users'


router = routers.DefaultRouter()
router.register('register', views.CreateUserViewSet)

urlpatterns = [
    path('', include(router.urls))
]
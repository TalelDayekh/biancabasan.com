from django.urls import path

from api import views

urlpatterns = [
    path("<str:version>/users/<str:username>/works/", views.Works.as_view())
]

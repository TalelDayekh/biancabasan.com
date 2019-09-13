from django.urls import path

from api import views

urlpatterns = [
    path(
        "<str:version>/users/<str:username>/works",
        views.AllWorks.as_view(),
        name="Works",
    )
]

from django.urls import path

from api import views

urlpatterns = [
    path(
        "<str:version>/users/<str:username>/works/",
        views.AllWorks.as_view(),
        name="all-works",
    ),
    path(
        "<str:version>/users/<str:username>/works/<int:pk>/",
        views.SingleWork.as_view(),
        name="single-work",
    ),
]

from django.urls import path

from api import views

urlpatterns = [
    path("<str:version>/works/", views.AllWorks.as_view(), name="all-works"),
    path(
        "<str:version>/works/<int:pk>/",
        views.SingleWork.as_view(),
        name="single-work",
    ),
    path(
        "<str:version>/<str:username>/works/years/",
        views.YearsToList.as_view(),
        name="years-to",
    ),
]

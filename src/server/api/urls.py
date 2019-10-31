from django.conf.urls import url

from api import views

urlpatterns = [
    url(
        r"^(?P<version>\w+)/works$", views.WorkList.as_view(), name="work_list"
    ),
    url(
        r"^(?P<version>\w+)/works/(?P<work_id>\d+)/images$",
        views.ImageList.as_view(),
        name="image_list",
    ),
    url(
        r"^(?P<version>\w+)/works/(?P<work_id>\d+)/images/(?P<image_id>\d+)$",
        views.ImageDetail.as_view(),
        name="image_detail",
    ),
]

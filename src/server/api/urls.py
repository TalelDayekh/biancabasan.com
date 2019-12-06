from django.conf.urls import url

from api import user_authentication, views

urlpatterns = [
    url(
        r"^login",
        user_authentication.AuthenticationToken.as_view(),
        name="authentication_token",
    ),
    url(
        r"^(?P<version>\w+)/works$", views.WorkList.as_view(), name="work_list"
    ),
    url(
        r"^(?P<version>\w+)/works/(?P<work_id>\d+)$",
        views.WorkDetail.as_view(),
        name="work_detail",
    ),
    url(
        r"^(?P<version>\w+)/works/years$",
        views.WorkYearsList.as_view(),
        name="work_years_list",
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

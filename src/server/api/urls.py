from django.conf.urls import url

from api import views

urlpatterns = [
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


# delete a specific image for a specific work

# urlpatterns = [
#     url(r'^(?P<version>.*)/(?P<username>[/.*])/images', views.AllImages.as_view(), name='all_images')
#     # url(r'^(?P<version>(.+:?))/works$', views.AllImages.as_view(), name='all_images')
# ]


# from django.urls import path, register_converter
# from django.urls.converters import StringConverter

# from api import views


# class BlaConverter:
#     regex = '.*'

#     def to_python(self, value):
#         if value:
#             print(value)
#             return value
#         else:
#             return None

#     def to_url(self, value):
#         return value if value is not None else ''

# register_converter(BlaConverter, 'whatever')


# urlpatterns = [
#     path("<str:version>/works/", views.AllWorks.as_view(), name="all-works"),
#     path(
#         "<str:version>/works/<int:work_id>/",
#         views.SingleWork.as_view(),
#         name="single-work",
#     ),
#     path(
#         "<str:version>/<str:username>/works/years/",
#         views.YearsToList.as_view(),
#         name="years-to",
#     ),


#     path(
#         "<str:version>/users/<whatever:username>/",
#         views.AllImages.as_view(),
#         name="all-images",
#     ),
#     # path(
#     #     "<str:version>/users/<str:username>/works/<int:work_id>/images/<int:image_id>/",
#     #     views.SingleImage.as_view(),
#     #     name="single-image",
#     # ),
# ]

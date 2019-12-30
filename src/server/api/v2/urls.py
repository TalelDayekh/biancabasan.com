from django.conf.urls import url

from . import auth

urlpatterns = [url(r"^auth/logout$", auth.Logout.as_view(), name="logout")]

from django.conf.urls import url

from . import auth, work

urlpatterns = [
    url(r"^auth/login$", auth.Login.as_view(), name="login"),
    url(r"^auth/logout$", auth.Logout.as_view(), name="logout"),
    url(
        r"^auth/password_update$",
        auth.PasswordUpdate.as_view(),
        name="password_update",
    ),
    url(
        r"^auth/password_reset_email$",
        auth.PasswordReset.as_view(),
        name="password_reset_email",
    ),
    url(
        r"^auth/password_reset/(?P<uid>\S+)/(?P<token>\S+)$",
        auth.PasswordReset.as_view(),
        name="password_reset",
    ),
    url(r"^/works$", work.WorkList.as_view(), name="work_list"),
]

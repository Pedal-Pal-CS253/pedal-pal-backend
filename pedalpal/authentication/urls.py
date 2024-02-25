# urls.py
from django.urls import path
from .views import RegisterAPI, LoginAPI, PasswordResetAPI, PasswordResetConfirmAPI

urlpatterns = [
    path("register/", RegisterAPI.as_view(), name="Userregister"),
    path("login/", LoginAPI.as_view(), name="Userlogin"),
    path("password-reset/", PasswordResetAPI.as_view(), name="User_password_reset"),
    path(
        "password-reset/confirm/",
        PasswordResetConfirmAPI.as_view(),
        name="User_password_reset_confirm",
    ),
]

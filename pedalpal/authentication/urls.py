# urls.py
from django.urls import path
from .views import RegisterAPI, LoginAPI, change_password

urlpatterns = [
    path("register/", RegisterAPI.as_view(), name="User_register"),
    path("login/", LoginAPI.as_view(), name="User_login"),
    path("change_password/", change_password, name="change_password"),
]

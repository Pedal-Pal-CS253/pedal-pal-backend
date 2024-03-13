# urls.py
from django.urls import path
from .views import RegisterAPI, LoginAPI, SubscribeAPI, change_password, GetAuthToken

urlpatterns = [
    path("register/", RegisterAPI.as_view(), name="User_register"),
    path("login/", LoginAPI.as_view(), name="User_login"),
    path("change_password/", change_password, name="change_password"),
    path("get_auth_token/", GetAuthToken.as_view()),
    path("subscribe/", SubscribeAPI.as_view(), name="subscribe"),
]

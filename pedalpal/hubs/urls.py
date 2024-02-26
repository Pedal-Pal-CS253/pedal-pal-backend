#urls.py

from django.urls import path
from .views import ViewsAPI

urlpatterns = [
    path("view/", ViewsAPI.as_view()),
]

from django.urls import path
from booking.views import BookNowAPI
from django.urls import path
from .views import ViewsAPI


urlpatterns = [
    path("book/", BookNowAPI.as_view(), name="book"),
    path("view/", ViewsAPI.as_view()),
    ]

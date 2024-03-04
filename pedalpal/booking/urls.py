from booking.views import BookNowAPI, EndRideAPI
from django.urls import path
from .views import ViewsAPI


urlpatterns = [
    path("book/", BookNowAPI.as_view(), name="book"),
    path("view/", ViewsAPI.as_view()),
    path("end/", EndRideAPI.as_view(), name="end"),
]

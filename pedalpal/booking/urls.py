from django.urls import path
from booking.views import BookNowAPI, EndRideAPI

urlpatterns = [path("book/", BookNowAPI.as_view(), name="book"),path("end/",EndRideAPI.as_view(),name="end")]

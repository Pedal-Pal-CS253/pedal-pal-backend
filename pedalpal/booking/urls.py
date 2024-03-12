from .views import BookNowAPI, EndRideAPI, BookLaterAPI, GetHubsDataAPI
from django.urls import path


urlpatterns = [
    path("book/", BookNowAPI.as_view(), name="book"),
    path("view_hubs/", GetHubsDataAPI.as_view()),
    path("end/", EndRideAPI.as_view(), name="end"),
    path("book_later/", BookLaterAPI.as_view(), name="book_later"),
]

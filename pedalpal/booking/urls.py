from booking.views import BookNowAPI, EndRideAPI, BookLaterAPI, ViewsAPI
from django.urls import path


urlpatterns = [
    path("book/", BookNowAPI.as_view(), name="book"),
    path("view_hubs/", ViewsAPI.as_view()),
    path("end/", EndRideAPI.as_view(), name="end"),
    path("book_later/", BookLaterAPI.as_view(), name="book_later"),
]

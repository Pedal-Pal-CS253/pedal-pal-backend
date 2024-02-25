from django.urls import path
from booking.views import BookNowAPI

urlpatterns = [path("book/", BookNowAPI.as_view(), name="book")]

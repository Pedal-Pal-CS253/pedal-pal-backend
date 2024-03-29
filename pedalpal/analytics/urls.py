from django.urls import path
from analytics.views import HistoryViewAPI, UserUpdateAPI, BookingViewAPI

urlpatterns = [
    path("history/", HistoryViewAPI.as_view(), name="Ride History"),
    path("settings/", UserUpdateAPI.as_view(), name="User Settings and Profile Update"),
    path("booking_history/", BookingViewAPI.as_view(), name="Booking History"),
]

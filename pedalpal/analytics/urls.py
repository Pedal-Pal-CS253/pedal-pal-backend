from django.urls import path
from analytics.views import HistoryViewAPI, UserUpdateAPI

urlpatterns = [
    path("history/", HistoryViewAPI.as_view(), name="Ride History"),
    path("settings/", UserUpdateAPI.as_view(), name="User Settings and Profile Update"),
]

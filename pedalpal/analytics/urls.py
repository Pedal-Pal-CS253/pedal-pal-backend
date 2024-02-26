from django.urls import path
from analytics.views import HistoryViewAPI

urlpatterns = [path("history/", HistoryViewAPI.as_view(), name="Ride History")]

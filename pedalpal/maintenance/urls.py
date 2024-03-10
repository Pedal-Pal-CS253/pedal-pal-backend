from django.urls import path
from maintenance import views

urlpatterns = [
    path("feedbacks/", views.FeedbackList.as_view(), name="feedback_list"),
    path("feedbacks/add/", views.FeedbackAdd.as_view(), name="feedback_add"),
]

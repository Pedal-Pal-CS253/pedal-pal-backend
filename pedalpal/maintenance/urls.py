from django.urls import path
from maintenance import views

urlpatterns = [path("feedbacks/", views.feedback_list, name="feedback_list")]

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("logout/", views.admin_logout, name="logout"),
]

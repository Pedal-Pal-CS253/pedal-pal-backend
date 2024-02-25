from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", include("maintenance.urls")),
    path("booking/", include("booking.urls")),
    path("admin/", admin.site.urls, name="admin"),
    path("logout/", views.admin_logout, name="logout"),
    path("auth/", include("authentication.urls")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.contrib import admin
from authentication.models import Profile
from import_export.admin import ImportExportModelAdmin


@admin.register(Profile)
class Profile(ImportExportModelAdmin):
    pass
    list_display = ("first_name", "last_name", "phone")

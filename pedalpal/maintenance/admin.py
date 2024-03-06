from django.contrib import admin
from maintenance.models import Feedback
from import_export.admin import ImportExportModelAdmin


@admin.register(Feedback)
class Feedback(ImportExportModelAdmin):
    pass

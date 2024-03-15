from django.contrib import admin
from .models import Payment
from import_export.admin import ImportExportModelAdmin


@admin.register(Payment)
class Payment(ImportExportModelAdmin):
  pass
  list_display = ("user", "amount", "status", "time")

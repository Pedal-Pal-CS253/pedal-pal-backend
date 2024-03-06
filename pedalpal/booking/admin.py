from django.contrib import admin
from .models import Hub, Cycle, Ride
from import_export.admin import ImportExportModelAdmin


@admin.register(Hub)
class Hub(ImportExportModelAdmin):
    pass
    list_display = ("hub_name", "max_capacity")


@admin.register(Cycle)
class Cycle(ImportExportModelAdmin):
    list_display = ("id", "hub", "booked", "active")


@admin.register(Ride)
class Ride(ImportExportModelAdmin):
    list_display = ("cycle", "user", "start_time", "end_time", "cost")

from django.contrib import admin
from .models import Hub, Cycle, Ride, Lock, Booking
from import_export.admin import ImportExportModelAdmin

@admin.register(Hub)
class Hub(ImportExportModelAdmin):
    list_display = ("hub_name", "max_capacity")


@admin.register(Cycle)
class Cycle(ImportExportModelAdmin):
    list_display = ("id", "hub", "booked", "active")


@admin.register(Ride)
class Ride(ImportExportModelAdmin):
    list_display = ("cycle", "user", "start_time", "end_time", "cost")


@admin.register(Booking)
class Booking(ImportExportModelAdmin):
    list_display = (
        "user",
        "hub",
        "cycle",
        "book_time",
        "start_time",
        "end_time",
        "cancelled",
        "payment_id",
    )


@admin.register(Lock)
class Lock(admin.ModelAdmin):
    list_display = ("cycle", "hub")

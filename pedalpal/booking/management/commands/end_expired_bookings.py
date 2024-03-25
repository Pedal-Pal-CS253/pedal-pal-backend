from django.core.management.base import BaseCommand
from booking.utils import end_expired_bookings


class Command(BaseCommand):
    help = "Ends expired bookings"

    def handle(self, *args, **options):
        end_expired_bookings()

from django.utils import timezone
from booking.models import Booking


def end_expired_bookings():
    now = timezone.now()
    bookings = Booking.objects.filter(end_time=None)

    for booking in bookings:
        if booking.start_time < now:
            booking.end_time = now
            booking.save()
            booking.cycle.booked = False
            booking.cycle.user = None
            booking.cycle.active = False
            booking.cycle.save()

            print(f"Booking {booking.id} ended.")
        else:
            print(f"Booking {booking.id} not ended.")

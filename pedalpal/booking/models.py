from django.db import models
from authentication.models import Profile
from payment.models import Payment
import uuid


class Hub(models.Model):
    hub_id = models.UUIDField(primary_key=True)
    hub_name = models.CharField(max_length=50)
    max_capacity = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()


class Cycle(models.Model):
    cycle_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    lock = models.CharField(max_length=64)  # TODO: change later

    def is_booked(self):
        return self.status == "booked"


class Ride(models.Model):
    ride_id = models.UUIDField(primary_key=True)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cycle_id = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    start_hub = models.ForeignKey(
        Hub, related_name="%(class)s_start", on_delete=models.CASCADE
    )
    end_hub = models.ForeignKey(
        Hub, related_name="%(class)s_end", on_delete=models.CASCADE
    )
    time = models.IntegerField()  # in minutes

    payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE)


class Booking(models.Model):
    booking_id = models.UUIDField(primary_key=True)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cycle_id = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20)
    payment_id = models.ForeignKey(Payment, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.booking_id)

from django.db import models
from authentication.models import Profile
from payment.models import Payment


class Hub(models.Model):
    hub_name = models.CharField(max_length=50)
    max_capacity = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()


class Cycle(models.Model):
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True)
    booked = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    lock = models.CharField(max_length=64)  # TODO: change later

    def is_booked(self):
        return self.booked

    def is_active(self):
        return self.active

    def bookNow(self, user):
        self.booked = True
        self.active = True
        self.user = user
        self.save()


class Ride(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    start_hub = models.ForeignKey(
        Hub, related_name="%(class)s_start", on_delete=models.CASCADE
    )
    end_hub = models.ForeignKey(
        Hub,
        related_name="%(class)s_end",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    time = models.IntegerField(blank=True, null=True)  # in minutes

    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, null=True, blank=True
    )


class Booking(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20)
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return str(self.booking_id)

from django.db import models
from authentication.models import Profile
from payment.models import Payment

COST_PER_UNIT_TIME = 1


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

    def is_booked(self):
        return self.booked

    def is_active(self):
        return self.active

    def book_now(self, user):
        self.booked = True
        self.active = True
        self.user = user
        self.save()

    def book_later(self, user):
        self.booked = True
        self.active = False
        self.user = user
        self.save()


class Lock(models.Model):
    arduino_port = models.CharField(max_length=50)
    cycle = models.OneToOneField(Cycle, on_delete=models.CASCADE, null=True, blank=True)
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE)


class Ride(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    cost = models.IntegerField(default=0)
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

    payment = models.OneToOneField(
        Payment, on_delete=models.CASCADE, null=True, blank=True
    )

    def end_ride(self, end_time, lock, payment):
        self.cycle.hub = lock.hub
        self.cycle.user = None
        self.cycle.active = False
        self.cycle.booked = False
        self.end_time = end_time
        self.user.set_ride_active(False)

        self.time = (self.end_time - self.start_time).total_seconds() / 60
        self.cost = self.time * COST_PER_UNIT_TIME
        self.payment = payment

        lock.cycle = self.cycle
        self.end_hub = lock.hub
        lock.save()
        self.cycle.save()
        self.user.save()
        self.save()


class Booking(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    cycle = models.ForeignKey(Cycle, on_delete=models.CASCADE)
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE)
    book_time = models.DateTimeField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    cancelled = models.BooleanField(default=False)
    cost = models.IntegerField(default=0)
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, blank=True, null=True
    )

    def end_booking(self, end_time):
        self.end_time = end_time
        self.cancelled = False
        self.cost = (
            (self.end_time - self.start_time).total_seconds() / 60 * COST_PER_UNIT_TIME
        )
        self.save()

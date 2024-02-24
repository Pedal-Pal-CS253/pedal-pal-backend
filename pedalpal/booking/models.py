from django.db import models

# Create your models here.


class Ride(models.Model):
    # define hubs later somewhere else

    start_hub = models.CharField(max_length=20, choices=HUBS)
    start_time = models.DateTimeField()
    durarion = models.DurationField()

    end_hub = models.CharField(max_length=20, choices=HUBS)
    end_time = models.DateTimeField()


class Cycle(models.Model):
    cycle_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    hub = models.CharField(max_length=100, choice=HUBS)
    locknum = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

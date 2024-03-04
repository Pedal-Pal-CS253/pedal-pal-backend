from django.db import models
import uuid
from authentication.models import Profile


class Statistics(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.SET_NULL, null=True)
    # rides= Ride._meta.model.objects.all()\
    cost = models.DecimalField(("cost"), max_digits=100, decimal_places=2)
    rides = models.IntegerField()
    duration = models.DurationField()

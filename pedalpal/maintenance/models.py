from django.db import models
from authentication.models import Profile


class Feedback(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    air_issues = models.BooleanField()
    sound_issues = models.BooleanField()
    brake_issues = models.BooleanField()
    chain_issues = models.BooleanField()
    detailed_issues = models.TextField()

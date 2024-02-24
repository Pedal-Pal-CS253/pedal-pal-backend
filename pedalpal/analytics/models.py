from django.db import models
from django.contrib.auth.models import User
import uuid


class Wallet(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    balance = models.DecimalField(("balance"), max_digits=100, decimal_places=2)
    account_name = models.CharField(("account name"), max_length=250)
    account_number = models.CharField(("account number"), max_length=100)
    bank = models.CharField(("bank"), max_length=100)
    phone_number = models.CharField(("phone number"), max_length=15)
    password = models.CharField(("password"), max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def pay():
        pass

    def add_money():
        pass

    def _str_(self):
        return f"{self.user.username} Wallet"


class Statistics(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    # rides= Ride._meta.model.objects.all()


class Stats(models.Model):
    cost = models.DecimalField(("cost"), max_digits=100, decimal_places=2)
    rides = models.IntegerField()
    duration = models.DurationField()

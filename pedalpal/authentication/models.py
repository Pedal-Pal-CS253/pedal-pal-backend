from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class ProfileManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, phone, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone, password):
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
        )
        user.is_staff = True
        user.is_superuser = True

        user.set_password(password)
        user.save(using=self._db)
        return user


class Profile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, null=True, default="User")
    last_name = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=15)
    is_subscribed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    ride_active = models.BooleanField(default=False)
    balance = models.IntegerField(default=0)
    otp = models.CharField(max_length=6, null=True, blank=True)

    objects = ProfileManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "phone"]

    groups = models.ManyToManyField("auth.Group", related_name="profile_users")
    user_permissions = models.ManyToManyField(
        "auth.Permission", related_name="profile_users"
    )

    def is_ride_active(self):
        return self.ride_active

    def set_ride_active(self, value):
        self.ride_active = value
        self.save()

    def subscribe(self, val):
        self.is_subscribed = val
        self.save()

    def check_subscription(self):
        return self.is_subscribed

    def __str__(self):
        return self.email

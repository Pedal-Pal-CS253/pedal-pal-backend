from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_resident = models.BooleanField()
    is_subscriber = models.BooleanField()
    subscription_end = models.DateField()
    mob_no = PhoneNumberField()
    # https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-a-phone-number-in-django-models
    image = models.ImageField(default="default.jpg", upload_to="profile_pics")
    # images present in 'profile_pics' directory, follow this:
    # https://medium.com/jungletronics/a-django-blog-in-vs-code-6dee94cec9c0

    session = models.BooleanField(default="false")
    # to see if session is on or not

    HUBS = [
        ("RM", "RM"),
        ("H6", "Hall 6"),
        ("LH20", "Lecture Hall 20"),
    ]

    start_hub = models.CharField(max_length=10, choices=HUBS)

    def _str_(self):
        return f"{self.user.username} Profile"

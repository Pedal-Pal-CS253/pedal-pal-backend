from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_resident = models.BooleanField()
    is_subscriber = models.BooleanField()
    subscription_end = models.DateField()
    mob_no = PhoneNumberField()
    # https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-a-phone-number-in-django-models
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
#    images present in 'profile_pics' directory, follow this:
#   https://medium.com/jungletronics/a-django-blog-in-vs-code-6dee94cec9c0

    session = models.BooleanField(default="false")
    # to see if session is on or not
        
    HUBS = {
        "RM": "RM",
        "Hall6": "Hall6",
        "LH20": "Lecture Hall 20",
    }
    
    start_hub = models.CharField(max_length=1, choices=HUB )
        


    def __str__(self):
      return f'{self.user.username} Profile'


class wallet(models.Model):
    balance = models.IntegerField(_(""))
    
       

    

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from authentication.email import send_email


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


from django.dispatch import receiver

# from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):

    context = {
        "current_user": reset_password_token.user,
        "first_name": reset_password_token.user.first_name,
        "email": reset_password_token.user.email,
        "reset_password_url": "https://pedal-pal-backend.vercel.app/auth/password_reset/confirm/?token={}".format(
            reset_password_token.key
        ),
    }

    send_email(
        "Password Reset for {title}".format(title="PedalPal"),
        "email/password_reset_email.txt",
        context,
        [reset_password_token.user.email],
    )

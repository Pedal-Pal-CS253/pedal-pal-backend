from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse

from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):

    context = {
        "current_user": reset_password_token.user,
        "first_name": reset_password_token.user.first_name,
        "email": reset_password_token.user.email,
        "reset_password_url": "{}?token={}".format(
            instance.request.build_absolute_uri(
                reverse("password_reset:reset-password-confirm")
            ),
            reset_password_token.key,
        ),
    }

    email_plaintext_message = render_to_string(
        "email/password_reset_email.txt", context
    )

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="PedalPal"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@yourdomain.com",
        # to:
        [reset_password_token.user.email],
    )
    msg.send()

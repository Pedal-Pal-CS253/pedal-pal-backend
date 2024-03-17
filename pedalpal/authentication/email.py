from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import random
from .models import Profile


def send_email(subject, template, context, recipient_list):
    plain_message = render_to_string(template, context)
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, plain_message, from_email, recipient_list)


def send_otp_via_email(email):
    otp = random.randint(1000, 9999)
    user_obj = Profile.objects.get(email=email)
    id = user_obj.id
    user_obj.otp = otp
    user_obj.save()

    context = {
        "user": id,
        "otp": otp,
        "email": email,
        "activate_url": "https://pedal-pal-backend.vercel.app/auth/verify/{}/{}/".format(
            id, otp
        ),
    }

    send_email("OTP for PedalPal", "email/otp_email.txt", context, [email])

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email(subject, template, context, recipient_list):
    plain_message = render_to_string(template, context)
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, plain_message, from_email, recipient_list)

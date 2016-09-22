from django.conf import settings
from django.core.mail import send_mail


def send_email():
    """

    Sends emails in case something goes wrong.

    """
    send_mail("You've got some problem.", 'REPAIR IT', 'dimazarj2009@rambler.ru',
              ['dimazarj2009@rambler.ru'], fail_silently=False,)

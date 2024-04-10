# tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Deposit
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_deposit_status_email(user_email, subject, html_template, context):
    logger.info("Executing send_deposit_status_email task")
    from_email = 'alerts@bitprofitonline.com'
    to_email = [user_email]

    html_message = render_to_string(html_template, context)
    plain_message = strip_tags(html_message)

    send_mail(subject, plain_message, from_email, to_email, html_message=html_message, fail_silently=False)

@shared_task
def check_deposit_status():
    logger.info("Executing check_deposit_status task")
    from .tasks import send_deposit_status_email
    deposits = Deposit.objects.filter(Confirmed=True) | Deposit.objects.filter(not_confirmed=True)
    
    for deposit in deposits:
        subject = 'Deposit Status Update'
        context = {'user': deposit.user, 'deposit': deposit}

        if deposit.Confirmed:
            subject = 'Deposit Confirmed'
            html_template = 'deposit_confirmed_email.html'
        elif deposit.not_confirmed:
            subject = 'Deposit Failed'
            html_template = 'deposit_failed_email.html'
        else:
            html_template = 'deposit_email.html'

        send_deposit_status_email.delay(deposit.user.email, subject, html_template, context)

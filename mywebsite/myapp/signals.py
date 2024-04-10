# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from myapp.tasks import send_deposit_status_email, check_deposit_status 
from .models import Deposit

@receiver(post_save, sender=Deposit)
def deposit_status_changed(sender, instance, **kwargs):
    if instance.Confirmed or instance.not_confirmed:
        check_deposit_status.delay()

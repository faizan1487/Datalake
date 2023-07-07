from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from .models import Newsletter
from requests.exceptions import RequestException
from user.signals import usersignal

@receiver(post_save, sender=Newsletter)
def send_lead_post_request(sender, instance, created, **kwargs):
    source='Newsletter'
    newsletter = usersignal(instance,source)
        
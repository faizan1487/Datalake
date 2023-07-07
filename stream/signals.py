from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from .models import StreamUser
from requests.exceptions import RequestException
from user.signals import usersignal

@receiver(post_save, sender=StreamUser)
def send_lead_post_request(sender, instance, created, **kwargs):
    source='Stream'
    stream_user = usersignal(instance,source)
        
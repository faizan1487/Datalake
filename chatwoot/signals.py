from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from .models import ChatwoorUser
from requests.exceptions import RequestException
from user.signals import usersignal

@receiver(post_save, sender=ChatwoorUser)
def send_lead_post_request(sender, instance, created, **kwargs):
    if created:
        chatwoot_user = usersignal(instance)
        
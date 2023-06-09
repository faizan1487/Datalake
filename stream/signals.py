from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from .models import StreamUser
from requests.exceptions import RequestException
from user.signals import usersignal

@receiver(post_save, sender=StreamUser)
def send_lead_post_request(sender, instance, created, **kwargs):
    if created:
        url = 'https://crm.alnafi.com/api/resource/Lead'
        api_key = '2b4b9755ecc2dc7'
        api_secret = '8d71fb9b172e2aa'
        
        headers = {
            'Authorization': f'token {api_key}:{api_secret}',
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        stream_user = usersignal(instance,url,headers)
        
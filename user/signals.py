from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from .models import Main_User
from requests.exceptions import RequestException


@receiver(post_save, sender=Main_User)
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
        
        data = {
            "first_name": instance.first_name or None,
            "last_name": instance.last_name or None,
            "email_id": instance.email or None,
            "mobile_no": instance.phone or None,
            "country": instance.country or None,
            # Add other fields from the Main_User model to the data dictionary as needed
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            if response.status_code == 200:
                print("Lead created successfully!")
        except RequestException as e:
            print('Error occurred while making the request:', str(e))
            print('Error:', response.status_code)
            print('Error:', response.text)
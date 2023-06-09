from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from .models import Main_User, AlNafi_User, IslamicAcademy_User,PSWFormRecords
from requests.exceptions import RequestException


@receiver(post_save, sender=AlNafi_User)
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
        alnafi_user = usersignal(instance,url,headers)
        

@receiver(post_save, sender=IslamicAcademy_User)
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
        islamic_user = usersignal(instance,url,headers)


@receiver(post_save, sender=PSWFormRecords)
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
        psw_form_user = usersignal(instance,url,headers)




def usersignal(instance,url,headers):
    data = {
            "first_name": instance.first_name or None,
            "last_name": instance.last_name if hasattr(instance, 'last_name') else None,
            "email_id": instance.email or None,
            "mobile_no": instance.phone if hasattr(instance, 'phone') else None,
            "country": instance.country if hasattr(instance, 'country') else None,
            # Add other fields from the Main_User model to the data dictionary as needed
        }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        if response.status_code == 200:
            lead_data = response.json()
            # print('lead_data',lead_data)
            # print("lead_data['data']['name']",lead_data['data']['name'])
            erp_lead_id = lead_data['data']['name']
            if erp_lead_id:
                instance.erp_lead_id = erp_lead_id
                instance.save(update_fields=['erp_lead_id'])
                print("Lead created successfully!")
    except RequestException as e:
        print('Error occurred while making the request:', str(e))
        print('Error:', response.status_code)
        print('Error:', response.text)


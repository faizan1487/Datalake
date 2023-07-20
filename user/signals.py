from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import requests
from .models import AlNafi_User, IslamicAcademy_User,PSWFormRecords
from user.constants import COUNTRY_CODES
from newsletter.signals import send_lead_post_request
import environ

env = environ.Env()
env.read_env()
DEBUG = env('DEBUG',cast=bool)

@receiver(post_save, sender=AlNafi_User)
def send_alnafi_lead_post_request(sender, instance, **kwargs):
    print("signal running")
    source='Alnafi'
    alnafi_user = usersignal(instance,source,sender)    

@receiver(post_save, sender=IslamicAcademy_User)
def send_islamic_lead_post_request(sender, instance, **kwargs):
    # print("islamic user signal")
    source='Islamic Academy'
    islamic_user = usersignal(instance,source,sender)


@receiver(post_save, sender=PSWFormRecords)
def send_psw_lead_post_request(sender, instance, **kwargs):
    source='PSWFormRecords'
    psw_form_user = usersignal(instance,source,sender)



def usersignal(instance,source,sender):
    post_save.disconnect(send_alnafi_lead_post_request, sender=AlNafi_User)
    post_save.disconnect(send_islamic_lead_post_request, sender=IslamicAcademy_User)
    post_save.disconnect(send_psw_lead_post_request, sender=PSWFormRecords)

    if DEBUG:
        api_key = '2768f34bb4bb7f7'
        api_secret = '21754cee8dc0f42'
        url = f'http://3.142.247.16/api/resource/Lead?fields=["name","email_id"]&filters=[["Lead","email_id","=","{instance.email}"]]'
    else:
        api_key = '2b4b9755ecc2dc7'
        api_secret = '8d71fb9b172e2aa'
        url = f'https://crm.alnafi.com/api/resource/Lead?fields=["name","email_id"]&filters=[["Lead","email_id","=","{instance.email}"]]'
    
    headers = {
        'Authorization': f'token {api_key}:{api_secret}',
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    country_code = getattr(instance, 'country', "Unknown")
    country_name = None

    if country_code:
        for name, code in COUNTRY_CODES.items():
            if code == country_code:
                country_name = name
                break

    data = {
            "first_name": instance.first_name or None,
            "last_name": instance.last_name if hasattr(instance, 'last_name') else None,
            "email_id": instance.email or None,
            "mobile_no": instance.phone if hasattr(instance, 'phone') else None,
            "country": country_name,
            "source": source
            # Add other fields from the Main_User model to the data dictionary as needed
        }
    


    response = requests.get(url, headers=headers)
    lead_data = response.json()
    
    already_existed = len(lead_data["data"]) > 0

    if already_existed:
        lead_id = lead_data['data'][0]['name']
        if DEBUG:
            url = f'http://3.142.247.16/api/resource/Lead/{lead_id}'
        else:
            url = f'https://crm.alnafi.com/api/resource/Lead/{lead_id}'

        response = requests.put(url, headers=headers, json=data)
        instance.erp_lead_id = lead_data['data'][0]['name']
        # print("lead updated")
        instance.save(update_fields=['erp_lead_id'])
    else:
        if DEBUG:
            url = 'http://3.142.247.16/api/resource/Lead'
        else:
            url = 'https://crm.alnafi.com/api/resource/Lead'

        response = requests.post(url, headers=headers, json=data)
        print("response.status_code",response.text)
        response.raise_for_status()
        # print("response.status_code",response.status_code)
        if response.status_code == 200:
            lead_data = response.json()
            erp_lead_id = lead_data['data']['name']
            if erp_lead_id:
                # print("lead id exists")
                instance.erp_lead_id = erp_lead_id
                instance.save(update_fields=['erp_lead_id'])
                # print("Lead created successfully!")

    post_save.connect(send_islamic_lead_post_request, sender=IslamicAcademy_User)
    post_save.connect(send_psw_lead_post_request, sender=PSWFormRecords)
    post_save.connect(send_alnafi_lead_post_request, sender=AlNafi_User)
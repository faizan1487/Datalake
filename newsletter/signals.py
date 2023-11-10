from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from .models import Newsletter
from requests.exceptions import RequestException
from user.constants import COUNTRY_CODES
import environ
from secrets_api.algorithem import round_robin

env = environ.Env()
env.read_env()

@receiver(post_save, sender=Newsletter)
def send_lead_post_request(sender, instance, created, **kwargs):
    source= instance.source
    newsletter = usersignal(instance,source)        


def usersignal(instance,source):
    print("instance.source",instance.source)
    if instance.source == 'Academy Newsletter':
        user_api_key = '2a1d467717681df'
        user_secret_key = '39faa082ac5f258'
    else:
        user_api_key, user_secret_key = round_robin()


    
    headers = {
        'Authorization': f'token {user_api_key}:{user_secret_key}',
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
    url = f'https://crm.alnafi.com/api/resource/Lead?fields=["name","email_id"]&filters=[["Lead","email_id","=","{instance.email}"]]'
    response = requests.get(url, headers=headers)
    lead_data = response.json()
    # print(response.status_code)

    if response.status_code == 403:
        return
    # print(lead_data['data'])
    # print(lead_data)
    if 'data' in lead_data:
        already_existed = len(lead_data["data"]) > 0
    else:
        already_existed = False
    # print(already_existed)
    if already_existed:
        response = requests.put(url, headers=headers, json=data)
        # print(response.status_code)
        # print(response.json())
        instance.erp_lead_id = lead_data['data'][0]['name']
        # print("lead updated")
        instance.save(update_fields=['erp_lead_id'])
    else:
        # print("in else")
        post_url = 'https://crm.alnafi.com/api/resource/Lead'
        response = requests.post(post_url, headers=headers, json=data)
        
        if response.status_code == 200:
            lead_data = response.json()
            erp_lead_id = lead_data['data']['name']
            if erp_lead_id:
                # print("lead id exists")
                instance.erp_lead_id = erp_lead_id
                # instance.save(update_fields=['erp_lead_id'])
                # print("Lead created successfully!")
        else:
            print(response.status_code)
            print(response.json())
    return
    # post_save.connect(send_lead_post_request, sender=Newsletter)
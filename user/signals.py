from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import requests
from .models import AlNafi_User, IslamicAcademy_User,PSWFormRecords, Moc_Leads,New_AlNafi_User
from user.constants import COUNTRY_CODES
from newsletter.signals import send_lead_post_request
import environ
from secrets_api.algorithem import round_robin
from albaseer.settings import DEBUG
env = environ.Env()
env.read_env()
api_key = env("FRAPPE_API_KEY")
api_secret = env("FRAPPE_API_SECRET")
DEBUG = env('DEBUG',cast=bool)

@receiver(post_save, sender=AlNafi_User)
def send_alnafi_lead_post_request(sender, instance, **kwargs):
    # print("signal running")
    source='Alnafi'
    alnafi_user = usersignal(instance,source,sender)    

@receiver(post_save, sender=IslamicAcademy_User)
def send_islamic_lead_post_request(sender, instance, **kwargs):

    print("islamic user signal")
    source='IslamicAcademy'
    islamic_user = usersignal(instance,source,sender)


@receiver(post_save, sender=PSWFormRecords)
def send_psw_lead_post_request(sender, instance, **kwargs):

    print("psw user signal")
    source='PSWFormRecords'
    psw_form_user = usersignal(instance,source,sender)

@receiver(post_save, sender=New_AlNafi_User)
def send_alnafi_new_request(sender, instance, **kwargs):

    source='NewAlnafiSignup'
    psw_form_user = newsignupsignal(instance,source,sender)


def usersignal(instance,source,sender):
    # post_save.disconnect(send_alnafi_lead_post_request, sender=AlNafi_User)
    # post_save.disconnect(send_islamic_lead_post_request, sender=IslamicAcademy_User)
    # post_save.disconnect(send_psw_lead_post_request, sender=PSWFormRecords)

    # try:
        # if DEBUG:
        #     api_key = '2768f34bb4bb7f7'
        #     api_secret = '21754cee8dc0f42'
        #     url = f'http://3.142.247.16/api/resource/Lead?fields=["name","email_id"]&filters=[["Lead","email_id","=","{instance.email}"]]'
        # else:

    url = f'https://crm.alnafi.com/api/resource/Lead?fields=["name","email_id"]&filters=[["Lead","email_id","=","{instance.email}"]]'
    # url = f'http://18.190.1.109/api/resource/Lead?fields=["name","email_id"]&filters=[["Lead","email_id","=","{instance.email}"]]'
    
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
    
    response = requests.get(url, headers=headers)
    lead_data = response.json()
    # print(lead_data)
    already_existed = len(lead_data["data"]) > 0

    if already_existed:
        lead_id = lead_data['data'][0]['name']
        # if DEBUG:
        #     url = f'http://3.142.247.16/api/resource/Lead/{lead_id}'
        # else:
        url = f'https://crm.alnafi.com/api/resource/Lead/{lead_id}'
        # url = f'http://18.190.1.109/api/api/resource/Lead/{lead_id}'
        # print(data)
        response = requests.put(url, headers=headers, json=data)
        instance.erp_lead_id = lead_data['data'][0]['name']
        # print("lead updated")
        # instance.save(update_fields=['erp_lead_id'])
    else:
            # if DEBUG:
            #     url = 'http://3.142.247.16/api/resource/Lead'
            # else:
            url = 'https://crm.alnafi.com/api/resource/Lead'
            # url = 'http://18.190.1.109/api/resource/Lead'
            # print(headers)
            lead_data = response.json()
            # print(lead_data)
            response = requests.post(url, headers=headers, json=data)
            # print("response.status_code",response.text)
            response.raise_for_status()
            # print("response.status_code",response.status_code)
            if response.status_code == 200:
                lead_data = response.json()
                # print(lead_data)
                erp_lead_id = lead_data['data']['name']
                if erp_lead_id:
                    # print("lead id exists")
                    instance.erp_lead_id = erp_lead_id
                    # instance.save(update_fields=['erp_lead_id'])
                    # print("Lead created successfully!")
    # except:
    # post_save.connect(send_islamic_lead_post_request, sender=IslamicAcademy_User)
    # post_save.connect(send_psw_lead_post_request, sender=PSWFormRecords)
    # post_save.connect(send_alnafi_lead_post_request, sender=AlNafi_User)

#############################################################
@receiver(post_save, sender=Moc_Leads)
def handle_lead_post_request(sender, instance, created, **kwargs):
    # return
    source=instance.source
    Moc_Leads = mocLeadsSignal(instance,source)   

def mocLeadsSignal(instance,source):
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
            "first_name": instance.full_name or None,
            "last_name": None,
            "email_id": instance.email or None,
            "mobile_no": instance.phone if hasattr(instance, 'phone') else None,
            "country": country_name,
            "source": source
            # Add other fields from the Main_User model to the data dictionary as needed
        }
    url = f'https://crm.alnafi.com/api/resource/Lead?fields=["name","email_id"]&filters=[["Lead","email_id","=","{instance.email}"]]'
    response = requests.get(url, headers=headers)
    lead_data = response.json()
    print(response.status_code)
    # print(lead_data['data'])
    print(lead_data)
    if response.status_code == 403:
        return
    # print(lead_data['data'])
    print(lead_data)
    if 'data' not in lead_data:
        already_existed = len(lead_data["data"]) > 0
    else:
        already_existed = False

   
    already_existed = len(lead_data["data"]) > 0
    # print(already_existed)
    if already_existed:
        response = requests.put(url, headers=headers, json=data)
        print(response.status_code)
        print(response.json())
        instance.erp_lead_id = lead_data['data'][0]['name']
        print("lead updated")
    else:
        print("in else")
        post_url = 'https://crm.alnafi.com/api/resource/Lead'
        response = requests.post(post_url, headers=headers, json=data)
        print(response.status_code)
        print(response.json())
        # response.raise_for_status()
        # print("response.status_code",response.status_code)
        if response.status_code == 200:
            lead_data = response.json()
            erp_lead_id = lead_data['data']['name']
            if erp_lead_id:
                print("lead id exists")
                instance.erp_lead_id = erp_lead_id
                print("Lead created successfully!")


def newsignupsignal(instance,source,sender):


    url = f'https://crm.alnafi.com/api/resource/Lead?fields=["name","email_id"]&filters=[["Lead","email_id","=","{instance.email}"]]'
    
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
            "first_name": instance.full_name or None,
            "last_name": None,
            "email_id": instance.email or None,
            "mobile_no": instance.phone if hasattr(instance, 'phone') else None,
            "country": country_name,
            "source": source
            # Add other fields from the Main_User model to the data dictionary as needed
        }
    
    response = requests.get(url, headers=headers)
    lead_data = response.json()
    # print(lead_data)
    already_existed = len(lead_data["data"]) > 0

    if already_existed:
        lead_id = lead_data['data'][0]['name']
        # if DEBUG:
        #     url = f'http://3.142.247.16/api/resource/Lead/{lead_id}'
        # else:
        url = f'https://crm.alnafi.com/api/resource/Lead/{lead_id}'
        # print(data)
        response = requests.put(url, headers=headers, json=data)
        instance.erp_lead_id = lead_data['data'][0]['name']
    else:
        # if DEBUG:
        #     url = 'http://3.142.247.16/api/resource/Lead'
        # else:
        url = 'https://crm.alnafi.com/api/resource/Lead'
        # url = 'http://18.190.1.109/api/resource/Lead'
        lead_data = response.json()
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        if response.status_code == 200:
            lead_data = response.json()
            erp_lead_id = lead_data['data']['name']
            if erp_lead_id:
                instance.erp_lead_id = erp_lead_id
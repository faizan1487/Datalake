from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import requests
from .models import Main_User, AlNafi_User, IslamicAcademy_User,PSWFormRecords
from requests.exceptions import RequestException


@receiver(post_save, sender=AlNafi_User)
def send_alnafi_lead_post_request(sender, instance, **kwargs):
    print("signal running")
    alnafi_user = usersignal(instance)    

@receiver(post_save, sender=IslamicAcademy_User)
def send_islamic_lead_post_request(sender, instance, created, **kwargs):
    # print("islamic user signal")
    if created:
        islamic_user = usersignal(instance)


@receiver(post_save, sender=PSWFormRecords)
def send_psw_lead_post_request(sender, instance, created, **kwargs):
    if created:
        psw_form_user = usersignal(instance)




def usersignal(instance):
    # Disconnect the signal temporarily
    post_save.disconnect(send_alnafi_lead_post_request, sender=AlNafi_User)
    url = 'https://crm.alnafi.com/api/resource/Lead'
    api_key = '2b4b9755ecc2dc7'
    api_secret = '8d71fb9b172e2aa'
    headers = {
        'Authorization': f'token {api_key}:{api_secret}',
        "Content-Type": "application/json",
        "Accept": "application/json",
    }    
    print("instance.country",instance.country)
    data = {
            "first_name": instance.first_name or None,
            "last_name": instance.last_name if hasattr(instance, 'last_name') else None,
            "email_id": instance.email or None,
            "mobile_no": instance.phone if hasattr(instance, 'phone') else None,
            "country": instance.country if hasattr(instance, 'country') else None,
            # Add other fields from the Main_User model to the data dictionary as needed
        }
    
    
    response = requests.get(url, headers=headers)
    lead_data = response.json()
    print(lead_data)
    lead_emails = [lead['name'] for lead in lead_data['data']]
    # print(len(lead_emails))
    try:
        if instance.email in lead_emails:
            response = requests.put(url, headers=headers, json=data)
            if response.status_code == 200:
                erp_lead_id = None
                for lead in lead_data['data']:
                    if lead['email_id'] == instance.email:
                        erp_lead_id = lead['name']
                        break

                # print("erp_lead_id",erp_lead_id)
                if erp_lead_id:
                    instance.erp_lead_id = erp_lead_id
                    instance.save(update_fields=['erp_lead_id'])
                    print("Lead created successfully!")
                    post_save.connect(send_alnafi_lead_post_request, sender=AlNafi_User)
                    return
        else:
            response = requests.post(url, headers=headers, json=data)

        response.raise_for_status()
        print("response.status_code",response.status_code)
        if response.status_code == 200:
            lead_data = response.json()
            erp_lead_id = lead_data['data']['name']
            if erp_lead_id:
                instance.erp_lead_id = erp_lead_id
                instance.save(update_fields=['erp_lead_id'])
                print("Lead created successfully!")
                post_save.connect(send_alnafi_lead_post_request, sender=AlNafi_User)
    except Exception as e:
        print('Error occurred while making the request:', str(e))
        # print('Error:', response.status_code)
        # print('Error:', response.text)
        print('Error:', response.status_code)
        print('Error:', response.text)
        # Reconnect the signal
        print("reconnect the signal")
        post_save.connect(send_alnafi_lead_post_request, sender=AlNafi_User)

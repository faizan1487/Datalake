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
    # api_key = '2b4b9755ecc2dc7'
    # api_secret = '8d71fb9b172e2aa'
    # headers = {
    #     'Authorization': f'token {api_key}:{api_secret}',
    #     "Content-Type": "application/json",
    #     "Accept": "application/json",
    # }    
    data = {
            "first_name": instance.first_name or None,
            "last_name": instance.last_name if hasattr(instance, 'last_name') else None,
            "email_id": instance.email or None,
            "mobile_no": instance.phone if hasattr(instance, 'phone') else None,
            "country": instance.country if hasattr(instance, 'country') else None,
            # Add other fields from the Main_User model to the data dictionary as needed
        }
    
    stage_api_key = '5c7de9468c72e9d'
    stage_api_secret = '7137b385a03daa0'
    stage_headers = {
        'Authorization': f'token {stage_api_key}:{stage_api_secret}',
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    stage_lead_url = 'http://13.59.168.46/api/resource/Lead?fields=["email_id", "name"]'
    
    response = requests.get(stage_lead_url, headers=stage_headers)
    lead_data = response.json()
    
    lead_emails = [lead['email_id'] for lead in lead_data['data']]
    # print(len(lead_emails))
    stage_lead_url = 'http://13.59.168.46/api/resource/Lead'
    try:
        if instance.email in lead_emails:
            # response = requests.put(url, headers=stage_headers, json=data)
            # print("put request")
            stage_response = requests.put(stage_lead_url, headers=stage_headers, json=data)
            if stage_response.status_code == 200:
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
            # response = requests.post(stage_lead_url, headers=stage_headers, json=data)
            stage_response = requests.post(stage_lead_url, headers=stage_headers, json=data)

        stage_response.raise_for_status()
        # response.raise_for_status()
        print("stage_response.status_code",stage_response.status_code)
        if stage_response.status_code == 200:
            # response.status_code & 
            # lead_data = response.json()
            stage_lead_data = stage_response.json()
            # print(stage_lead_data)
            # print('lead_data',lead_data)
            # print("lead_data['data']['name']",lead_data['data']['name'])
            erp_lead_id = stage_lead_data['data']['name']
            if erp_lead_id:
                instance.erp_lead_id = erp_lead_id
                instance.save(update_fields=['erp_lead_id'])
                print("Lead created successfully!")
                post_save.connect(send_alnafi_lead_post_request, sender=AlNafi_User)
    except Exception as e:
        print('Error occurred while making the request:', str(e))
        # print('Error:', response.status_code)
        # print('Error:', response.text)
        print('Error:', stage_response.status_code)
        print('Error:', stage_response.text)
        # Reconnect the signal
        print("reconnect the signal")
        post_save.connect(send_alnafi_lead_post_request, sender=AlNafi_User)

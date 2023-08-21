from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from .models import AffiliateUser
from requests.exceptions import RequestException
from user.constants import COUNTRY_CODES

# @receiver(post_save, sender=AffiliateUser)
def send_lead_post_request(sender, instance, created, **kwargs):
    source='Affiliate'
    affiliate_user = usersignal(instance,source)

def usersignal(instance,source):
    # Disconnect the post_save signal temporarily to avoid recursive calls
    post_save.disconnect(send_lead_post_request, sender=AffiliateUser)

    # Set API key and secret for authentication
    api_key = '2b4b9755ecc2dc7'
    api_secret = '8d71fb9b172e2aa'
    # Prepare headers for the API request
    headers = {
        'Authorization': f'token {api_key}:{api_secret}',
        "Content-Type": "application/json",
        "Accept": "application/json",
    }    
     # Get country details from the instance
    country_code = getattr(instance, 'country', "Unknown")
    country_name = None

    if country_code:
        for name, code in COUNTRY_CODES.items():
            if code == country_code:
                country_name = name
                break

    # Prepare data for sending to the API
    data = {
            "first_name": instance.first_name or None,
            "last_name": instance.last_name if hasattr(instance, 'last_name') else None,
            "email_id": instance.email or None,
            "mobile_no": instance.phone if hasattr(instance, 'phone') else None,
            "country": country_name,
            "source": source
            # Add other fields from the Main_User model to the data dictionary as needed
        }
    
    # Prepare the URL for querying existing leads by email
    url = f'https://crm.alnafi.com/api/resource/Lead?fields=["name","email_id"]&filters=[["Lead","email_id","=","{instance.email}"]]'
    # Query the CRM API to check if the lead already exists
    response = requests.get(url, headers=headers)
    lead_data = response.json()
    # print(lead_data['data'])
    
    already_existed = len(lead_data["data"]) > 0
    # print(already_existed)
    if already_existed:
        # If the lead exists, update it with new data
        response = requests.put(url, headers=headers, json=data)
        instance.erp_lead_id = lead_data['data'][0]['name']
        # print("lead updated")
        instance.save(update_fields=['erp_lead_id'])
    else:
        # If the lead doesn't exist, create a new one
        # print("in else")
        post_url = 'https://crm.alnafi.com/api/resource/Lead'
        response = requests.post(post_url, headers=headers, json=data)
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
    
    # Reconnect the post_save signal after processing
    post_save.connect(send_lead_post_request, sender=AffiliateUser)
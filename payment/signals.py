from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from .models import Main_Payment
from rest_framework.response import Response
from requests.exceptions import RequestException

@receiver(post_save, sender=Main_Payment)
def send_payment_post_request(sender, instance, created, **kwargs):
    if created:
        url = 'https://crm.alnafi.com/api/resource/Customer'
        api_key = '2b4b9755ecc2dc7'
        api_secret = '8d71fb9b172e2aa'
        headers = {
            'Authorization': f'token {api_key}:{api_secret}',
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            for i in range(len(data['data'])):
                first_name = instance.user.first_name if instance.user.first_name else ''
                last_name = instance.user.last_name if instance.user.last_name else ''
                full_name = f'{first_name} {last_name}'.strip()
                if data['data'][i]['name'] == full_name:
                    payment = create_payment(instance,headers)
                    break
            else:
                lead_url = 'https://crm.alnafi.com/api/resource/Lead'
                response = requests.get(lead_url, headers=headers)

                lead_data = response.json()
                print(lead_data)
                for i in range(len(lead_data['data'])):
                    if lead_data['data'][i]['name'] == instance.user.erp_lead_id:
                        #createe customer with lead id
                        customer = create_customer(instance,headers,full_name)
                        #then create payment from that customer
                        payment = create_payment(instance,headers)
                        break
                else:
                    #create lead
                    lead = create_lead(instance)
                    #then create customer from that lead
                    customer = create_customer(instance,headers,full_name)
                    #then create payment from that customer
                    payment = create_payment(instance,headers)
        except RequestException as e:
            print('Error occurred while making the request:', str(e))
            print('Error:', response.status_code)
            print('Error:', response.text) 
    else:
        pass

def create_lead(instance):
    lead_url = 'https://crm.alnafi.com/api/resource/Lead'
    api_key = '2b4b9755ecc2dc7'
    api_secret = '8d71fb9b172e2aa'
    
    headers = {
        'Authorization': f'token {api_key}:{api_secret}',
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    
    lead_data = {
        "first_name": instance.user.first_name or None,
        "last_name": instance.user.last_name or None,
        "email_id": instance.user.email or None,
        "mobile_no": instance.user.phone or None,
        "country": instance.user.country or None,
        # Add other fields from the Main_User model to the data dictionary as needed
    }
    try:
        response = requests.post(lead_url, headers=headers, json=lead_data)
        response.raise_for_status()
        if response.status_code == 200:
            lead_data = response.json()
            # print('lead_data',lead_data)
            # print("lead_data['data']['name']",lead_data['data']['name'])
            erp_lead_id = lead_data['data']['name']
            if erp_lead_id:
                instance.user.erp_lead_id = erp_lead_id
                instance.user.save(update_fields=['erp_lead_id'])
                print("Lead created successfully!")
    except RequestException as e:
        print('Error occurred while making the request:', str(e))
        print('Error:', response.status_code)
        print('Error:', response.text)


def create_customer(instance,headers,full_name):
    customer_url = 'https://crm.alnafi.com/api/resource/Customer'
    api_key = '2b4b9755ecc2dc7'
    api_secret = '8d71fb9b172e2aa'

    customer_data = {
        "customer_name": full_name or None,
        "customer_type": "Individual",
        "customer_group": "Commercial",
        "territory": instance.user.country or "Unknown",
        "lead_name": instance.user.erp_lead_id,
    }

    response = requests.post(customer_url, headers=headers, json=customer_data)
    if response.status_code == 200:
        print("Customer created successfully!")


def create_payment(instance,headers):
    url = 'https://crm.alnafi.com/api/resource/Payment Entry'
        
    first_name = instance.user.first_name if instance.user.first_name else ''
    last_name = instance.user.last_name if instance.user.last_name else ''
    full_name = f'{first_name} {last_name}'.strip()
    data1 = {
        "payment_type": "Receive",
        "mode_of_payment": instance.source or "Unknown",
        "party_type": "Customer",
        "party": full_name,
        "party_name": full_name,
        "paid_to": "Cash - A",
        "paid_amount": instance.amount,
        "received_amount": instance.amount,
    }
    try:
        response = requests.post(url, headers=headers, json=data1)
        response.raise_for_status() 
        if response.status_code == 200:
            print("Payment created successfully!")     
    except RequestException as e:
        print('Error occurred while creating payment:', str(e)) 
        print('Error:', response.status_code)
        print('Error:', response.text)
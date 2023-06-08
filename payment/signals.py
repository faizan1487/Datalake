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
                url = 'https://crm.alnafi.com/api/resource/Customer'
                api_key = '2b4b9755ecc2dc7'
                api_secret = '8d71fb9b172e2aa'

                #Customer data
                customer_data = {
                    "customer_name": full_name or "Unknown",
                    "customer_type": "Individual",
                    "customer_group": "Commercial",
                    "territory": instance.user.country or "Unknown",
                }

                response = requests.post(url, headers=headers, json=customer_data)
                if response.status_code == 200:
                    print("Customer created successfully!")
                else:
                    print('Error:', response.status_code)
                    print('Error:', response.text)  
                                
                payment = create_payment(instance,headers)
        except RequestException as e:
            print('Error occurred while making the request:', str(e))
    else:
        pass


def create_payment(instance,headers):
    url = 'https://crm.alnafi.com/api/resource/Payment Entry'
        
    first_name = instance.user.first_name if instance.user.first_name else ''
    last_name = instance.user.last_name if instance.user.last_name else ''
    full_name = f'{first_name} {last_name}'.strip()
    data1 = {
        "payment_type": "Receive",
        "mode_of_payment": instance.source or "Unknown",
        "party_type": "Customer",
        "party": full_name or "unknown",
        "party_name": full_name or "unknown",
        "paid_to": "Cash - A",
        "paid_amount": instance.amount or "unknown",
        "received_amount": instance.amount or "unknown",
    }
    try:
        response = requests.post(url, headers=headers, json=data1)
        response.raise_for_status() 
        if response.status_code == 200:
            print("Payment created successfully!")
        else:
            print('Error:', response.status_code)
            print('Error:', response.text)      
    except RequestException as e:
        print('Error occurred while creating payment:', str(e))          
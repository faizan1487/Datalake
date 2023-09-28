from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import requests
from .models import AlNafi_Payment,UBL_IPG_Payment,UBL_Manual_Payment,Stripe_Payment,Easypaisa_Payment
from rest_framework.response import Response
from requests.exceptions import RequestException
from user.models import Main_User
from django.core.cache import cache
from django.conf import settings
import json
from datetime import datetime
from user.constants import COUNTRY_CODES
import environ
from secrets_api.algorithem import round_robin_support

env = environ.Env()
env.read_env()
# api_key = env("FRAPPE_API_KEY")
# api_secret = env("FRAPPE_API_SECRET")
DEBUG = env('DEBUG',cast=bool)

@receiver(pre_save, sender=AlNafi_Payment)
def send_payment_post_request(sender, instance, **kwargs):
    # print("signal running")
    url = 'https://crm.alnafi.com/api/resource/Suppport?limit_start=0&limit_page_length=5000&fields=["*"]'
    api_key, api_secret = round_robin_support()
    api_key = '351b6479c5a4a16'
    api_secret = 'e459db7e2d30b34'
  
    headers = {
        'Authorization': f'token {api_key}:{api_secret}',
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    try:
        print("in try")
        response = requests.get(url, headers=headers)
        # response.raise_for_status()
        data = response.json()
        print(response.text)
        payment_user = Main_User.objects.filter(email__iexact=instance.customer_email)
        print(payment_user)
        print(data)
        # print(len(data['data']))
        if not payment_user:
            return
        for i in range(len(data['data'])):
            print("in for")
            # print(payment_user)
            first_name = payment_user[0].first_name if payment_user[0].first_name else ''
            last_name = payment_user[0].last_name if payment_user[0].last_name else ''
            full_name = f'{first_name} {last_name}'.strip()
            # print("full name", full_name)
            # uncomment this check condition for customer
            if data['data'][i]['customer_email'] == instance.customer_email:
                print("customer exists")
                customer_id = data['data'][i]['name']
                # print(customer_id)
                # if DEBUG:
                #     url = f'https://stage-erp.alnafi.com/api/resource/Suppport/{customer_id}'
                # else:
                url = f'https://crm.alnafi.com/api/resource/Suppport/{customer_id}'
                # url = f'http://18.190.1.109/api/api/resource/Lead/{lead_id}'

                
                current_date = datetime.now().date()
                if instance.expiration_datetime and instance.expiration_datetime.date() >= current_date:
                    expiration_status = 'Active'
                else:
                    expiration_status = 'Expired'

                customer_data = {
                    "full_name": full_name or None,
                    "contact_no": payment_user[0].phone or None,
                    "customer_email": payment_user[0].email or None,
                    "country": payment_user[0].country or None,
                    "product_name": instance.product_name or None,
                    "price_pkr": instance.amount_pkr or None,
                    "price_usd": instance.amount_usd or None,
                    "payment_source": instance.source.capitalize() if instance.source else None,
                    "payment_date": instance.order_datetime.isoformat() if instance.order_datetime else None,
                    "expiration_date": instance.expiration_datetime.isoformat() if instance.expiration_datetime else None,
                    "expiration_status": expiration_status,
                }
                # print(customer_data)
                response = requests.put(url, headers=headers, json=customer_data)
                # print(response)
                print(response.text)
                instance.customer_email = data['data'][i]['customer_email']
                print("lead updated")
                break
        else:
            first_name = payment_user[0].first_name if payment_user[0].first_name else ''
            last_name = payment_user[0].last_name if payment_user[0].last_name else ''
            full_name = f'{first_name} {last_name}'.strip()
            customer = create_customer(instance,headers,full_name,payment_user)


    except RequestException as e:
        print("in except")
        print('Error occurred while making the request:', str(e))
        print('Error:', response.status_code)
        print('Error:', response.text) 
     
  

def create_customer(instance,headers,full_name,payment_user):
    customer_url = 'https://crm.alnafi.com/api/resource/Suppport'
    # print("payment_user",payment_user)
    # print("payment_user[0].erp_lead_id",payment_user[0].erp_lead_id)
    country_code = payment_user[0].country or None
    country_name = None

    if country_code:
        for name, code in COUNTRY_CODES.items():
            if code == country_code:
                country_name = name
                break

    
    current_date = datetime.now().date()
    if instance.expiration_datetime and instance.expiration_datetime.date() >= current_date:
        expiration_status = 'Active'
    else:
        expiration_status = 'Expired'

    customer_data = {
        "full_name": full_name or None,
        "contact_no": payment_user[0].phone or None,
        "customer_email": payment_user[0].email or None,
        "country": payment_user[0].country or None,
        "product_name": instance.product_name or None,
        "price_pkr": instance.amount_pkr or None,
        "price_usd": instance.amount_usd or None,
        "payment_source": instance.source.capitalize() if instance.source else None,
        "payment_date": instance.order_datetime.isoformat() if instance.order_datetime else None,
        "expiration_date": instance.expiration_datetime.isoformat() if instance.expiration_datetime else None,
        "expiration_status": expiration_status,
    }

    response = requests.post(customer_url, headers=headers, json=customer_data)
    # print(response)
    print(response.text)
    if response.status_code == 200:
        lead_data = response.json()
        print(lead_data)
        customer_email = lead_data['data']['customer_email']
        if customer_email:
            # print("lead id exists")
            instance.customer_email = customer_email
            print("Lead created successfully!")




def get_USD_rate():
    usd_details = cache.get("usd_details")
    if usd_details:
        # print(usd_details)
        # print("usd_details", usd_details["PKR"])
        return json.loads(usd_details)
    usd_details = {}
    url = f"https://v6.exchangerate-api.com/v6/{settings.EXCHANGE_RATE_API_KEY}/latest/USD"
    response = requests.get(url).json()
    usd_details["PKR"] = response["conversion_rates"]["PKR"]
    usd_details["USD"] = response["conversion_rates"]["USD"]

    cache.set("usd_details", json.dumps(usd_details), 60*120)
    # print("usd_details",usd_details)
    return usd_details
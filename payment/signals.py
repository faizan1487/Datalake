from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import requests
from .models import AlNafi_Payment,New_Alnafi_Payments
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
from threading import Thread
from threading import Timer

env = environ.Env()
env.read_env()
# api_key = env("FRAPPE_API_KEY")
# api_secret = env("FRAPPE_API_SECRET")
DEBUG = env('DEBUG',cast=bool)



@receiver(pre_save, sender=New_Alnafi_Payments)
def new_alnafi_payment_signal_support(sender, instance: New_Alnafi_Payments, *args, **kwargs):
    print("new alnafi signal running")
    model_name = 'new_alnafi'
    Thread(target=send_payment_support_module, args=(instance,model_name,)).start()
    # data = send_payment_support_module(instance,model_name)


@receiver(pre_save, sender=AlNafi_Payment)
def alnafi_payment_signal_support(sender, instance: AlNafi_Payment, *args, **kwargs):
    print("alnafi signal running")
    model_name = 'alnafi'
    Thread(target=send_payment_support_module, args=(instance,model_name,)).start()


@receiver(pre_save, sender=New_Alnafi_Payments)
def new_alnafi_payment_signal_sales(sender, instance: New_Alnafi_Payments, *args, **kwargs):
    print("new alnafi signal running for sales")
    Thread(target=change_lead_status_sales_module, args=(instance,)).start()
    # data = send_payment_support_module(instance,model_name)


@receiver(pre_save, sender=AlNafi_Payment)
def alnafi_payment_signal_sales(sender, instance: AlNafi_Payment, *args, **kwargs):
    print("alnafi signal running for sales")
    Thread(target=change_lead_status_sales_module, args=(instance,)).start()


def send_payment_support_module(instance,model_name, **kwargs):
    print("signal FUNCTION running")
    # print("model_name", model_name)
    url = 'https://crm.alnafi.com/api/resource/Suppport?limit_start=0&limit_page_length=5000&fields=["*"]'
    api_key, api_secret = round_robin_support()
  
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
        # print(response.text)
        payment_user = Main_User.objects.filter(email__iexact=instance.customer_email)
        # print(payment_user)
        # print(data)
        # print(len(data['data']))
        if not payment_user:
            return
        for i in range(len(data['data'])):
            pass
            # print("in for")
            # print(payment_user)
            # if data['data'][i]['customer_email'] == instance.customer_email:
                # print(model_name)
                # if model_name == 'alnafi':
                #     print("in if")
                #     customer_data = alnafi_payment_support_data(instance,payment_user)
                # else:
                #     print("in else")
                #     customer_data = new_alnafi_payment_support_data(instance, payment_user)

                # customer_id = data['data'][i]['name']
                # url = f'https://crm.alnafi.com/api/resource/Suppport/{customer_id}'
                # print(customer_data)
                # response = requests.put(url, headers=headers, json=customer_data)
                # print(response)
                # print(response.text)
                # instance.customer_email = data['data'][i]['customer_email']
                # print("lead updated")
                # break
        else:
            # customer_data = alnafi_payment_support_data(instance,payment_user)
            if model_name == 'alnafi':
                print("in if")
                customer_data = alnafi_payment_support_data(instance,payment_user)
            else:
                print("in else")
                customer_data = new_alnafi_payment_support_data(instance, payment_user)

            customer_url = 'https://crm.alnafi.com/api/resource/Suppport'
            response = requests.post(customer_url, headers=headers, json=customer_data)
            print(response)
            print(response.text)
            if response.status_code == 200:
                lead_data = response.json()
                # print(lead_data)
                customer_email = lead_data['data']['customer_email']
                if customer_email:
                    # print("lead id exists")
                    instance.customer_email = customer_email
                    # print("Lead created successfully!")
    except RequestException as e:
        # pass
        print("in except")
        print('Error occurred while making the request:', str(e))
        print('Error:', response.status_code)
        print('Error:', response.text) 



def change_lead_status_sales_module(instance, **kwargs):
    # print("change_lead_status_sales signal running")
    # print("model_name", model_name)
    # url = 'https://crm.alnafi.com/api/resource/Lead?limit_start=0&limit_page_length=23023&fields=["*"]'
    url = f'https://crm.alnafi.com/api/resource/Lead?fields=["name","email_id"]&filters=[["Lead","email_id","=","{instance.customer_email}"]]'
    api_key, api_secret = round_robin_support()
  
    headers = {
        'Authorization': f'token {api_key}:{api_secret}',
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    try:
        # print("in try")
        response = requests.get(url, headers=headers)
        # response.raise_for_status()
        data = response.json()
        already_existed = len(data["data"]) > 0

        # print(response.status_code)
        # print(data['data'])
        if already_existed:
            converted_date = datetime.now().date()
            lead_id = data['data'][0]['name']
            url = f'https://crm.alnafi.com/api/resource/Lead/{lead_id}'
            # print(customer_data)
            lead_data = {
                "status": "Converted",
                "converted_date": converted_date.isoformat()
            }
            # print(lead_data)
            response = requests.put(url, headers=headers, json=lead_data)
            # print(response)
            # print(response.text)
            instance.customer_email = data['data'][0]['email_id']
            # print("lead updated")
            # break
        else:
            pass
    except RequestException as e:
        pass
        # print("in except")
        # print('Error occurred while making the request:', str(e))
        # print('Error:', response.status_code)
        # print('Error:', response.text)     



def new_alnafi_payment_support_data(instance,payment_user):
    print("in New Alnafi Payment fubc")
    # print(payment_user)
    first_name = payment_user[0].first_name if payment_user[0].first_name else ''
    last_name = payment_user[0].last_name if payment_user[0].last_name else ''
    full_name = f'{first_name} {last_name}'.strip()

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

    # if instance.expiration_date and instance.expiration_date.date() >= current_date:
    #     expiration_status = 'Active'
    # else:
    #     expiration_status = 'Expired'

    if instance.payment_date:
        order_datetime_str = str(instance.payment_date)
        # Parse the original datetime string
        order_datetime = datetime.fromisoformat(order_datetime_str)

        # Format it in the expected format
        formatted_order_datetime_str = order_datetime.strftime('%Y-%m-%d %H:%M:%S')
    else:
        formatted_order_datetime_str = None

    if instance.expiration_date:
        expire_datetime_str = str(instance.expiration_date)
        # Parse the original datetime string
        expire_datetime = datetime.fromisoformat(expire_datetime_str)

        # Format it in the expected format
        formatted_expire_datetime_str = expire_datetime.strftime('%Y-%m-%d %H:%M:%S')
    else:
        formatted_expire_datetime_str = None

    
    if isinstance(instance.product_names, list):
        # Handle the list of product names in a way that makes sense for your use case
        # For example, you can join the list into a single string
        product_name = ", ".join(instance.product_names)
    else:
        product_name = instance.product_names


    # print(instance.product_names)
    customer_data = {
        "full_name": full_name or None,
        "contact_no": payment_user[0].phone or None,
        "customer_email": payment_user[0].email or None,
        "country": country_name,
        "product_name": product_name,
        "price_pkr": instance.amount_pkr or None,
        "price_usd": instance.amount_usd or None,
        "payment_source": instance.payment_method_source_name.capitalize() if instance.payment_method_source_name else None,
        "payment_date": formatted_order_datetime_str,
        "expiration_date": formatted_expire_datetime_str,
        "expiration_status": 'Active',
    }
    return customer_data




def alnafi_payment_support_data(instance,payment_user):
    first_name = payment_user[0].first_name if payment_user[0].first_name else ''
    last_name = payment_user[0].last_name if payment_user[0].last_name else ''
    full_name = f'{first_name} {last_name}'.strip()

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

    if instance.order_datetime:
        order_datetime_str = str(instance.order_datetime)
        # Parse the original datetime string
        order_datetime = datetime.fromisoformat(order_datetime_str)

        # Format it in the expected format
        formatted_order_datetime_str = order_datetime.strftime('%Y-%m-%d %H:%M:%S')
    else:
        formatted_order_datetime_str = None

    if instance.expiration_datetime:
        expire_datetime_str = str(instance.expiration_datetime)
        # Parse the original datetime string
        expire_datetime = datetime.fromisoformat(expire_datetime_str)

        # Format it in the expected format
        formatted_expire_datetime_str = expire_datetime.strftime('%Y-%m-%d %H:%M:%S')
    else:
        formatted_expire_datetime_str = None

    if isinstance(instance.product_name, list):
        # Handle the list of product names in a way that makes sense for your use case
        # For example, you can join the list into a single string
        product_name = ", ".join(instance.product_name)
    else:
        product_name = instance.product_name

    customer_data = {
        "full_name": full_name or None,
        "contact_no": payment_user[0].phone or None,
        "customer_email": payment_user[0].email or None,
        "country": country_name,
        "product_name": product_name,
        "price_pkr": instance.amount_pkr or None,
        "price_usd": instance.amount_usd or None,
        "payment_source": instance.source.capitalize() if instance.source else None,
        "payment_date": formatted_order_datetime_str,
        "expiration_date": formatted_expire_datetime_str,
        "expiration_status": 'Active',
    }
    # print(customer_data)
    return customer_data




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
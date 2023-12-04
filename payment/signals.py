import string
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import requests
from payment.views import AlnafiPayment

from products.models import Alnafi_Product
from .models import AlNafi_Payment, Main_Payment,New_Alnafi_Payments,Renewal
from rest_framework.response import Response
from requests.exceptions import RequestException
from user.models import Main_User
from django.core.cache import cache
from django.conf import settings
import json
from user.constants import COUNTRY_CODES
import environ
from secrets_api.algorithem import round_robin_support
from threading import Thread
from threading import Timer
from datetime import datetime
import math
import csv


env = environ.Env()
env.read_env()
# api_key = env("FRAPPE_API_KEY")
# api_secret = env("FRAPPE_API_SECRET")
DEBUG = env('DEBUG',cast=bool)



@receiver(pre_save, sender=New_Alnafi_Payments)
def new_alnafi_payment_signal_support(sender, instance: New_Alnafi_Payments, *args, **kwargs):
    # print("new alnafi signal running")
    model_name = 'new_alnafi'
    Thread(target=send_payment_support_module, args=(instance,model_name,)).start()


@receiver(pre_save, sender=AlNafi_Payment)
def alnafi_payment_signal_support(sender, instance: AlNafi_Payment, *args, **kwargs):
    model_name = 'alnafi'
    Thread(target=send_payment_support_module, args=(instance,model_name,)).start()


@receiver(pre_save, sender=New_Alnafi_Payments)
def new_alnafi_payment_signal_sales(sender, instance: New_Alnafi_Payments, *args, **kwargs):
    # print("new alnafi signal running for sales")
    model = 'NewAlnafi'
    Thread(target=change_lead_status_sales_module, args=(instance,model,)).start()


@receiver(pre_save, sender=AlNafi_Payment)
def alnafi_payment_signal_sales(sender, instance: AlNafi_Payment, *args, **kwargs):
    # print("alnafi signal running for sales")
    model = 'Alnafi'
    Thread(target=change_lead_status_sales_module, args=(instance,model,)).start()

@receiver(pre_save, sender=AlNafi_Payment)
def alnafi_payment_signal_renewal_leads(sender, instance: AlNafi_Payment, *args, **kwargs):
    # print("alnafi signal running for sales")
    Thread(target=change_lead_status_renewal_module, args=(instance,)).start()

@receiver(pre_save, sender=New_Alnafi_Payments)
def new_alnafi_payment_renewal_leads(sender, instance: New_Alnafi_Payments, *args, **kwargs):
    # print("new alnafi signal running for sales")
    Thread(target=change_lead_status_renewal_module, args=(instance,)).start()



@receiver(pre_save, sender=Renewal)
def support_renewal_leads_signal(sender, instance: Renewal, *args, **kwargs):
    # print("renewal leads signal running for support")
    Thread(target=support_renewal_leads, args=(instance,)).start()


def send_payment_support_module(instance,model_name, **kwargs):
    if model_name == 'alnafi':     
        if isinstance(instance.product_name, list):
            product_name = ", ".join(instance.product_name)
        else:
            product_name = instance.product_name            
    else:
        if isinstance(instance.product_names, list):
            product_name = ", ".join(instance.product_names)
        else:
            product_name = instance.product_names

    url = f'https://crm.alnafi.com/api/resource/Suppport?fields=["customer_email","product_name"]&filters=[["Suppport","customer_email","=","{instance.customer_email}"],["Suppport","product_name","=","{product_name}"]]'
    user_api_key = '4e7074f890507cb'
    user_secret_key = 'c954faf5ff73d31'
    admin_headers = {
        'Authorization': f'token {user_api_key}:{user_secret_key}',
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    try:
        response = requests.get(url, headers=admin_headers)
        data = response.json()
        payment_user = Main_User.objects.filter(email__iexact=instance.customer_email)
        testing_email = payment_user[0].email

        if testing_email.endswith("yopmail.com"):
            pass
        else:
            already_existed = len(data["data"]) > 0
        
            if already_existed:
                pass
            else:
                url = f'https://crm.alnafi.com/api/resource/Suppport?fields=["lead_creator"]&filters=[["Suppport","customer_email","=","{instance.customer_email}"]]'

                response = requests.get(url, headers=admin_headers)
                data = response.json()

                already_exist = len(data["data"]) > 0
                if already_exist:
                    email = data['data'][0]["lead_creator"]

                    agents = {"zeeshan.mehr@alnafi.edu.pk": ["a17f7cc184a55ec","3e26bf2dde0db20"],
                              "mutahir.hassan@alnafi.edu.pk": ["ee3c9803e0a7aa0","ad8a5dc4bc4f13f"],
                              "sufyan.arshad@alnafi.edu.pk": ["ae5b7895b8b9ba8","da5406f0c217a40"],
                              "mehtab.sharif@alnafi.edu.pk": ["6b0bb41dba21795","f56c627e47bdff6"],
                              "salman.amjad@alnafi.edu.pk": ["c09e9698c024bd5","02c5e4ff622bb22"],
                              "ahsan.ali@alnafi.edu.pk": ["b5658b2d5a087d0","a9faaabc26bddc5"],
                              "mujtaba.jawed@alnafi.edu.pk": ["940ef42feabf766","7a642a5b930eb44"]
                              }
                    
                    if email in agents:
                        keys_of_agent = agents[email]
                    

                        if model_name == 'alnafi':
                            customer_data = alnafi_payment_support_data(instance,payment_user)
                        else:
                            customer_data = new_alnafi_payment_support_data(instance, payment_user)

                        agent_headers = {
                            'Authorization': f'token {keys_of_agent[0]}:{keys_of_agent[1]}',
                            "Content-Type": "application/json",
                            "Accept": "application/json",
                        }
                        customer_url = 'https://crm.alnafi.com/api/resource/Suppport'
                        response = requests.post(customer_url, headers=agent_headers, json=customer_data)
                        if response.status_code != 200:
                            lead_data = response.json()
                        
                else:
                    if model_name == 'alnafi':
                        customer_data = alnafi_payment_support_data(instance,payment_user)
                    else:
                        customer_data = new_alnafi_payment_support_data(instance, payment_user)

                    api_key, api_secret = round_robin_support()
                    headers = {
                        'Authorization': f'token {api_key}:{api_secret}',
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    }
                    customer_url = 'https://crm.alnafi.com/api/resource/Suppport'
                    response = requests.post(customer_url, headers=headers, json=customer_data)
                    if response.status_code == 200:
                        lead_data = response.json()
                        customer_email = lead_data['data']['customer_email']
                        if customer_email:
                            instance.customer_email = customer_email
                    else:
                        pass
                    
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
    except Exception as e:
        pass
       




def new_alnafi_payment_support_data(instance,payment_user):
    # print("in New Alnafi Payment fubc")
    # print(payment_user)
    first_name = payment_user[0].first_name if payment_user[0].first_name else ''
    last_name = payment_user[0].last_name if payment_user[0].last_name else ''

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

        formatted_order_datetime = datetime.strptime(formatted_order_datetime_str, "%Y-%m-%d %H:%M:%S")

        formatted_order_date = formatted_order_datetime.strftime('%Y-%m-%d')
    else:
        formatted_order_date = None


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
        "first_name": first_name or None,
        "last_name": last_name or None,
        "contact_no": payment_user[0].phone or None,
        "customer_email": payment_user[0].email or None,
        "country": country_name,
        "product_name": product_name,
        "price_pkr": instance.amount_pkr or None,
        "price_usd": instance.amount_usd or None,
        "amount": instance.amount or None,
        "currency": instance.payment_method_currency or None,
        "payment_source": instance.payment_method_source_name.upper() if instance.payment_method_source_name and (instance.payment_method_source_name == 'ubl' or instance.payment_method_source_name == 'UBL' or instance.payment_method_source_name == 'Ubl') else instance.payment_method_source_name.capitalize() if instance.payment_method_source_name else None,
        "payment": formatted_order_date,
        "expiration_date": formatted_expire_datetime_str,
        "expiration_status": 'Active',
    }
    return customer_data




def alnafi_payment_support_data(instance,payment_user):
    first_name = payment_user[0].first_name if payment_user[0].first_name else ''
    last_name = payment_user[0].last_name if payment_user[0].last_name else ''

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
        # Convert the string to a datetime object
        formatted_order_datetime = datetime.strptime(formatted_order_datetime_str, "%Y-%m-%d %H:%M:%S")

        formatted_order_date = formatted_order_datetime.strftime('%Y-%m-%d')
        # Now, you can access the date attribute
        # formatted_order_date = formatted_order_date.date()
    else:
        formatted_order_date = None

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
        "first_name": first_name or None,
        "last_name": last_name or None,
        "contact_no": payment_user[0].phone or None,
        "customer_email": payment_user[0].email or None,
        "country": country_name,
        "product_name": product_name,
        "price_pkr": instance.amount_pkr or None,
        "price_usd": instance.amount_usd or None,
        "payment_source": instance.source.upper() if instance.source and (instance.source == 'ubl' or instance.source == 'UBL' or instance.source == 'Ubl') else instance.source.capitalize() if instance.source else None,
        "payment": formatted_order_date,
        "expiration_date": formatted_expire_datetime_str,
        "expiration_status": 'Active',
    }
    return customer_data



def support_renewal_leads(instance):
    crm_endpoint = 'https://crm.alnafi.com/api/resource/Renewal Leads'

    api_key, api_secret = round_robin_support()
    # api_key = '2a1d467717681df'
    # api_secret = '39faa082ac5f258'

    headers = {
        'Authorization': f'token {api_key}:{api_secret}',
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    # print("instance.date_joined",instance.date_joined)
    # print("instance.payment_date",instance.payment_date)

    def format_date(date):
        if isinstance(date, str):
            try:
                # Attempt to parse the date string
                date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f %z")
            except ValueError:
                date = None  # Handle invalid date string
        return date.isoformat() if date else None


    data = {
        "first_name": instance.first_name or None,
        "last_name": instance.last_name or None,
        "user_id": instance.user_id or None,
        "phone": instance.phone if instance.phone else None,
        "country": instance.country or "Unknown",
        "address": instance.address or None,
        "date_joined": instance.date_joined,
        "payment_date": instance.payment_date,
        "expiration_date": instance.expiration_date if instance.expiration_date else None,
        "product_name": instance.product_name or None,
        "status": instance.status or None,
        "assigned_date": datetime.now().date().isoformat()
    }

    # print(data)

    failed_leads = []

    try:
        response = requests.post(crm_endpoint, headers=headers, json=data)
    except Exception as e:
        print("Error posting renewal lead data:", str(e))
        failed_leads.append(data)

    if failed_leads:
        with open('failed_renewal_leads.csv', 'w', newline='') as csvfile:
            fieldnames = failed_leads[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for lead in failed_leads:
                writer.writerow(lead)

    if response.status_code != 200:
        print(headers)
        # print(data)
        # print(f"Failed to upload data for: {instance.user_id}")
        # print(response.status_code)
        # print(response.text)
    else:
        print("lead created successfully")





def change_lead_status_renewal_module(instance):
    if hasattr(instance, 'product_name'):
        product_name = instance.product_name
        if isinstance(product_name, list):
            product_name = instance.product_name[0]
            
    elif hasattr(instance, 'product_names'):
        product_name = instance.product_names
        if isinstance(product_name, list):
            product_name = instance.product_names[0]

    # print(product_name)
    url = f'https://crm.alnafi.com/api/resource/Renewal Leads?fields=["name","user_id"]&filters=[["Renewal Leads","user_id","=","{instance.customer_email}"],["Renewal Leads","product_name","=","{product_name}"]]'
    # print(instance.product_name[0])
    api_key = '4e7074f890507cb'
    api_secret = 'c954faf5ff73d31'

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
        # exit()
        if already_existed:
            converted_date = datetime.now().date()
            lead_id = data['data'][0]['name']
            url = f'https://crm.alnafi.com/api/resource/Renewal Leads/{lead_id}'
            # print(customer_data)

            if hasattr(instance, 'expiration_datetime') and instance.expiration_datetime is not None:
                expiration_date = instance.expiration_datetime.isoformat()
            elif hasattr(instance, 'expiration_date') and instance.expiration_date is not None:
                expiration_date = instance.expiration_date.isoformat()
            else:
                # Handle the case where neither attribute is present or is None
                expiration_date = ""  # You can set a default value or raise an exception if needed


            lead_data = {
                "status": "Converted",
                # "converted_date": converted_date.isoformat(),
                "expiration_date": expiration_date

            }
            # print(lead_data)
            response = requests.put(url, headers=headers, json=lead_data)
            # print(response)
            # print(response.text)
            # print("lead updated")
        else:
            pass
    except Exception as e:
        # pass
        print(e)
        print(response)
        print(response.text)
    






def change_lead_status_sales_module(instance,model, **kwargs):
    # print("change_lead_status_sales signal running")
    # print("instance.customer_email",instance.customer_email)
    url = f'https://crm.alnafi.com/api/resource/Lead?fields=["name","email_id"]&filters=[["Lead","email_id","=","{instance.customer_email}"]]'

    if model == 'Alnafi':
        payments_matching_criteria = AlNafi_Payment.objects.filter(product_name=instance.product_name, customer_email=instance.customer_email)
    elif model == 'NewAlnafi':
        payments_matching_criteria = New_Alnafi_Payments.objects.filter(product_names=instance.product_names, customer_email=instance.customer_email)

    # print("payments_matching_criteria",payments_matching_criteria)
    if not payments_matching_criteria:
        # print("inside if")
        # api_key, api_secret = round_robin_support()
        api_key = '4e7074f890507cb'
        api_secret = 'c954faf5ff73d31'

        headers = {
            'Authorization': f'token {api_key}:{api_secret}',
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        # try:
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
        # except Exception as e:
        #     pass
            # print("in except")
            # print('Error occurred while making the request:', str(e))
            # print('Error:', response.status_code)
            # print('Error:', response.text)     
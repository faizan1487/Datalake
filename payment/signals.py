import string
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import requests
from .services import get_pkr_rate
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
from secrets_api.algorithem import round_robin_support, round_robin_exam
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
def new_alnafi_payment_signal_exam(sender, instance: New_Alnafi_Payments, *args, **kwargs):
    # print("exam new alnafi signal running")
    model_name = 'new_alnafi'
    fun = send_payment_exam_module(instance,model_name)
    # Thread(target=send_payment_exam_module, args=(instance,model_name,)).start()

@receiver(pre_save, sender=AlNafi_Payment)
def alnafi_payment_signal_exam(sender, instance: New_Alnafi_Payments, *args, **kwargs):
    # print("alnafi exam signal running")
    model_name = 'alnafi'
    fun = send_payment_exam_module(instance,model_name)    

@receiver(pre_save, sender=New_Alnafi_Payments)
def new_alnafi_payment_signal_sales(sender, instance: New_Alnafi_Payments, *args, **kwargs):
    # print("new alnafi signal running for sales")
    model = 'NewAlnafi'
    Thread(target=change_lead_status_sales_module, args=(instance,model,)).start()

@receiver(post_save, sender=New_Alnafi_Payments)
def new_alnafi_payment_signal_commission(sender, instance: New_Alnafi_Payments, *args, **kwargs):
    # print("new alnafi signal running for commission")
    model = 'NewAlnafi'
    Thread(target=send_payment_to_commission_doctype, args=(instance,model,)).start()

@receiver(post_save, sender=AlNafi_Payment)
def alnafi_payment_signal_commission(sender, instance: AlNafi_Payment, *args, **kwargs):
    # print("alnafi signal running for commission")
    model = 'Alnafi'
    Thread(target=send_payment_to_commission_doctype, args=(instance,model,)).start()


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
            flat_list = [item for sublist in instance.product_names for item in sublist]
            product_name = ", ".join(flat_list)
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

    response = requests.get(url, headers=admin_headers)
    data = response.json()
    payment_user = Main_User.objects.filter(email__iexact=instance.customer_email)
    testing_email = payment_user[0].email

    if testing_email.endswith("yopmail.com"):
        pass
    else:
        already_existed = len(data["data"]) > 0

        # print("support already_existed",already_existed)
    
        if already_existed:
            pass
        else:
            # print("in else")
            url = f'https://crm.alnafi.com/api/resource/Suppport?fields=["lead_creator"]&filters=[["Suppport","customer_email","=","{instance.customer_email}"]]'

            response = requests.get(url, headers=admin_headers)
            data = response.json()

            already_exist = len(data["data"]) > 0
            if already_exist:
                email = data['data'][0]["lead_creator"]


                agents = {"zeeshan.mehr@alnafi.edu.pk": ["a17f7cc184a55ec","3e26bf2dde0db20"],
                            "mutahir.hassan@alnafi.edu.pk": ["ee3c9803e0a7aa0","ad8a5dc4bc4f13f"],
                            "mehtab.sharif@alnafi.edu.pk": ["6b0bb41dba21795","f56c627e47bdff6"],
                            "haider.raza@alnafi.edu.pk": ["2a1d467717681df","39faa082ac5f258"],
                            "salman.amjad@alnafi.edu.pk": ["c09e9698c024bd5","02c5e4ff622bb22"],
                            "ahsan.ali@alnafi.edu.pk": ["b5658b2d5a087d0","a9faaabc26bddc5"],
                            "mujtaba.jawed@alnafi.edu.pk": ["940ef42feabf766","7a642a5b930eb44"]
                            }
                
                if email in agents:
                    keys_of_agent = agents[email]
                
                    product = 'simple product'
                    if model_name == 'alnafi':
                        customer_data = alnafi_payment_support_data(instance,payment_user,product)
                    else:
                        customer_data = new_alnafi_payment_support_data(instance, payment_user,product)
                    
                    if customer_data is None:
                        return

                    agent_headers = {
                        'Authorization': f'token {keys_of_agent[0]}:{keys_of_agent[1]}',
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    }
                    customer_url = 'https://crm.alnafi.com/api/resource/Suppport'
                    response = requests.post(customer_url, headers=agent_headers, json=customer_data)
                    if response.status_code != 200:
                        pass
                        # print(response.text)
                    else:
                        pass
                        # print("data for already existed agent sent to support doctype")
            

            else:
                product = 'simple product'
                if model_name == 'alnafi':
                    customer_data = alnafi_payment_support_data(instance,payment_user,product)
                else:
                    customer_data = new_alnafi_payment_support_data(instance, payment_user,product)

                if customer_data is None:
                    return

                api_key, api_secret = round_robin_support()
                headers = {
                    'Authorization': f'token {api_key}:{api_secret}',
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                }
                customer_url = 'https://crm.alnafi.com/api/resource/Suppport'
                response = requests.post(customer_url, headers=headers, json=customer_data)
                if response.status_code != 200:
                    pass
                    # print(response.text)
                else:
                    pass
                    # print("data sent to support doctype")
                   
   


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


def send_payment_to_commission_doctype(instance,model_name, **kwargs):
    # print("signal Running")
    current_date = datetime.now().date()
    # print("instance.created_at",type(instance.created_at.date()))
    # print("current_date",type(current_date))

    # print("instance.created_at",instance.created_at.date())
    # print("current_date",current_date)

    if instance.created_at.date() >= current_date: 

        url = f'https://crm.alnafi.com/api/resource/Lead?fields=["name","lead_creator","phone"]&filters=[["Lead","email_id","=","{instance.customer_email}"]]'
        api_key = "4e7074f890507cb"
        api_secret = "c954faf5ff73d31"
        email_keys = {
            "muzammil.raees@alnafi.edu.pk": ("b6d818ef8024f5a", "ce1749a7dcf8577"),
            "ribal.shahid@alnafi.edu.pk": ("39d14c9d602fa09", "216de0a015e7fd1"),
            "waqas.shah@alnafi.edu.pk" : ("b09d1796de6444a", "9ac70da03e4c23c"),
            "shoaib.akhtar@alnafi.edu.pk": ("484f3e9978c00f3","f61de5c03b3935d"),
            "haider.raza@alnafi.edu.pk": ("2a1d467717681df", "f2edc530744442b"),
            "saad.askari@alnafi.edu.pk": ("e31afcb884def7e", "cb799e6913b57f9"),
            "saima.ambreen@alnafi.edu.pk": ("3da0a250742fa00", "5ec8bb8e1e94930"),
            "hamza.jamal@alnafi.edu.pk": ("dd3d10e83dfbb6b", "a1a50d549455fe3"),
            "wamiq.siddiqui@alnafi.edu.pk": ("31c85c7e921b270", "845aff8197932c3"),
            "Administrator": ("4e7074f890507cb", "c954faf5ff73d31"),
        }

        headers = {
            'Authorization': f'token {api_key}:{api_secret}',
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        response = requests.get(url, headers=headers)
        data = response.json()
        # print(data)
        already_existed = len(data.get("data", [])) > 0

        # print("already_existed", already_existed)
        check_payment_url = 'https://crm.alnafi.com/api/resource/Commission'
        Headers = {
            'Authorization': f'token {api_key}:{api_secret}',
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        check_data = {
                "filters": [["payment_id", "=", instance.id]]
        }

        response = requests.get(check_payment_url, headers=Headers, json=check_data)
        lead_data = response.json()
        # print("lead_data",lead_data)

        if len(lead_data.get("data", [])) > 0:
            pass
            # print("Payment already exists in commission system")
        else:
            if already_existed:
                # print("In if")
                lead_info = data["data"][0] if len(data.get("data", [])) > 0 else {}
                # lead_creator_email = data.get('lead_creator', '')
                lead_creator_email = lead_info.get('lead_creator', '')

                if lead_creator_email in email_keys:
                    post_api_key, post_secret_key = email_keys[lead_creator_email]
                    
                    headers_post = {
                        'Authorization': f'token {post_api_key}:{post_secret_key}',
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    }

                commission_url = 'https://crm.alnafi.com/api/resource/Commission'
                
                # Extracting phone and lead_creator safely
                lead_info = data["data"][0] if len(data.get("data", [])) > 0 else {}
                phone = lead_info.get('phone')
                lead_creator = lead_info.get('lead_creator')
                total_product_payment = 0
                commission_amount = 0
                if model_name == "NewAlnafi":
                        payment_date = instance.payment_date.date()
                        if isinstance(instance.product_names, list):
                            # Flatten the list of lists into a single list
                            flat_list = [item for sublist in instance.product_names for item in sublist]

                            # Join the flattened list into a string
                            product_name = ", ".join(flat_list)
                        else:
                            product_name = instance.product_names
                if model_name == "Alnafi" :   
                    payment_date = instance.order_datetime.date()
                    if isinstance(instance.product_name, list):
                        flat_list = [item for sublist in instance.product_name for item in sublist]

                        # Join the flattened list into a string
                        product_name = ", ".join(flat_list)
                    else:
                        product_name = instance.product_name 
                if "easy pay study" in product_name.lower():
                    commission_percentage = 0.02  
                else:
                    commission_percentage = 0.08  
                if lead_creator:
                    # commission_percentage = 0.0
                    if model_name == "NewAlnafi":
                        if instance.payment_method_currency.lower() == 'pkr':
                            # commission_percentage = 0.08 
                            if instance.amount: 
                                commission_amount = instance.amount * commission_percentage
                                total_product_payment = instance.amount
                    else:
                        if instance.amount_pkr > 0:
                            # commission_percentage = 0.08
                            commission_amount = instance.amount_pkr * commission_percentage
                            total_product_payment = instance.amount_pkr

                    if model_name == "NewAlnafi":
                        if instance.payment_method_currency.lower() != 'pkr':
                            if instance.amount:
                                amount = instance.amount
                                currency_rate = get_pkr_rate(instance.payment_method_currency, amount)
                                converted_amount = round(float(amount) / currency_rate[instance.payment_method_currency], 2)
                                # print(converted_amount)
                                # commission_percentage = 0.08  
                                commission_amount = round(float(converted_amount * commission_percentage), 2)
                                total_product_payment = converted_amount
                    else:
                        if instance.amount_usd > 0:
                            amount = instance.amount_usd
                            currency = "usd"
                            currency_rate = get_pkr_rate(currency, amount)
                            converted_amount = round(float(amount) / currency_rate[currency], 2)
                            # print(converted_amount)
                            commission_percentage = 0.08  
                            commission_amount = round(float(converted_amount * commission_percentage), 2)
                            total_product_payment = converted_amount
                
                    if model_name == "NewAlnafi":
                        order_id = instance.orderId    
                    else:
                        order_id = instance.order_id
                    if model_name == "NewAlnafi":
                        source = instance.payment_method_source_name    
                    else:
                        source = instance.source

                        
                    commission_data = {
                        "payment_id": instance.id,
                        "title": instance.customer_email,
                        "phone": phone or 0,
                        "order_id": order_id,
                        "payment_date": payment_date.isoformat(),
                        "total_product_payment": total_product_payment,
                        "owner_pkr": commission_amount,
                        "product": product_name,
                        "source": source,
                        "lead_owner": lead_creator,
                        "created_at": current_date.isoformat()
                    }
                
                    response = requests.post(commission_url, headers=headers_post, json=commission_data)
                    # print(response.text)
                    if response.status_code == 200:
                        # Successfully created Commission entry based on lead information
                        pass
                        # print(response.status_code)
                    else:
                        pass
                        print(response.text)
                else:
                    pass
                    # Handle cases where phone or lead_creator is missing
                    # print("phone or lead_creator is missing Went Wrong")
            else:
                pass
                # Handle cases where data['data'] is empty
                # print(" data['data'] is empty Went Wrong")


def new_alnafi_payment_support_data(instance,payment_user,product):
    # print("in New Alnafi Payment data fubc")
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
        if product == 'simple product':
            product_names = []

            for product in instance.product_names:
                if 'exam' not in product.lower():
                    product_names.append(product) 

            # print("new alnafi simple len(product_names)",len(product_names))
            if len(product_names) <= 0:
                return

            product_name = ", ".join(product_names)
        else:
            product_names = []

            for product in instance.product_names:
                if 'exam' in product.lower():  
                    product_names.append(product) 

            # print('here')
            # print("new alnafi exam len(product_names)",len(product_names))
            if len(product_names) <= 0:
                return

            product_name = ", ".join(product_names)
            # print("product_name",product_name)
    else:
        if not instance.product_names:
            return
        #handle exam product here too
        if product == 'simple product':
            if 'exam' not in instance.product_names:
                product_name = instance.product_names
            else:
                return
        else:
            if 'exam' in instance.product_names:
                product_name = instance.product_names
            else:
                return

    



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



def alnafi_payment_support_data(instance,payment_user,product):
    first_name = payment_user[0].first_name if payment_user[0].first_name else ''
    last_name = payment_user[0].last_name if payment_user[0].last_name else ''
    country_code = payment_user[0].country or None
    country_name = None

    if country_code:
        for name, code in COUNTRY_CODES.items():
            if code == country_code:
                country_name = name
                break


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
        if product == 'simple product':
            product_names = []

            for product in instance.product_name:
                if 'exam' not in product.lower():
                    product_names.append(product) 

            # print("simple len(product_names)",len(product_names))
            if len(product_names) <= 0:
                return
            

            product_name = ", ".join(product_names)
        else:
            product_names = []

            for product in instance.product_name:
                if 'exam' in product.lower():  
                    product_names.append(product) 

            # print("exam len(product_names)",len(product_names))
            if len(product_names) <= 0:
                return

            product_name = ", ".join(product_names)
    else:
        #handle exam product here too
        if product == 'simple product':
            if not instance.product_name:
                return
            if 'exam' not in instance.product_name:
                product_name = instance.product_name
            else:
                return
        else:
            if not instance.product_name:
                return
            if 'exam' in instance.product_name:
                product_name = instance.product_name
            else:
                return


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
        pass
        # print(e)
        # print(response)
        # print(response.text)


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


def send_payment_exam_module(instance,model_name, **kwargs):

    if model_name=='alnafi':
        if isinstance(instance.product_name, list):
            product_names = []

            for product in instance.product_name:
                if 'exam' in product.lower():  
                    product_names.append(product)

            # print("exam alnafi payment length of product for filtering the product len(product_names)",len(product_names))
            if len(product_names) <= 0:
                return

            product_name = product_names[0] 
        else:
            product_name = instance.product_name
    else:
        if isinstance(instance.product_names, list):
            product_names = []

            for product in instance.product_names:
                if 'exam' in product.lower():  
                    product_names.append(product) 


            # print("exam new alnafi payment length of product for filtering the product len(product_names)",len(product_names))
            if len(product_names) <= 0:
                return

            product_name = product_names[0] 
        else:
            product_name = instance.product_names


    url = f'https://crm.alnafi.com/api/resource/Exam 5 6 Leads?fields=["customer_email","product_name"]&filters=[["Exam 5 6 Leads","customer_email","=","{instance.customer_email}"],["Exam 5 6 Leads","product_name","=","{product_name}"]]'
    user_api_key = '4e7074f890507cb'
    user_secret_key = 'c954faf5ff73d31'
    admin_headers = {
        'Authorization': f'token {user_api_key}:{user_secret_key}',
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=admin_headers)
    data = response.json()
    payment_user = Main_User.objects.filter(email__iexact=instance.customer_email)
    if payment_user:
        testing_email = payment_user[0].email
    else:
        testing_email = None
    if testing_email and testing_email.endswith("yopmail.com"):
        pass
    else:
        already_existed = len(data["data"]) > 0
    
        if already_existed:
            pass
        else:
            url = f'https://crm.alnafi.com/api/resource/Exam 5 6 Leads?fields=["lead_creator"]&filters=[["Exam 5 6 Leads","customer_email","=","{instance.customer_email}"]]'

            response = requests.get(url, headers=admin_headers)
            data = response.json()


            already_exist = len(data["data"]) > 0
            if already_exist:
                print("agent already exists")
                email = data['data'][0]["lead_creator"]

                agents = {"zeeshan.mehr@alnafi.edu.pk": ["a17f7cc184a55ec","3e26bf2dde0db20"],
                            "mehtab.sharif@alnafi.edu.pk": ["6b0bb41dba21795","f56c627e47bdff6"],
                            "haider.raza@alnafi.edu.pk": ["2a1d467717681df","39faa082ac5f258"],
                            }
                
                if email in agents:
                    keys_of_agent = agents[email]
                
                    product = 'exam product'
                    if model_name == 'alnafi':
                        customer_data = alnafi_payment_support_data(instance,payment_user,product)
                    else:
                        customer_data = new_alnafi_payment_support_data(instance, payment_user,product)
                    if customer_data is None:
                        return
                    customer_data['created_at'] = datetime.today().isoformat()

                    agent_headers = {
                        'Authorization': f'token {keys_of_agent[0]}:{keys_of_agent[1]}',
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    }
                    customer_url = 'https://crm.alnafi.com/api/resource/Exam 5 6 Leads'
                    response = requests.post(customer_url, headers=agent_headers, json=customer_data)
                    if response.status_code != 200:
                        lead_data = response.json()
                    
            else:

                product = 'exam product'
                if model_name == 'alnafi':
                    customer_data = alnafi_payment_support_data(instance,payment_user,product)
                else:
                    customer_data = new_alnafi_payment_support_data(instance, payment_user,product)
                # print("customer data",customer_data)
                if customer_data is None:
                    return
                customer_data['created_at'] = datetime.today().isoformat()
                

                api_key, api_secret = round_robin_exam()
                headers = {
                    'Authorization': f'token {api_key}:{api_secret}',
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                }
                customer_url = 'https://crm.alnafi.com/api/resource/Exam 5 6 Leads'
                response = requests.post(customer_url, headers=headers, json=customer_data)
                if response.status_code != 200:
                    pass
                    # print(response.text)
                else:
                    pass
                    # print("data sent to exam doctype")
                    

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import requests
from .models import AlNafi_User, IslamicAcademy_User,PSWFormRecords, Moc_Leads,New_AlNafi_User, CvForms
from user.constants import COUNTRY_CODES
from newsletter.signals import send_lead_post_request
import environ
from secrets_api.algorithem import round_robin
from albaseer.settings import DEBUG
from datetime import datetime
import csv
import json
import pandas as pd


env = environ.Env()
env.read_env()
DEBUG = env('DEBUG',cast=bool)

@receiver(post_save, sender=AlNafi_User)
def alnafi_lead_to_erp(sender, instance, **kwargs):
    # print("alnafi user signal running")
    # source='Academy Signup'
    source = instance.login_source
    alnafi_user = usersignal(instance,source,sender)


@receiver(post_save, sender=IslamicAcademy_User)
def send_islamic_lead_post_request(sender, instance, **kwargs):

    # print("islamic user signal")
    source='IslamicAcademy'
    islamic_user = usersignal(instance,source,sender)


@receiver(post_save, sender=PSWFormRecords)
def psw_lead_to_erp(sender, instance, **kwargs):

    # print("psw user signal")
    source='PSWFormRecords'
    psw_form_user = usersignal(instance,source,sender)

@receiver(post_save, sender=New_AlNafi_User)
def new_alnafi_lead_to_erp(sender, instance, created, *args, **kwargs):
    new_alnafi_user = newsignupsignal(instance,sender)


def usersignal(instance,source,sender):
    # print("user signal running")
    if source == 'Academy' or source == 'Academy Signup' or instance.form == 'O Level Academy Form' or instance.form == 'O-Level New Batch (Crash Course)':
        user_api_key = '2a1d467717681df'
        user_secret_key = '39faa082ac5f258'

        if instance.email.endswith("yopmail.com"):
            # Admin keys
            user_api_key = '4e7074f890507cb'
            user_secret_key = 'c954faf5ff73d31'
        
        url = f'https://crm.alnafi.com/api/resource/Lead?fields=["name","email_id"]&filters=[["Lead","email_id","=","{instance.email}"]]'
        
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



        # Assuming instance.created_at is a datetime object
        if hasattr(instance, 'created_at'):
            date_joined_str = instance.created_at.strftime('%Y-%m-%d %H:%M:%S')
        else:
            date_joined_str = None

        data = {
            "first_name": instance.first_name or None,
            "last_name": instance.last_name if hasattr(instance, 'last_name') else None,
            "email_id": instance.email or None,
            "mobile_no": str(instance.phone) if hasattr(instance, 'phone') and instance.phone else '00000000000',
            "country": country_name,
            "source": source,
            "form": instance.form or None,
            "date": date_joined_str,  # Convert to ISO 8601 string
            "advert_detail": instance.advert or None,
            # Add other fields from the Main_User model to the data dictionary as needed
        }

        response = requests.get(url, headers=headers)
        lead_data = response.json()
        if 'data' not in lead_data:
            already_existed = False
        else:
            already_existed = len(lead_data["data"]) > 0
        

        if already_existed:
            pass
        else:
            if not instance.affiliate_code:
                url = 'https://crm.alnafi.com/api/resource/Lead'
                lead_data = response.json()
                response = requests.post(url, headers=headers, json=data)
                if response.status_code != 200:
                    print("response.status_code",response.text)
                    print("response.status_code",response.status_code)
                else:
                    print("lead created successfully")
            

#############################################################
# @receiver(post_save, sender=Moc_Leads)
def post_request_sale_doctype(sender, instance, created, **kwargs):
    # return
    source=instance.login_source
    Moc_Leads = mocLead_Signalto_sale_doctype(instance,source)   

# @receiver(post_save, sender=Moc_Leads)
def post_request_moc_doctype(sender, instance, created, **kwargs):
    # return
    source=instance.login_source
    Moc_Leads = mocLead_Signalto_moc_doctype(instance,source)


@receiver(post_save, sender=AlNafi_User)
def alnafi_lead_to_moc_doctype(sender, instance, **kwargs):
    print("alnafi lead to moc signal running")
    # source='Academy Signup'
    source = instance.login_source
    alnafi_user = mocLead_Signalto_moc_doctype(instance,source)    


import math  # Import math for handling nan

def mocLead_Signalto_moc_doctype(instance,source):
    # print("mocdoctype signa;")
    api_key = '351b6479c5a4a16'
    api_secret = 'e459db7e2d30b34'
    headers = {
        'Authorization': f'token {api_key}:{api_secret}',
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    country_code = getattr(instance, 'country', "Unknown")
    print("country_code",country_code)

    if math.isnan(country_code):
        country_name = None
    else:
        if country_code:
            country_name = None
            if len(country_code) <= 2:
                if country_code:
                    for name, code in COUNTRY_CODES.items():
                        if code == country_code:
                            country_name = name
                            break
            else:
                country_name = country_code
        else:
            country_name = "Unknown"
    
    data = {
            "name1": instance.first_name or None,
            "first_name": instance.first_name or None,
            "last_name": instance.last_name if hasattr(instance, 'last_name') else None,
            "email": instance.email or None,
            "contact_no": str(instance.phone) if hasattr(instance, 'phone') else None,
            "country": country_name,
            "lead_source":instance.login_source or None,
            "form":instance.form or None,
            "cv_link": instance.cv_link if hasattr(instance, 'cv_link') else None,
            "interest": instance.interest if hasattr(instance, 'interest') else None,
            "qualification": instance.qualification if hasattr(instance, 'qualification') else None,
            "created_at": instance.created_at.isoformat() or None,
            # Add other fields from the Main_User model to the data dictionary as needed
        }
    
    print(data)


    url = f'https://crm.alnafi.com/api/resource/moclead?fields=["name","email"]&filters=[["moclead","email","=","{instance.email}"]]'
    response = requests.get(url, headers=headers)
    lead_data = response.json()
    if response.status_code == 403:
        return
    if 'data' in lead_data:
        already_existed = len(lead_data["data"]) > 0
    else:
        already_existed = False

    failed_leads = []
    if not already_existed:
        if hasattr(instance, 'affiliate_code') and not instance.affiliate_code:

            print("mocdoctype signa;")
            try:
                post_url = 'https://crm.alnafi.com/api/resource/moclead'
                response = requests.post(post_url, headers=headers, json=data)
                if response.status_code == 200:
                    print("Lead created successfully!")

            except Exception as e:
                print("Error posting lead data:", str(e))
                failed_leads.append(data)
        

        if failed_leads:
            with open('failed_moc_doctype_leads.csv', 'a', newline='') as csvfile:
                fieldnames = failed_leads[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                # Check if the file is empty, and write header only if it's a new file
                if csvfile.tell() == 0:
                    writer.writeheader()

                for lead in failed_leads:
                    writer.writerow(lead)
        


def mocLead_Signalto_sale_doctype(instance,source):
    # print("mocLead_Signalto_sale_doctype")
    if source == 'Academy' or source == 'Academy Signup' or instance.form == 'O Level Academy Form' or instance.form == 'O-Level New Batch (Crash Course)':
        user_api_key = '2a1d467717681df'
        user_secret_key = '39faa082ac5f258'
    else:
        #	
        user_api_key = '5306bb96b02c8f1'
        user_secret_key = '362d44b933cef9e'
        # user_api_key, user_secret_key = round_robin()

        #admin keys
        # user_api_key = '4e7074f890507cb'
        # user_secret_key = 'c954faf5ff73d31'
        

    headers = {
        'Authorization': f'token {user_api_key}:{user_secret_key}',
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


    country_code = getattr(instance, 'country', "Unknown")
    if country_code:
        country_name = None
        if len(str(country_code)) <= 2:
            if country_code:
                for name, code in COUNTRY_CODES.items():
                    if code == country_code:
                        country_name = name
                        break
        else:
            country_name = country_code
    else:
        country_name = "Unknown"


    if hasattr(instance, 'created_at') and instance.created_at is not None:
        date_joined_str = instance.created_at.strftime('%Y-%m-%d %H:%M:%S')
    else:
        date_joined_str = None

        

    data = {
            "first_name": instance.first_name or None,
            "last_name": instance.last_name if hasattr(instance, 'last_name') else None,
            "email_id": instance.email or None,
            "mobile_no": str(instance.phone) if hasattr(instance, 'phone') else None,
            "country": country_name,
            "source":instance.login_source or None,
            "form":instance.form or None,
            "cv_link": instance.cv_link or None,
            "interest": instance.interest or None,
            "qualification": instance.qualification or None,
            "date_joined": str(date_joined_str) if date_joined_str else None,
            "date": str(date_joined_str) if date_joined_str else None,
            "advert_detail": instance.advert or None,
        }
    
    for key, value in data.items():
        if pd.isna(value):
            data[key] = None
    

    url = f'https://crm.alnafi.com/api/resource/Lead?fields=["name","email_id"]&filters=[["Lead","email_id","=","{instance.email}"]]'
    response = requests.get(url, headers=headers)

    lead_data = response.json()
    
    if 'data' in lead_data:
        already_existed = len(lead_data["data"]) > 0
    else:
        already_existed = False
    
    failed_leads = []
    if already_existed:
        # print("already exists")
        auth_url = 'https://auth.alnafi.edu.pk/api/v1.0/enrollments/demo-user/'
        enrollment_url = 'https://auth.alnafi.edu.pk/api/v1.0/enrollments/enrollment-user/'
        auth_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        }
        query_parameters = {
        "email": lead_data['data'][0]['email_id']  # Replace with the actual email you want to send
        }
        demo_user = requests.get(auth_url, headers=auth_headers, params=query_parameters)
        enrollment_user = requests.get(enrollment_url, headers=auth_headers, params=query_parameters)
        
        if demo_user.status_code == 200:
            demo_data = demo_user.json()
            data['demo_product'] = demo_data['product_name']

        if enrollment_user.status_code == 200:
            enrollment_data = enrollment_user.json()
            if len(enrollment_data['enrollments']) > 1:
                data['enrollment'] = enrollment_data['product_name']

        email_id = lead_data['data'][0]['email_id']
        url = f'https://crm.alnafi.com/api/resource/Lead/{email_id}'
        # print(data)
        response = requests.put(url, headers=headers, json=data)
        if response.status_code != 200:
            response_data = json.loads(response.text)
            if "exception" in response_data and "DuplicateEntryError" in response_data["exception"]:
                pass
            else:
                # print(response.text)
                data['error'] = response.text
                data['status_code'] = response.status_code
                failed_leads.append(data)
        else:
            print(f"updated {instance.email}")
    else:
        post_url = 'https://crm.alnafi.com/api/resource/Lead'
        response = requests.post(post_url, headers=headers, json=data)
        if response.status_code != 200:
            response_data = json.loads(response.text)
            if "exception" in response_data and "DuplicateEntryError" in response_data["exception"]:
                pass
            else:
                data['error'] = response.text
                data['status_code'] = response.status_code
                print("response.text",response.text)
                print("status code",response.status_code)
                failed_leads.append(data)
                # print(response.text)
        else:
            print(f"sale doctype signa; lead created successfully {instance.email}")


    if failed_leads:
        with open('failed_affiliate_from_signal.csv', 'a', newline='') as csvfile:
            fieldnames = failed_leads[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if csvfile.tell() == 0:
                writer.writeheader()

            for lead in failed_leads:
                writer.writerow(lead)




def newsignupsignal(instance,sender):
    # print("newsignupsignal running")
    source = instance.source

    if source == 'Academy' or source == 'Academy Signup':
        user_api_key = '2a1d467717681df'
        user_secret_key = '39faa082ac5f258'
    
        if instance.email.endswith("yopmail.com"):
            user_api_key = '4e7074f890507cb'
            user_secret_key = 'c954faf5ff73d31'

        url = f'https://crm.alnafi.com/api/resource/Lead?fields=["name","email_id"]&filters=[["Lead","email_id","=","{instance.email}"]]'

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

            if hasattr(instance, 'created_at'):
                date_joined_str = instance.created_at.strftime('%Y-%m-%d %H:%M:%S')
            else:
                date_joined_str = None


            data = {
                    "first_name": instance.first_name or None,
                    "last_name": None,
                    "email_id": instance.email or None,
                    "mobile_no": instance.phone if hasattr(instance, 'phone') else None,
                    "country": country_name,
                    "source": source,
                    "date": str(date_joined_str) if date_joined_str else None,
                    # Add other fields from the Main_User model to the data dictionary as needed
                }
            
            if not instance.affiliate_code:
                url = 'https://crm.alnafi.com/api/resource/Lead'
                response = requests.post(url, headers=headers, json=data)

                # if response and response.status_code != 200:
                #     print(response.text)


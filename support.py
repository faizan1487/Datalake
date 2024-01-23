import os
import django
from django.conf import settings
import csv
import datetime
import requests
import random
import json
import pandas as pd

# Set DEBUG and other required settings here
# settings.configure(
#     DEBUG=True,
#     # Add other required settings here
# )

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "albaseer.settings")
django.setup()

from secrets_api.algorithem import round_robin_support

def send_support_leads_on_crm():
    post_url = 'https://crm.alnafi.com/api/resource/Lead'
    # user_api_key, user_secret_key = round_robin_support()
    # headers = {
    #     'Authorization': f'token {user_api_key}:{user_secret_key}',
    #     "Content-Type": "application/json",
    #     "Accept": "application/json",
    # }
    data = pd.read_csv('/home/uzair/Documents/Al-Baseer-Backend/support leads.csv')
    for index, row in data.iterrows():
        first_name = str(row['first_name'])
        email = str(row['email_id'])
        phone = str(row['mobile_no'])
        source = str(row['source'])
        status = str(row['status'])
        form = str(row['form'])
        advert_detail = str(row['advert_detail'])
        date = datetime.datetime.now().date().isoformat()
        # print(source)
        lead = {
            'first_name': first_name,
            'email_id': email,
            'source': source,
            'status': status,
            'phone': phone,
            'form': form,
            'advert_detail': advert_detail,
            'date': date,
        }
        user_api_key, user_secret_key = round_robin_support()
        headers = {
        'Authorization': f'token {user_api_key}:{user_secret_key}',
        "Content-Type": "application/json",
        "Accept": "application/json",
        }
        response = requests.post(post_url, headers=headers, json=lead)
        print(response.status_code)
        print(f'Lead Uploaded Successfully {email}')

send_support_leads_on_crm()

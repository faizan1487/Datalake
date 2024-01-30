import imp
from locale import currency
import os
import requests
from user.constants import COUNTRY_CODES
from faker import Faker
import random
import csv
import django
import json
import math
from datetime import date, datetime, timedelta
import pandas as pd


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "albaseer.settings")
django.setup()


from user.models import Moc_Leads

def upload_leads():
    data = pd.read_csv('/home/uzair/Documents/Al-Baseer-Backend/Special.csv')
    # Iterate over rows in the DataFrame
    for index, row in data.iterrows():
        failed_leads = []
        # Extracting data from the row
        full_name = row['full_name']
        email = row['email']
        phone = row['phone']
        country = row['country']
        login_source = row['source']
        created_at_str = row['created_at']    
        if pd.isna(created_at_str):
            created_at = datetime.now()
        else:
            created_at = pd.to_datetime(created_at_str, format="%Y-%m-%d %H:%M:%S.%f%z")
        print("index", index)
    

        #from signal error file
        # full_name = row['first_name']
        # email = row['email_id']
        # phone = row['mobile_no']
        # country = row['country']
        # login_source = row['source']
        # created_at_str = row['date_joined']    

        form = row['form']
        form = None if pd.isna(form) else form
        advert = row['advert']
        # advert = row['advert detail']
        # created_at = pd.to_datetime(created_at_str, format="%Y/%m/%d %H:%M:%S")
        # try:
        moc, created = Moc_Leads.objects.get_or_create(email=email, defaults={
            'first_name': full_name,
            'phone': phone,
            'email': email,
            'form': form,
            'country': country,
            'login_source': login_source,
            'created_at': created_at,
            'advert': advert,
        })

        if not created:
            moc.first_name = full_name
            moc.email = email
            moc.phone = phone
            moc.form = form
            moc.country = country
            moc.login_source = login_source
            moc.created_at = created_at
            moc.advert = advert
            moc.save()
    # except Exception as e:
        lead_data = {
            'full_name':row['full_name'],
            'email':row['email'],
            'phone': row['phone'],
            'country': row['country'],
            'login_source':row['source'],
            'created_at_str': row['created_at'], 
            'form': row['form'],
            'advert': row['advert']
        }

        failed_leads.append(lead_data)

        if index <= 39:
            # Toqir Bhai keys
            user_api_key = '5306bb96b02c8f1'
            user_secret_key = '362d44b933cef9e'
        elif index >= 40 and index < 80: 
            # Saad Bhai Keys
            user_api_key = 'e31afcb884def7e'
            user_secret_key = 'cb799e6913b57f9'
        elif index >= 80 and index < 120:
            # Marij Keys
            user_api_key = 'b3bb7a167ec651a'
            user_secret_key = '449cd28cd263361'
        elif index >= 120 and index < 160:
            # Sunil Keys
            user_api_key = '9d37a29d966277f'
            user_secret_key = '018c3f6127c43cc'
        elif index >= 160 and index < 200:
            # Suleman Keys
            user_api_key = '3f6d0f005e4fccc'
            user_secret_key = 'bbcaef6140205d2'
        elif index >= 200 and index < 240:
            # Ribal Keys
            user_api_key = '39d14c9d602fa09'
            user_secret_key = '216de0a015e7fd1'
        elif index >= 240 and index < 280:
            # Waqas Keys
            user_api_key = 'b09d1796de6444a'
            user_secret_key = '9ac70da03e4c23c'
        elif index >= 280 and index < 320:
            # Shoaib keys
            user_api_key = '484f3e9978c00f3'
            user_secret_key = 'f61de5c03b3935d'
        elif index >= 320 and index < 360:
            # Saima Keys
            user_api_key = '3da0a250742fa00'
            user_secret_key = '5ec8bb8e1e94930'
        elif index >= 360 and index < 400:
            # Hamza Bhai keys
            user_api_key = 'dd3d10e83dfbb6b'
            user_secret_key = 'a1a50d549455fe3'
        elif index >= 400 and index < 440:
            # Wamiq Keys
            user_api_key = '31c85c7e921b270'
            user_secret_key = '845aff8197932c3'
            
        # print(f"Iteration: {index}, Using keys: {user_api_key}, {user_secret_key}")
        headers = {
            'Authorization': f'token {user_api_key}:{user_secret_key}',
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        country_code = getattr(data, 'country', "Unknown")

        if isinstance(country_code, str):
            country_name = country_code
        else:
            if not country_code.empty and country_code.notna().any():
                country_name = None
                if len(str(country_code.iloc[0])) <= 2:
                    for name, code in COUNTRY_CODES.items():
                        if code == country_code.iloc[0]:
                            country_name = name
                            break
            else:
                country_name = "Unknown"

        if 'created_at' in data and isinstance(data['created_at'], pd.Series) and pd.api.types.is_datetime64_any_dtype(data['created_at']):
            date_joined_str = data['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
        else:
            date_joined_str = None
        data = {
            "first_name": full_name or None,
            "last_name": None,  
            "email_id": email or None,
            "mobile_no": str(phone) if phone else None,
            "country": country_name,
            "source": login_source or None,
            "form": form or None,
            "cv_link": None,  
            "interest": None,  
            "qualification": None,  
            "date_joined": str(date_joined_str) if date_joined_str else None,
            "date": str(datetime.now().date()),
            "advert_detail": None if isinstance(advert, float) and math.isnan(advert) else advert,
        }


        url = 'https://crm.alnafi.com/api/resource/Lead?fields=["name","email_id"]&filters=[["Lead","email_id","=","{}"]]'.format(row['email'])

        response = requests.get(url, headers=headers)

        lead_data = response.json()

        if 'data' in lead_data:
            already_existed = len(lead_data["data"]) > 0
        else:
            already_existed = False

        failed_leads = []
        updated_leads = []
        if already_existed:
            updated_leads.append(data)
            # print("already exists")
            # # print("already exists")
            # auth_url = 'https://auth.alnafi.edu.pk/api/v1.0/enrollments/demo-user/'
            # enrollment_url = 'https://auth.alnafi.edu.pk/api/v1.0/enrollments/enrollment-user/'
            # auth_headers = {
            #     "Content-Type": "application/json",
            #     "Accept": "application/json",
            # }
            # query_parameters = {
            #     "email": lead_data['data'][0]['email_id']  # Replace with the actual email you want to send
            # }
            # demo_user = requests.get(auth_url, headers=auth_headers, params=query_parameters)
            # enrollment_user = requests.get(enrollment_url, headers=auth_headers, params=query_parameters)

            # if demo_user.status_code == 200:
            #     demo_data = demo_user.json()
            #     data['demo_product'] = demo_data['product_name']

            # if enrollment_user.status_code == 200:
            #     enrollment_data = enrollment_user.json()
            #     if len(enrollment_data['enrollments']) > 1:
            #         data['enrollment'] = enrollment_data['product_name']

            # email_id = lead_data['data'][0]['email_id']
            # url = f'https://crm.alnafi.com/api/resource/Lead/{email_id}'
            # # print(data)
            # response = requests.put(url, headers=headers, json=data)
            # if response.status_code != 200:
            #     response_data = json.loads(response.text)
            #     if "exception" in response_data and "DuplicateEntryError" in response_data["exception"]:
            #         pass
            #     else:
            #         # print(response.text)
            #         data['error'] = response.text
            #         data['status_code'] = response.status_code
            #         failed_leads.append(data)
            # else:
            with open('update_leads.csv', 'a', newline='') as csvfile:
                fieldnames = updated_leads[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            print(f"Already Exist {email}")
            print(f"updated {email}")
        else:
            # for i in range(1, leads_per_group * len(api_key_groups) + 1):
            post_url = 'https://crm.alnafi.com/api/resource/Lead'
            # print("headers", headers)
            response = requests.post(post_url, headers=headers, json=data)
            # print(response)
            if response.status_code != 200:
                # print("In If")
                response_data = json.loads(response.text)
                # print("response_data", response_data)
                if "exception" in response_data and "DuplicateEntryError" in response_data["exception"]:
                    print(f'This {email} Is Already There')
                    pass
                else:
                    data['error'] = response.text
                    data['status_code'] = response.status_code
                    # print(response.text)
                    failed_leads.append(data)
                    # print(response.text)
            else:
                print(f"sale doctype signal; lead created successfully {email}")

        if failed_leads:
            with open('failed_lead_from_script.csv', 'a', newline='') as csvfile:
                fieldnames = failed_leads[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if csvfile.tell() == 0:
                    writer.writeheader()

                for lead in failed_leads:
                    writer.writerow(lead)


upload_leads()



        
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


# give them leads till 8 march
# Zeeshan, Mehtab, haider bhai

#support 2 agents 30 leads fresh  Zeeshan, Mehtab, haider bhai
#hamza bhai 10 leads fresh
# haider bhai 10 leads fresh
# sales same process except hamza bhai
# remaining 4 support agents 10 leads old



def upload_leads():
    # data = pd.read_csv('/home/faizan/albaseer/Al-Baseer-Backend/lead bank - Lead Godaam.csv')
    data = pd.read_csv('/home/uzair/Documents/Al-Baseer-Backend/Today Lead.csv')
    # Iterate over rows in the DataFrame
    for index, row in data.iterrows():
        failed_leads = []

        #sales
        full_name = row['full_name']
        email = row['email']
        phone = row['phone']
        country = row['country']
        login_source = row['source']
        created_at_str = row['created_at']
        city = row['city']
        advert = row['advert']

        if pd.isna(created_at_str):
            created_at = datetime.now()
        else:
            created_at = pd.to_datetime(created_at_str, format="%Y-%m-%d %H:%M:%S.%f%z")

        form = row['form']
        form = None if pd.isna(form) else form


        # try:
        #     moc, created = Moc_Leads.objects.get_or_create(email=email, defaults={
        #         'first_name': full_name,
        #         'phone': phone,
        #         'email': email,
        #         'form': form,
        #         'country': country,
        #         'login_source': login_source,
        #         'created_at': created_at,
        #         'advert': advert,
        #         'city': city,
        #     })

        #     if not created:
        #         moc.first_name = full_name
        #         moc.email = email
        #         moc.phone = phone
        #         moc.form = form
        #         moc.country = country
        #         moc.login_source = login_source
        #         moc.created_at = created_at
        #         moc.advert = advert
        #         moc.city = city
        #         moc.save()
        # except Exception as e:
        #     pass
        



        #sales
        lead_data = {
            'full_name':row['full_name'],
            'email':row['email'],
            'phone': row['phone'],
            'country': row['country'],
            'login_source':row['source'],
            'created_at_str': row['created_at'], 
            'form': row['form'],
            'advert': row['advert'],
            'city': row['city']
        }


        ## For Old Leads Support
        # if index <= 10:
        #     user_api_key = 'ee3c9803e0a7aa0'
        #     user_secret_key = 'ad8a5dc4bc4f13f'
        #     print("mutahir")
        # elif index >= 10 and index < 20:
        #     user_api_key = 'c09e9698c024bd5'
        #     user_secret_key = '02c5e4ff622bb22'  
        #     print("salman")
        # elif index >= 20 and index < 30:
        #     user_api_key = 'b5658b2d5a087d0'
        #     user_secret_key = 'a9faaabc26bddc5' 
        #     print("ahsan") 
        # elif index >= 30 and index < 4:
        #     user_api_key = '940ef42feabf766'
        #     user_secret_key = '7a642a5b930eb44'
        #     print("mujtaba")
        #support
        # lead_data = {
        #     'full_name':row['first_name'],
        #     'email':row['email_id'],
        #     'phone': row['mobile_no'],
        #     'login_source':row['source'],
        #     'created_at_str': created_at, 
        #     'form': row['form'],
        #     'advert': row['advert_detail'],
        # }


        #SUpport keys
        # if index <= 9:
        # user_api_key = '2a1d467717681df'
        # user_secret_key = '39faa082ac5f258'
        # print("haider")
        # elif index >= 10 and index < 20:
        # user_api_key = 'ee3c9803e0a7aa0'
        # user_secret_key = 'ad8a5dc4bc4f13f'
        #     print("mutahir")
        # elif index >= 20 and index < 30:
        # user_api_key = 'a17f7cc184a55ec'
        # user_secret_key = '3e26bf2dde0db20'
        #     print("zeeshan")
        # elif index >= 30 and index < 40:
        # user_api_key = '6b0bb41dba21795'
        # user_secret_key = 'f56c627e47bdff6'
        #     print("mehtab")
        # elif index >= 40 and index < 50:
        # user_api_key = 'c09e9698c024bd5'
        # user_secret_key = '02c5e4ff622bb22'  
        #     print("salman")
        # elif index >= 50 and index < 60:
        # user_api_key = 'b5658b2d5a087d0'
        # user_secret_key = 'a9faaabc26bddc5' 
        #     print("ahsan") 
        # elif index >= 60 and index < 70:
        user_api_key = '940ef42feabf766'
        user_secret_key = '7a642a5b930eb44'
        #     print("mujtaba")


        
        # New Lead distribution keys concept for support
        # support 2 agents 30 leads fresh  Zeeshan, Mehtab

        # if index <= 10:
        #     user_api_key = 'a17f7cc184a55ec'
        #     user_secret_key = '3e26bf2dde0db20'
        #     print("zeeshan")
        # elif index >=10 and index <= 21:
        #     user_api_key = '2a1d467717681df'
        #     user_secret_key = '39faa082ac5f258'
        #     print("haider")
        # elif index >=21 and index <= 33:
        #     user_api_key = '6b0bb41dba21795'
        #     user_secret_key = 'f56c627e47bdff6'
        #     print("mehtab")
      
        
        #india leads
        #maarij hamza toqir sunil


      
        # if index <= 38:
        #     # Wamiq Keys
        #     user_api_key = '31c85c7e921b270'
        #     user_secret_key = '845aff8197932c3'
        # elif index >= 38 and index < 76: 
        #     # Saad Bhai Keys
        #     user_api_key = 'e31afcb884def7e'
        #     user_secret_key = 'cb799e6913b57f9'
        # elif index >= 76 and index < 114:
        #     # Saima Keys
        #     user_api_key = '3da0a250742fa00'
        #     user_secret_key = '5ec8bb8e1e94930'
        # elif index >= 114 and index < 152:
        #     # Shoaib keys
        #     user_api_key = '484f3e9978c00f3'
        #     user_secret_key = 'f61de5c03b3935d'
        # elif index >= 152 and index < 190:
        #     # Suleman Keys
        #     user_api_key = '3f6d0f005e4fccc'
        #     user_secret_key = 'bbcaef6140205d2'
        # elif index >= 190 and index < 228:
        #     # Ribal Keys
        #     user_api_key = '39d14c9d602fa09'
        #     user_secret_key = '216de0a015e7fd1'
        # elif index >= 228 and index < 266:
        #     # Waqas Kes
        #     user_api_key = 'b09d1796de6444a'
        #     user_secret_key = '9ac70da03e4c23c'
        # elif index >= 266 and index < 304:
        #     # Rehan Bhai keys
        #     user_api_key = 'b6a9a44a08790f8'
        #     user_secret_key = 'b6d91bfa5792ccc'
        # elif index >= 304 and index < 342:
        #     # Marij Keys
        #     user_api_key = 'b3bb7a167ec651a'
        #     user_secret_key = '449cd28cd263361'
        # elif index >= 342 and index < 342:
        #     # Sunil Keys
        #     user_api_key = '9d37a29d966277f'
        #     user_secret_key = '018c3f6127c43cc'
        # elif index >= 330 and index < 370:
        #     # Toqir Bhai keys
        #     user_api_key = '5306bb96b02c8f1'
        #     user_secret_key = '362d44b933cef9e'
            


        # if index <= 17:
        #     # Toqir Bhai keys
        # user_api_key = '5306bb96b02c8f1'
        # user_secret_key = '362d44b933cef9e'
        # elif index >= 17 and index <= 34: 
        #     # Saad Bhai Keys
        # user_api_key = 'e31afcb884def7e'
        # user_secret_key = 'cb799e6913b57f9'
        # elif index >= 34 and index <= 51:
        #     # Saima Keys
        # user_api_key = '3da0a250742fa00'
        # user_secret_key = '5ec8bb8e1e94930'
        # elif index >= 51 and index <= 68:
        #     # Shoaib keys
        # user_api_key = '484f3e9978c00f3'
        # user_secret_key = 'f61de5c03b3935d'
        # elif index >= 68 and index <= 85:
        #     # Suleman Keys
        # user_api_key = '3f6d0f005e4fccc'
        # user_secret_key = 'bbcaef6140205d2'
        # elif index >= 85 and index <= 102:
        #     # Ribal Keys
        # user_api_key = '39d14c9d602fa09'
        # user_secret_key = '216de0a015e7fd1'
        # elif index >= 102 and index <= 119:
        #     # Sunil Keys
        # user_api_key = '9d37a29d966277f'
        # user_secret_key = '018c3f6127c43cc'
        # elif index >= 119 and index <= 136:
        #     # Rehan Bhai keys
        # user_api_key = 'b6a9a44a08790f8'
        # user_secret_key = 'b6d91bfa5792ccc'
        # elif index >= 136 and index <= 153:
        #     # Marij Keys
        # user_api_key = 'b3bb7a167ec651a'
        # user_secret_key = '449cd28cd263361'
        # elif index >= 153 and index < 173:
        #     # Waqas Kes
        # user_api_key = 'b09d1796de6444a'
        # user_secret_key = '9ac70da03e4c23c'
        # elif index <= 173 and index < 198:
        # # Hamza Bhai keys only 10 leads indexes
        # user_api_key = 'dd3d10e83dfbb6b'
        # user_secret_key = 'a1a50d549455fe3'

        #maarij
        #rehan
        #hamza

        # if index <= 3:
        #     # Toqir Bhai keys
        #     user_api_key = '5306bb96b02c8f1'
        #     user_secret_key = '362d44b933cef9e'
        # elif index >= 3 and index < 7:
        #     user_api_key = 'dd3d10e83dfbb6b'
        #     user_secret_key = 'a1a50d549455fe3'
        # elif index >= 7 and index < 10:
        #     user_api_key = '9d37a29d966277f'
        #     user_secret_key = '018c3f6127c43cc'
        # elif index >= 10 and index < 14:
        #     user_api_key = 'b3bb7a167ec651a'
        #     user_secret_key = '449cd28cd263361'
        # elif index >= 135 and index < 152:
        #     # Wamiq Keys
        #     user_api_key = '31c85c7e921b270'
        #     user_secret_key = '845aff8197932c3'

    
        headers = {
            'Authorization': f'token {user_api_key}:{user_secret_key}',
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        # country_code = getattr(lead_data, 'country', "Unknown")
        country_code = lead_data['country']

        if isinstance(country_code, str):
            country_name = country_code
        else:
            if isinstance(country_code, (pd.DataFrame, pd.Series)):
                if not country_code.empty and country_code.notna().any():
                    country_name = None
                    if len(str(country_code.iloc[0])) <= 2:
                        for name, code in COUNTRY_CODES.items():
                            if code == country_code.iloc[0]:
                                country_name = name
                                break
                    else:
                        country_name = row['country']
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
            "country": 'unknown',
            "city": city or None,
            "source": login_source or None,
            "form": form or None,
            "cv_link": None,  
            "interest": None,  
            "qualification": None,  
            "date_joined": str(date_joined_str) if date_joined_str else None,
            "date": str(datetime.now().date()),
            "advert_detail": None if isinstance(advert, float) and math.isnan(advert) else advert,
        }

        for key, value in data.items():
            if pd.isna(value):
                data[key] = None

        url = 'https://crm.alnafi.com/api/resource/Lead?fields=["name","email_id"]&filters=[["Lead","email_id","=","{}"]]'.format(row['email'])

        response = requests.get(url, headers=headers)

        lead_data = response.json()

        if 'data' in lead_data:
            already_existed = len(lead_data["data"]) > 0
        else:
            already_existed = False

        failed_leads = []
        if already_existed:
            print(data['email_id'])
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
                else:
                    data['error'] = response.text
                    data['status_code'] = response.status_code
                    print(response.text)
                    failed_leads.append(data)
                    # print(response.text)
            else:
                print(f"lead created successfully {email}")

        if failed_leads:
            with open('failed_lead_from_script.csv', 'a', newline='') as csvfile:
                fieldnames = failed_leads[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if csvfile.tell() == 0:
                    writer.writeheader()

                for lead in failed_leads:
                    writer.writerow(lead)

upload_leads()

def upload_support_leads():
    data = pd.read_csv('/home/faizan/albaseer/Al-Baseer-Backend/MOC Leads - Al Baseer to CRM - Facebook.csv')
    # Iterate over rows in the DataFrame
    for index, row in data.iterrows():
        failed_leads = []

        # email_id,first_name,mobile_no,source,form,advert_detail
        #support
        # full_name = row['first_name']
        # email = row['email_id']
        # phone = row['mobile_no']
        # login_source = row['source']
        # advert = row['advert_detail']
        # created_at = datetime.now()

        form = row['form']
        form = None if pd.isna(form) else form


        #sales
        full_name = row['full_name']
        email = row['email']
        phone = row['phone']
        country = row['country']
        login_source = row['source']
        created_at_str = row['created_at']
        city = row['city']
        advert = row['advert']




        # try:
        #     moc, created = Moc_Leads.objects.get_or_create(email=email, defaults={
        #         'first_name': full_name,
        #         'phone': phone,
        #         'email': email,
        #         'form': form,
        #         'login_source': login_source,
        #         'created_at': created_at,
        #         'advert': advert,
        #     })

        #     if not created:
        #         moc.first_name = full_name
        #         moc.email = email
        #         moc.phone = phone
        #         moc.form = form
        #         moc.login_source = login_source
        #         moc.created_at = created_at
        #         moc.advert = advert
        #         moc.save()
        # except Exception as e:
        #     pass


        #support
        # lead_data = {
        #     'full_name':row['first_name'],
        #     'email':row['email_id'],
        #     'phone': row['mobile_no'],
        #     'login_source':row['source'],
        #     'created_at_str': created_at, 
        #     'form': row['form'],
        #     'advert': row['advert_detail'],
        # }


           #sales
        lead_data = {
            'full_name':row['full_name'],
            'email':row['email'],
            'phone': row['phone'],
            'country': row['country'],
            'login_source':row['source'],
            'created_at_str': row['created_at'], 
            'form': row['form'],
            'advert': row['advert'],
            'city': row['city']
        }



    
        ## For Old Leads Support
        # if index < 30:
        #     user_api_key = 'ee3c9803e0a7aa0'
        #     user_secret_key = 'ad8a5dc4bc4f13f'
        #     print("mutahir")
        # elif index >= 30 and index < 60:
        #     user_api_key = 'c09e9698c024bd5'
        #     user_secret_key = '02c5e4ff622bb22'  
        #     print("salman")
        # elif index >= 60 and index < 90:
            # user_api_key = 'b5658b2d5a087d0'
            # user_secret_key = 'a9faaabc26bddc5' 
            # print("ahsan") 
        # elif index >= 90 and index < 120:
            # user_api_key = '940ef42feabf766'
            # user_secret_key = '7a642a5b930eb44'
            # print("mujtaba")
        # elif index <= 120 and index < 150:
        # user_api_key = 'a17f7cc184a55ec'
        # user_secret_key = '3e26bf2dde0db20'
        # print("zeeshan")
        # elif index >=150 and index <= 181:
        # user_api_key = '6b0bb41dba21795'
        # user_secret_key = 'f56c627e47bdff6'
        # print("mehtab")

        user_api_key = 'c09e9698c024bd5'
        user_secret_key = '02c5e4ff622bb22'  
        print("salman")

        headers = {
            'Authorization': f'token {user_api_key}:{user_secret_key}',
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if 'created_at' in data and isinstance(data['created_at'], pd.Series) and pd.api.types.is_datetime64_any_dtype(data['created_at']):
            date_joined_str = data['created_at'].dt.strftime('%Y-%m-%d %H:%M:%S')
        else:
            date_joined_str = None

        data = {
            "first_name": full_name or None,
            "last_name": None,  
            "email_id": email or None,
            "mobile_no": str(phone) if phone else None,
            "country": 'unknown',
            "source": login_source or None,
            "form": form or None,
            "cv_link": None,
            "interest": None,  
            "qualification": None,  
            "date_joined": str(date_joined_str) if date_joined_str else None,
            "date": str(datetime.now().date()),
            "advert_detail": None if isinstance(advert, float) and math.isnan(advert) else advert,
        }

        for key, value in data.items():
            if pd.isna(value):
                data[key] = None

        url = 'https://crm.alnafi.com/api/resource/Lead?fields=["name","email_id"]&filters=[["Lead","email_id","=","{}"]]'.format(row['email'])

        response = requests.get(url, headers=headers)

        lead_data = response.json()

        if 'data' in lead_data:
            already_existed = len(lead_data["data"]) > 0
        else:
            already_existed = False

        failed_leads = []
        if already_existed:
            print(data['email_id'])
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
                else:
                    data['error'] = response.text
                    data['status_code'] = response.status_code
                    print(response.text)
                    failed_leads.append(data)
                    # print(response.text)
            else:
                print(f"lead created successfully {email}")

        if failed_leads:
            with open('failed_lead_from_script.csv', 'a', newline='') as csvfile:
                fieldnames = failed_leads[0].keys()
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if csvfile.tell() == 0:
                    writer.writeheader()

                for lead in failed_leads:
                    writer.writerow(lead)


# upload_support_leads()
                    


#40 hamza bhai 
                    

#haider bhai
# 30 support   Zeeshan, Mehtab,

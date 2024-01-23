import imp
from locale import currency
import os
import django
from faker import Faker
import random
from datetime import date, datetime, timedelta
import pandas as pd


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "albaseer.settings")  # Replace with your project's settings module
django.setup()


from user.models import Moc_Leads

def upload_leads():
    data = pd.read_csv('/home/faizan/albaseer/Al-Baseer-Backend/user/MOC Leads - Al Baseer to CRM - Facebook.csv')
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
        data = {
            'full_name':row['full_name'],
            'email':row['email'],
            'phone': row['phone'],
            'country': row['country'],
            'login_source':row['source'],
            'created_at_str': row['created_at'], 
            'form': row['form'],
            'advert': row['advert']
        }
        failed_leads.append(data)




        
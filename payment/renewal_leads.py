import sys
import os

sys.path.append('/home/faizan/albaseer/Al-Baseer-Backend')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'albaseer.settings')

import django
django.setup()

from payment.models import Renewal
import requests
import pandas as pd

# url = "https://stage-auth.alnafi.edu.pk/api/v1.0/enrollments/expiry_date_user/"
url = "https://auth.alnafi.edu.pk/api/v1.0/enrollments/expiry_date_user/"


response = requests.get(url)
data = response.json()

lst = []
for i in data:
    first_name = i['user_username']
    user_id = i['user_email']
    phone = i['user_phone']
    date_joined = i['user_date_joined']
    product_name = i['product_name']
    payment_date = i['payment_date']
    expiration_date = i['expiry_date']
    status = 'Active'

    # print("date_joined",date_joined)
    # print("payment_date",payment_date)
    # print("expiration_date",expiration_date)


    # print("date_joined",type(date_joined))
    # print("payment_date",type(payment_date))
    # print("expiration_date",type(expiration_date))
    
    # Remove everything after the date for date_joined
    date_joined = date_joined.split()[0]

    # Remove everything after the date for payment_date
    payment_date = payment_date.split()[0]

    # Remove everything after the date for expiration_date
    expiration_date = expiration_date.split()[0]

    # try:
    renewal = Renewal.objects.create(
        first_name=first_name,
        user_id=user_id,
        phone=phone,
        date_joined=date_joined,
        payment_date=payment_date,
        expiration_date=expiration_date,
        product_name=product_name,
        status=status
    )
    # except Exception as e:
    #     print(e)
    #     lst.append(i['email'])
        
    data_Frame = pd.DataFrame(lst)
    data_Frame.to_csv("error.csv")
    

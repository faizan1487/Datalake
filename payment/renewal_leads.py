from payment.models import Renewal
import requests
import pandas as pd

def handle():
    # url = "https://fc37-2400-adc1-175-d500-5cbe-3fd2-50b-5daa.ngrok-free.app/api/v1.0/enrollments/expiry_date_user/"
    url = "stage-api-al-baseer.alnafi.com/api/v1.0/enrollments/expiry_date_user/"
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
        
handle()
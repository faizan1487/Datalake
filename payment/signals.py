from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import requests
from .models import AlNafi_Payment,UBL_IPG_Payment,UBL_Manual_Payment,Stripe_Payment,Easypaisa_Payment
from rest_framework.response import Response
from requests.exceptions import RequestException
from user.models import Main_User
from django.core.cache import cache
from django.conf import settings
import json
from datetime import datetime
from user.constants import COUNTRY_CODES

@receiver(pre_save, sender=AlNafi_Payment)
def send_payment_post_request(sender, instance, **kwargs):
    # print("signal running")
    url = 'https://crm.alnafi.com/api/resource/Customer?limit_start=0&limit_page_length=5000'
    api_key = '2b4b9755ecc2dc7'
    api_secret = '8d71fb9b172e2aa'
    headers = {
        'Authorization': f'token {api_key}:{api_secret}',
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        payment_user = Main_User.objects.filter(email__iexact=instance.customer_email)
        # print(payment_user)
        # print(len(data['data']))
        for i in range(len(data['data'])):
            # print(payment_user)
            first_name = payment_user[0].first_name if payment_user[0].first_name else ''
            last_name = payment_user[0].last_name if payment_user[0].last_name else ''
            full_name = f'{first_name} {last_name}'.strip()
            
            # uncomment this check condition for customer
            if data['data'][i]['name'] == full_name:
                print("customer exists")
                payment = create_payment(instance,headers,payment_user)
                break
        else:
            lead_url = 'https://crm.alnafi.com/api/resource/Lead?limit_start=0&limit_page_length=5000'
            response = requests.get(lead_url, headers=headers)

            lead_data = response.json()
            # print(lead_data)
            # print("payment_user[0].erp_lead_id",payment_user[0].erp_lead_id)
            for i in range(len(lead_data['data'])):
                if lead_data['data'][i]['name'] == payment_user[0].erp_lead_id:
                    print("lead exists")
                    #createe customer with lead id
                    customer = create_customer(instance,headers,full_name,payment_user)
                    #then create payment from that customer
                    payment = create_payment(instance,headers,payment_user)
                    break
            else:
                #create lead
                # lead = create_lead(instance,headers,payment_user)
                #then create customer from that lead
                customer = create_customer(instance,headers,full_name,payment_user)
                #then create payment from that customer
                payment = create_payment(instance,headers,payment_user)
    except RequestException as e:
        print('Error occurred while making the request:', str(e))
        print('Error:', response.status_code)
        print('Error:', response.text) 
     
# def create_lead(instance,headers,payment_user):
#     # print("payment_user[0].source",payment_user[0].source)
#     # print("payment_user[0]",payment_user[0])
#     country_code = payment_user[0].country or None
#     country_name = None

#     if country_code:
#         for name, code in country_codes.items():
#             if code == country_code:
#                 country_name = name
#                 break

#     data = {
#         "first_name": payment_user[0].first_name or None,
#         "last_name": payment_user[0].last_name or None,
#         "email_id": payment_user[0].email or None,
#         "mobile_no": payment_user[0].phone or None,
#         "country": country_name or "Unknown",
#         "source": payment_user[0].source if hasattr(instance, 'source') else None
#         # Add other fields from the Main_User model to the data dictionary as needed
#     }

#     url = 'https://crm.alnafi.com/api/resource/Lead?limit_start=0&limit_page_length=5000&fields=["name","email_id"]'
#     response = requests.get(url, headers=headers)
#     lead_data = response.json()

#     try:
#     # for lead in lead_data['data']:
#     #     if lead['email_id'] == payment_user[0].email:
#     #         response = requests.put(url, headers=headers, json=data)
#     #         erp_lead_id = lead['name']
#     #         print("erp_lead_id",erp_lead_id)
#     #         payment_user[0].erp_lead_id = erp_lead_id
#     #         payment_user[0].save(update_fields=['erp_lead_id'])
#     #         # post_save.connect(send_alnafi_lead_post_request, sender=AlNafi_User)
#     #         print("lead updated")
#     #         break
#     # else:
#         lead_url = 'https://crm.alnafi.com/api/resource/Lead'
#         response = requests.post(lead_url, headers=headers, json=data)
#         response.raise_for_status()
#         if response.status_code == 200:
#             lead_data = response.json()
#             erp_lead_id = lead_data['data']['name']
#             if erp_lead_id:
#                 payment_user[0].erp_lead_id = erp_lead_id
#                 payment_user[0].save(update_fields=['erp_lead_id'])
#             print("Lead created successfully!")
#     except RequestException as e:
#         print('Error occurred while making the request:', str(e))
#         print('Error:', response.status_code)
#         print('Error:', response.text)
        

def create_customer(instance,headers,full_name,payment_user):
    customer_url = 'https://crm.alnafi.com/api/resource/Customer'
    # print("payment_user",payment_user)
    # print("payment_user[0].erp_lead_id",payment_user[0].erp_lead_id)
    country_code = payment_user[0].country or None
    country_name = None

    if country_code:
        for name, code in COUNTRY_CODES.items():
            if code == country_code:
                country_name = name
                break
    customer_data = {
        "customer_name": full_name or None,
        "customer_type": "Individual",
        "customer_group": "Commercial",
        "territory": country_name or "Unknown",
        "lead_name": payment_user[0].erp_lead_id,
    }

    response = requests.post(customer_url, headers=headers, json=customer_data)
    if response.status_code == 200:
        print("Customer created successfully!")
    else:
        print('Error occurred while creating customer:')      
        print('Error:', response.status_code)
        print('Error:', response.text)


def create_payment(instance,headers,payment_user):
    first_name = payment_user[0].first_name if payment_user[0].first_name else ''
    last_name = payment_user[0].last_name if payment_user[0].last_name else ''
    full_name = f'{first_name} {last_name}'.strip()

    #account paid from Debtor  - A (pkr) or Debtors - B - A(usd)
    #account paid to Bank Account - A (pkr) or Back - Account - B - A (usd)
    usd_rate = get_USD_rate()
    plan = ""

    if "monthly" in instance.product_name.lower():
        plan = "Monthly"
    elif "half yearly" in instance.product_name.lower():
        plan = "Half Yearly"
    elif "yearly" in instance.product_name.lower() or "annual" in instance.product_name.lower():
        plan = "Yearly"
    elif "18 Months" in instance.product_name.lower():
        plan = "18 Months"
    elif "quarterly" in instance.product_name.lower():
        plan = "Quarterly"


    data1 = {
        "payment_type": "Receive",
        "posting_date": str(instance.order_datetime),
        "product_name": instance.product_name or "Test",
        "mode_of_payment": instance.source or "Unknown",
        "customer_email": instance.customer_email or "Test@example.com",
        "al_nafi_payment_id": instance.payment_id,
        "plan": plan,
        "party_type": "Customer",
        "party": full_name,
        "party_name": full_name,
        "paid_from": "",
        "paid_to": "Bank Account - A",
        "paid_amount": instance.amount_usd if instance.amount_usd != 0 else instance.amount_pkr,
        "received_amount": instance.amount_usd * usd_rate['PKR'] if instance.amount_usd != 0 else instance.amount_pkr,
        "source_exchange_rate": usd_rate['PKR'],
        "reference_no": instance.payment_id,
        "reference_date": str(instance.created_at) if instance.created_at is not None else str(datetime.now()),
    }
    # print("instance.amount_usd",instance.amount_usd)
    # print('instance.amount_pkr',instance.amount_pkr)
    # print("received_amount",data1["received_amount"])
    # print("data1[paid_amount]",data1["paid_amount"])
    if instance.amount_pkr == 0:
        data1["paid_from"] = "Debtors - B - A"
    else:
        data1["paid_from"] = "Debtors - A"
    # print("paid from",data1["paid_from"])
    
    url = 'https://crm.alnafi.com/api/resource/Payment Entry?fields=["al_nafi_payment_id"]&limit_start=0&limit_page_length=5000'
    response = requests.get(url, headers=headers)
    payment_data = response.json()
    # print("payment_data",payment_data)
    # print("len payment data",len(payment_data['data']))
    try: 
        url = 'https://crm.alnafi.com/api/resource/Payment Entry'
        
        payment_id = instance.payment_id
        for item in payment_data['data']:
            # print(type(item['al_nafi_payment_id']))
            # print("payment id",type(payment_id))
            if item['al_nafi_payment_id'] == str(payment_id):
                print("put request")
                # Perform the desired action when the payment_id matches
                # response = requests.post(url, headers=headers, json=data1)
                response = requests.put(url, headers=headers, json=data1)
                print("Payment ID found!")
                break
        else:
            # response = requests.post(url, headers=headers, json=data1)
            response = requests.post(url, headers=headers, json=data1)
            # response.raise_for_status() 
            response.raise_for_status() 
            # payment_data = response.json()
            payment_data = response.json()
            # print(payment_data)
            if response.status_code == 200:
                # response.status_code == 200 & 
                print("Payment created successfully!")     
    except RequestException as e:
        print('Error occurred while creating payment:', str(e)) 
        print('Error:', response.status_code)
        print('Error:', response.text)


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




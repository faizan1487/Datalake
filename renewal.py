import pandas as pd
import requests
## For uploading REnewal Academy LEads ###
# def post_data_for_academy_renewal():
#     url = 'https://crm.alnafi.com/api/resource/Renewal Leads'
#     user_api_key = '2a1d467717681df'
#     user_secret_key = '39faa082ac5f258'

#     headers = {
#         'Authorization': f'token {user_api_key}:{user_secret_key}',
#         'Content-Type': 'application/json',
#         'Accept': 'application/json',
#     }
#     data = pd.read_csv('/home/uzair/Documents/Al-Baseer-Backend/REnewal.csv')
#     for index, row in data.iterrows():
#         first_name = row['name']
#         user_id = row['email']
#         phone = row['phone']
#         date_joined = row['date_joined']
#         product_name = row['product_name']
#         payment_date = row['payment_date']
#         expiration_date = row['expiry_date']
#         status = row['status']

#         date_joined = date_joined.split()[0]

#         # Remove everything after the date for payment_date
#         payment_date = payment_date.split()[0]

#         # Remove everything after the date for expiration_date
#         expiration_date = expiration_date.split()[0]
#         renewal = {
#             'first_name': first_name,
#             'user_id': user_id,
#             'phone': phone,
#             'date_joined': date_joined,
#             'payment_date': payment_date,
#             'expiration_date': expiration_date,
#             'product_name': product_name,
#             'status': status
#         }

#         response = requests.post(url, headers=headers, json=renewal)
#         print(response.status_code)
#         print(response.text)

# post_data_for_academy_renewal()

#####For upload sales lead For one user#######
def upload_sales_lead():
    url = 'https://crm.alnafi.com/api/resource/Lead'
    user_api_key = 'b09d1796de6444a'
    user_secret_key = '9ac70da03e4c23c'

    headers = {
        'Authorization': f'token {user_api_key}:{user_secret_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    data = pd.read_csv('/home/uzair/Documents/Al-Baseer-Backend/Lead.csv')
    for index, row in data.iterrows():
        first_name = str(row['first_name'])
        email = str(row['email'])
        phone = str(row['phone'])
        source = str(row['source'])
        status = str(row['status'])
        print(source)
        lead = {
            'first_name': first_name,
            'email_id': email,
            'source': source,
            'status': status,
            'phone': phone,
        }
        print("lead", lead)
        response = requests.post(url, headers=headers, json=lead)
        print(response.status_code)
        print(response.text)
upload_sales_lead()


import imp
from locale import currency
import os
import django
from faker import Faker
import random
from datetime import datetime, timedelta

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "albaseer.settings")  # Replace with your project's settings module
django.setup()

# # Import your model
# from payment.models import Main_Payment  # Replace 'your_app' with the name of your Django app
# from user.models import Main_User
# from products.models import Main_Product
# # Create a Faker instance
# fake = Faker()

# Define a function to add fake data to the Main_Payment model
# def add_fake_payment_data(num_records,products,users):
#     for _ in range(num_records):
#         user_instance = random.choice(users)  # Select a random user from the list
#         payment = Main_Payment(
#             source_payment_id=fake.uuid4(),
#             alnafi_payment_id=fake.uuid4(),
#             easypaisa_ops_id=fake.uuid4(),
#             easypaisa_customer_msidn=fake.phone_number(),
#             card_mask=fake.credit_card_number(card_type="mastercard"),
#             user=user_instance,  # You may need to create user instances and assign them here
#             amount=fake.random_int(min=1, max=1000),
#             currency=fake.currency_code(),
#             source=fake.word(),
#             internal_source=fake.word(),
#             status=random.choice(["Pending", "Successful", "Failed"]),
#             order_datetime=fake.date_time_between(start_date="-1y", end_date="now"),
#             expiration_datetime=fake.date_time_between(start_date="now", end_date="+1y"),
#             activation_datetime=fake.date_time_between(start_date="now", end_date="+1y"),
#             token_paid_datetime=fake.date_time_between(start_date="now", end_date="+1y"),
#             easypaisa_fee_pkr=fake.random_int(min=1, max=100),
#             easypaisa_fed_pkr=fake.random_int(min=1, max=100),
#             ubl_captured=fake.word(),
#             ubl_reversed=fake.word(),
#             ubl_refund=fake.word(),
#             ubl_approval_code=fake.word(),
#             description=fake.sentence(),
#             qarz=fake.boolean(),
#             remarks=fake.text(),
#             payment_proof=fake.uri(),
#             send_invoice=fake.boolean(),
#             pk_invoice_number=fake.random_int(min=1000, max=9999),
#             us_invoice_number=fake.random_int(min=1000, max=9999),
#             sponsored=fake.boolean(),
#             coupon_code=fake.word(),
#             is_upgrade_payment=fake.boolean(),
#             affiliate=fake.word(),
#             candidate_name=fake.name(),
#             ubl_depositor_name=fake.name(),
#             candidate_phone=fake.phone_number(),
#             bin_bank_name=fake.word(),
#             error_reason=fake.sentence(),
#         )

#         payment.save()
#         # Assign one or more Main_Product instances to the product field
#         product_list = list(products)
#         random_products = random.sample(product_list, k=random.randint(1, len(product_list)))
#         payment.product.set(random_products)
#         payment.save()

# if __name__ == "__main__":
#     num_records_to_create = 100  # Adjust the number of records you want to create
#     products = Main_Product.objects.all()
#     users = Main_User.objects.all()
#     add_fake_payment_data(num_records_to_create,products,users)
#     print(f"Added {num_records_to_create} fake Main_Payment records.")


#=====================================================================================================



# import pandas as pd

# # Load your CSV file into a DataFrame
# df = pd.read_csv("/home/faizan/albaseer/Al-Baseer-Backend/Leads - Al Baseer to CRM - O Levels.csv")

# # Parse the date_joined column into datetime objects
# df['date_joined'] = pd.to_datetime(df['date_joined'], format='%Y-%m-%dT%H:%M:%S%z')

# # Convert the datetime objects to the "yyyy-mm-dd" format
# df['date_joined'] = df['date_joined'].dt.strftime('%Y-%m-%d')

# # Save the DataFrame back to a CSV file
# df.to_csv("/home/faizan/albaseer/Al-Baseer-Backend/new_file.csv", index=False)


#===========================================================================================

# import pandas as pd

# def find_unique_records(file1, file2, email_column='email'):
#     # Read CSV files into pandas DataFrames
#     df1 = pd.read_csv(file1)
#     df2 = pd.read_csv(file2)

#     # Identify records in the first file that are not in the second file
#     unique_records_file1 = df1[~df1[email_column].isin(df2[email_column])]

#     return unique_records_file1

# # Replace 'file1.csv' and 'file2.csv' with the actual file paths
# file1_path = '/home/faizan/albaseer/Al-Baseer-Backend/expired_auth.csv'
# file2_path = '/home/faizan/albaseer/Al-Baseer-Backend/Renewed_Payments_2023-12-13_05-03-02.csv'

# unique_records_file1 = find_unique_records(file1_path, file2_path)

# # Save the unique records to a new CSV file
# unique_records_file1.to_csv('expired_present_auth_missing_albaseer.csv', index=False)


# import pandas as pd

# def find_common_records(file1, file2, email_column='email'):
#     # Read CSV files into pandas DataFrames
#     df1 = pd.read_csv(file1)
#     df2 = pd.read_csv(file2)

#     # Identify records that are common in both files
#     common_records = pd.merge(df1, df2, on=email_column, how='inner', indicator=True).query("_merge == 'both'").drop('_merge', axis=1)

#     return common_records

# # Replace 'file1.csv' and 'file2.csv' with the actual file paths
# file1_path = '/home/faizan/albaseer/Al-Baseer-Backend/expired_auth.csv'
# file2_path = '/home/faizan/albaseer/Al-Baseer-Backend/renewed_auth.csv'

# common_records = find_common_records(file1_path, file2_path)

# # Save the common records to a new CSV file
# common_records.to_csv('common_records.csv', index=False)


# import csv
# import datetime
# import requests
import csv
import datetime
from doctest import REPORT_CDIFF
import requests

# def get_and_save_all_lead_data():

#     user_api_key = '4e7074f890507cb'
#     user_secret_key = 'c954faf5ff73d31'

#     headers = {
#         'Authorization': f'token {user_api_key}:{user_secret_key}',
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#     }

#     # Construct the URL to get leads
#     get_url = f'https://crm.alnafi.com/api/resource/Lead?fields=["email_id","status","date","lead_creator"]&limit_start=0&limit_page_length=10000000'

#     # Make the API request
#     response = requests.get(get_url, headers=headers)

#     if response.status_code == 200:
#         leads_data = response.json()

#         if 'data' in leads_data:
#             leads = leads_data['data']

#             # Get today's date
#             today_date = datetime.date.today()

#             # Calculate 3 days before today
#             three_days_before = today_date - datetime.timedelta(days=3)

#             # Filter leads with status 'Lead' and date 3 days before today
#             filtered_leads = [
#                 lead for lead in leads 
#                 if lead.get('status') == 'Lead'
#                 and lead.get('lead_creator') != 'haider.raza@alnafi.edu.pk' 
#                 and lead.get('date') is not None 
#                 and datetime.datetime.strptime(lead.get('date'), '%Y-%m-%d').date() == three_days_before
#             ]

#             print(f"Total number of leads with status 'Lead' and date 3 days before today: {len(filtered_leads)}")

#             # Save filtered leads to a CSV file
#             with open('leads_with_status_lead_3_days_before.csv', 'w', newline='') as csvfile:
#                 fieldnames = ['Email', 'Status', 'Assigned Date', 'Lead Owner']
#                 writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
#                 writer.writeheader()
#                 for lead in filtered_leads:
#                     lead_id = lead.get('email_id')
#                     lead_status = lead.get('status')
#                     lead_date = lead.get('date')
#                     lead_creator = lead.get('lead_creator')
#                     writer.writerow({'Email': lead_id, 'Status': lead_status, 'Assigned Date': lead_date, 'Lead Owner': lead_creator})

#             print("Filtered leads data saved to 'leads_with_status_lead_3_days_before.csv'")
#         else:
#             print("No leads found in the response.")
#     else:
#         print("Failed to fetch data. Status code:", response.status_code)

# get_and_save_all_lead_data()
# import csv
# import datetime
# import requests

# def get_and_save_all_lead_data():
#     user_api_key = '4e7074f890507cb'
#     user_secret_key = 'c954faf5ff73d31'

# =========================================================================================================

#extract leads from crm with status lead and with no comments
#then delete them from crm or send put request and assign those leads to admin
#or send delete request with id to delete those leads

from datetime import datetime
import requests
import pandas as pd
import csv
import json


# def fetch_idol_leads():
#     print("fetch_idol_leads")
#     # Admin keys
#     user_api_key = '4e7074f890507cb'
#     user_secret_key = 'c954faf5ff73d31'
    
#     # url = 'https://crm.alnafi.com/api/resource/Lead?fields=["first_name","status","lead_creator","phone","country","email_id","form","advert_detail","product_names_list","source","notes","`tabCRM Note`.note","`tabCRM Note`.added_on","`tabCRM Note`.added_by"]&filters=[["Lead","status","=","Lead"]]&limit_start=0&limit_page_length=10000000'


#     url = 'https://crm.alnafi.com/api/resource/Lead?fields=["first_name","status","lead_creator","phone","date","country","email_id","form","product_names_list","demo_product","enrollment","interest","qualification","cv_link","source","notes","`tabCRM Note`.note","`tabCRM Note`.added_on","`tabCRM Note`.added_by"]&filters=[["Lead","status","=","Lead"]]&limit_start=0&limit_page_length=10000000'


    
#     headers = {
#         'Authorization': f'token {user_api_key}:{user_secret_key}',
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#     }

#     # Construct the URL to get leads
#     get_url = f'https://crm.alnafi.com/api/resource/Lead?fields=["email_id","status","date","lead_creator"]&limit_start=0&limit_page_length=10000000'

#     # Make the API request
#     response = requests.get(get_url, headers=headers)

#     if response.status_code == 200:
#         leads_data = response.json()

#         if 'data' in leads_data:
#             leads = leads_data['data']

#             # Get today's date
#             today_date = datetime.date.today()

#             # Calculate 3 days before today
#             three_days_before = today_date - datetime.timedelta(days=3)

#             # Group leads by lead_creator
#             leads_by_creator = {}
#             for lead in leads:
#                 if lead.get('status') == 'Lead' and lead.get('date') is not None:
#                     lead_date = datetime.datetime.strptime(lead.get('date'), '%Y-%m-%d').date()
#                     if lead_date == three_days_before and lead.get('lead_creator') != 'haider.raza@alnafi.edu.pk':
#                         lead_creator = lead.get('lead_creator')
#                         if lead_creator not in leads_by_creator:
#                             leads_by_creator[lead_creator] = []
#                         leads_by_creator[lead_creator].append(lead)

#             print(f"Total number of leads with status 'Lead' and date 3 days before today: {len(leads)}")

#             # Save leads to separate CSV files based on lead_creator
#             for creator, creator_leads in leads_by_creator.items():
#                 filename = f"leads_{creator.replace('@', '_').replace('.', '_')}_3_days_before.csv"
#                 with open(filename, 'w', newline='') as csvfile:
#                     fieldnames = ['Email', 'Status', 'Assigned Date', 'Lead Owner']
#                     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#                     writer.writeheader()
#                     for lead in creator_leads:
#                         lead_id = lead.get('email_id')
#                         lead_status = lead.get('status')
#                         lead_date = lead.get('date')
#                         lead_creator = lead.get('lead_creator')
#                         writer.writerow({'Email': lead_id, 'Status': lead_status, 'Assigned Date': lead_date, 'Lead Owner': lead_creator})

#                 print(f"Filtered leads data for {creator} saved to '{filename}'")
#         else:
#             print("No leads found in the response.")
#     else:
#         print("Failed to fetch data. Status code:", response.status_code)

# get_and_save_all_lead_data()
#     response = requests.get(url, headers=headers)
#     lead_data = json.loads(response.text)

#     if 'data' in lead_data:
#         lead_data = lead_data['data']

#         if lead_data:
#             # Create an empty dictionary to store data
#             data_dict = {}

#             # Loop through the response data
#             for item in lead_data:
#                 for key, value in item.items():
#                     if key in data_dict:
#                         data_dict[key].append(value)
#                     else:
#                         data_dict[key] = [value]

#             # Create a DataFrame from the dictionary
#             df = pd.DataFrame(data_dict)

#             # Define the CSV file name
#             csv_filename = 'all_lead_data.csv'

#             # Save the data to a CSV file with column names
#             df.to_csv(csv_filename, index=False)

#             print(f"Data saved to {csv_filename}")
#         else:
#             print("No data found in the response.")
#     else:
#         print(response.text)
#         print("The 'data' key is missing in the response.")



#     #Loop over the leads data and delete those leads which don't have a comment
        
#     # data = response.json()
#     # for i in data['data']:
#     #     if not i['note']:
#     #         email = i['email_id']  
#     #         delete_url = f'https://crm.alnafi.com/api/resource/Lead/{email}'
#     #         response = requests.delete(delete_url, headers=headers)
#     #         print(response.text)



# fetch_idol_leads()

#============================================================================================

# import sys
# import os

# sys.path.append('/home/faizan/albaseer/Al-Baseer-Backend')  # Add your project directory

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'albaseer.settings')

# import django
# django.setup()

import datetime
import requests
import json
import random
# import requests
# import pandas as pd
# from secrets_api.algorithem import round_robin_support

#upload renewal leads to crm

# def support_renewal_leads():
#     crm_endpoint = 'https://crm.alnafi.com/api/resource/Renewal Leads'

#     data = pd.read_csv('/home/faizan/albaseer/Al-Baseer-Backend/dec_file.csv')
#     for index, row in data.iterrows():
#         # api_key = '2a1d467717681df'
#         # api_secret = '39faa082ac5f258'

#         #Admin keys
#         api_key = '4e7074f890507cb'
#         api_secret = 'c954faf5ff73d31'
#         email = row['email']
#         product_name = row['product__product_name']

#         print("email",email)

#         url = f'https://crm.alnafi.com/api/resource/Renewal Leads?fields=["name","user_id"]&filters=[["Renewal Leads","user_id","=","{email}"],["Renewal Leads","product_name","=","{product_name}"]]'


#         headers = {
#             'Authorization': f'token {api_key}:{api_secret}',
#             "Content-Type": "application/json",
#             "Accept": "application/json",
#         }

#         response = requests.get(url, headers=headers)
#         data = response.json()
#         already_existed = len(data["data"]) > 0


#         if not already_existed:
#             order_datetime_str = row['order_datetime']
#             expiration_datetime_str = row['expiration_datetime']

#             # # Convert strings to datetime objects
#             # # order_datetime_str = order_datetime_str.rsplit('.', 1)[0]  # Remove fractional seconds if present
#             # order_datetime = datetime.strptime(order_datetime_str, '%Y-%m-%d %H:%M:%S.%f%z')
#             # expiration_datetime = datetime.strptime(expiration_datetime_str, '%Y-%m-%d %H:%M:%S%z')

#             # # Format datetime objects to strings with only the date part
#             # order_date_str = order_datetime.strftime('%Y-%m-%d')
#             # expiration_date_str = expiration_datetime.strftime('%Y-%m-%d')


#             data = {
#                 "first_name": row['name'] or None,
#                 # "last_name": row['last_name'] or None,
#                 "user_id": row['email'] or None,
#                 "phone": row['phone'] if row['phone'] else None,
#                 "country": row['country'] or "Unknown",
#                 # "address": row['address'] or None,
#                 # "date_joined": row['date_joined'],
#                 "payment_date": order_datetime_str,
#                 "expiration_date": expiration_datetime_str,
#                 "product_name": row['product__product_name'] or None,
#                 "status": 'Expired',
#                 "assigned_date": datetime.now().date().isoformat()
#             }

#             failed_leads = []

#             api_key, api_secret = round_robin_support()
#             headers = {
#             'Authorization': f'token {api_key}:{api_secret}',
#             "Content-Type": "application/json",
#             "Accept": "application/json",
#             }

#             try:
#                 response = requests.post(crm_endpoint, headers=headers, json=data)
#             except Exception as e:
#                 failed_leads.append(data)
            
#             if response.status_code != 200:
#                 pass
#             else:
#                 print("lead created successfully")



#     if failed_leads:
#         with open('failed_renewal_leads.csv', 'w', newline='') as csvfile:
#             fieldnames = failed_leads[0].keys()
#             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#             writer.writeheader()
#             for lead in failed_leads:
#                 writer.writerow(lead)



# support_renewal_leads()



#================================================================================

from numpy import nan, source

# Script to import easy pay leads

def sale_easy_pay_leads():
    # print("func running")
    crm_endpoint = 'https://crm.alnafi.com/api/resource/Lead'
    support_endpoint = 'https://crm.alnafi.com/api/resource/Suppport'

    sales_email_keys = {
        "Hamza": ("dd3d10e83dfbb6b", "a1a50d549455fe3"),
        "Muzammil": ("b6d818ef8024f5a", "ce1749a7dcf8577"),
        "Ribal": ("39d14c9d602fa09", "216de0a015e7fd1"),
        "Saad": ("e31afcb884def7e", "cb799e6913b57f9"),
        "Saima": ("3da0a250742fa00", "5ec8bb8e1e94930"),
        "Shoaib": ("484f3e9978c00f3","f61de5c03b3935d"),
        "Sufyan": ("ae5b7895b8b9ba8","da5406f0c217a40"),
        "Wamiq": ("31c85c7e921b270", "845aff8197932c3"),
        "Waqas" : ("b09d1796de6444a", "9ac70da03e4c23c"),
    }

    support_email_keys = {
        "Ahsan": ("b5658b2d5a087d0","a9faaabc26bddc5"),
        "Haider": ("2a1d467717681df", "39faa082ac5f258"),
        "Mehtab": ("6b0bb41dba21795","f56c627e47bdff6"),
        "Mujtaba": ("940ef42feabf766","7a642a5b930eb44"),
        "Mutahir": ("ee3c9803e0a7aa0","ad8a5dc4bc4f13f"),
        "Salman": ("c09e9698c024bd5","02c5e4ff622bb22"),
        "Zeeshan": ("a17f7cc184a55ec","3e26bf2dde0db20"),

    }



    # data = pd.read_csv('/home/faizan/albaseer/Al-Baseer-Backend/Again_Easy_format_leads.csv')

    # data = pd.read_csv('/home/faizan/albaseer/Al-Baseer-Backend/Again_Easy_format_leads (copy).csv')

    data = pd.read_csv('/home/faizan/albaseer/Al-Baseer-Backend/support_failed_easy_pay_leads.csv')

    data = data.applymap(lambda x: None if pd.isna(x) else x)

    support_names = ['Ahsan','Haider','Mehtab','Mujtaba','Mutahir','Salman','Zeeshan']

    # Iterate over rows in the DataFrame
    for index, row in data.iterrows():
        failed_leads = []
        name = row['assigned_agent']

        if name in support_names:
            # first_name = row['full_name']
            # email = row['email']
            # phone = row['phone']
            # form = row['form']
            # country = row['country']
            # advert_detail = row['advert detail']
            # source = row['source']
            # created_at = row['formatted_date']
            # assigned_date = row['formatted_assigned_date']
            # # comments_by_Agent = row['Comments by Agent']
            # first_follow_up = row['1st Follow Up']
            # second_follow_up = row['2nd Follow Up']
            # third_follow_up = row['3rd Follow Up']
            # fourth_follow_up = row['4th Follow Up']
            # status = row['Status']
            # comment = row['Comments by Agent']

            #from failed lead csv file
            first_name = row['first_name'] or None
            email = row['customer_email'] or None
            phone = row['contact_no'] or None
            form = row['form'] or None
            country = row['country'] or None
            advert_detail = row['advert_detail'] or None
            source = row['source'] or None
            created_at = row['created_at'] or None
            assigned_date = row['assigned_date'] or None
            # comments_by_Agent = row['Comments by Agent']
            first_follow_up = row['first_follow_up_date'] or None
            second_follow_up = row['second_follow_up_date'] or None
            third_follow_up = row['third_follow_up_date'] or None
            fourth_follow_up = row['fourth_follow_up_date'] or None
            status = row['lead_status']
            # comment = row['Comments by Agent']

            data = {
                "first_name": first_name,
                "customer_email": email,
                "contact_no": str(phone),
                "form": form,
                "country": country,
                "advert_detail":advert_detail,
                "source": source,
                "created_at":created_at,
                "payment": assigned_date,
                "first_follow_up_date":first_follow_up,
                "second_follow_up_date":second_follow_up,
                "third_follow_up_date":third_follow_up,
                "fourth_follow_up_date":fourth_follow_up,
                "lead_status": status,
                "expiration_status": "Active"
            }

            url = f'https://crm.alnafi.com/api/resource/Suppport?fields=["customer_email"]&filters=[["Suppport","customer_email","=","{email}"],["Suppport","form","=","{form}"]]'

            user_api_key = '4e7074f890507cb'
            user_secret_key = 'c954faf5ff73d31'

            admin_headers = {
                'Authorization': f'token {user_api_key}:{user_secret_key}',
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            response = requests.get(url, headers=admin_headers)
            lead_data = response.json()

            try:
                if lead_data["data"]:
                    already_existed = len(lead_data["data"]) > 0
                else:
                    already_existed = False
            except KeyError:
                # Handle the case when "data" key is not present in lead_data
                already_existed = False

            if not already_existed:
                post_api_key, post_secret_key = support_email_keys[name]
                headers = {
                    'Authorization': f'token {post_api_key}:{post_secret_key}',
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                }

                response = requests.post(support_endpoint, headers=headers, json=data)
                if response.status_code != 200:
                    # print(email)
                    # print(data)
                    # print(name)
                    print(response.text)
                    # response_data = json.loads(response.text)
                    # if "exception" in response_data and "DuplicateEntryError" in response_data["exception"]:
                    #     pass
                    # else:

                    #     data['assigned_agent'] = name   
                    #     data['Comments by Agent'] = comment 
                    #     data['error'] = response.text
                    #     data['status_code'] = response.status_code     
                    #     # failed_leads.append(data)
                else:
                    print(f"lead created succesfully {email}")
        else:
            pass
            # print(f"name in sales {name}")
            # Extracting data from the row
            # first_name = row['full_name'] or None
            # email = row['email'] or None
            # phone = row['phone'] or None
            # form = row['form'] or None
            # country = row['country'] or None
            # advert_detail = row['advert detail'] or None
            # source = row['source'] or None
            # created_at = row['formatted_date'] or None
            # assigned_date = row['formatted_assigned_date'] or None
            # # comments_by_Agent = row['Comments by Agent']
            # first_follow_up = row['1st Follow Up'] or None
            # second_follow_up = row['2nd Follow Up'] or None
            # third_follow_up = row['3rd Follow Up'] or None
            # fourth_follow_up = row['4th Follow Up'] or None
            # status = row['Status']
            # comment = row['Comments by Agent']

            #from failed lead csv file
            # first_name = row['first_name'] or None
            # email = row['email_id'] or None
            # phone = row['phone'] or None
            # form = row['form'] or None
            # country = row['country'] or None
            # advert_detail = row['advert_detail'] or None
            # source = row['source'] or None
            # created_at = row['created_at'] or None
            # assigned_date = row['date'] or None
            # # comments_by_Agent = row['Comments by Agent']
            # first_follow_up = row['first_follow_up_date'] or None
            # second_follow_up = row['second_follow_up_date'] or None
            # third_follow_up = row['third_follow_up_date'] or None
            # fourth_follow_up = row['fourth_follow_up_date'] or None
            # status = row['status']
            # # comment = row['Comments by Agent']

            # data = {
            #     "first_name": first_name,
            #     "lead_name": first_name,
            #     "email_id": email,
            #     "phone": str(phone),
            #     "form": form,
            #     "country": country,
            #     "advert_detail":advert_detail,
            #     "source": source,
            #     "created_at":created_at,
            #     "date": assigned_date,
            #     "first_follow_up_date":first_follow_up,
            #     "second_follow_up_date":second_follow_up,
            #     "third_follow_up_date":third_follow_up,
            #     "fourth_follow_up_date":fourth_follow_up,
            #     "status": status
            # }


            # post_api_key, post_secret_key = sales_email_keys[name]

            # headers = {
            #     'Authorization': f'token {post_api_key}:{post_secret_key}',
            #     "Content-Type": "application/json",
            #     "Accept": "application/json",
            # }

            # response = requests.post(crm_endpoint, headers=headers, json=data)

            # if response.status_code != 200:
            #     response_data = json.loads(response.text)
            #     if "exception" in response_data and "DuplicateEntryError" in response_data["exception"]:
            #         pass
            #     else:
            #         # data['assigned_agent'] = name   
            #         # data['Comments by Agent'] = comment    
            #         # data['error'] = response.text
            #         # data['status_code'] = response.status_code
            #         # failed_leads.append(data)
            # else:
            #     print(f"lead created succesfully {email}")
   
        # if failed_leads:
        #     # print("failed leads exits")
        #     with open('support_failed_easy_pay_leads.csv', 'a', newline='') as csvfile:
        #         fieldnames = failed_leads[0].keys()
        #         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        #         # Check if the file is empty, and write header only if it's a new file
        #         if csvfile.tell() == 0:
        #             writer.writeheader()

        #         for lead in failed_leads:
        #             writer.writerow(lead)

sale_easy_pay_leads()

#=================================================================================

#SCRIPT TO IMPORT COMMENTS

#import comments to crm
from datetime import datetime
import requests
import requests
import pandas as pd

# def crmnote():
#     #   haider bhai keys
#     # user_api_key = '2a1d467717681df'
#     # user_secret_key = '39faa082ac5f258'

#     # Admin keys
#     api_key = '4e7074f890507cb'
#     api_secret = 'c954faf5ff73d31'

#     headers = {
#         'Authorization': f'token {api_key}:{api_secret}',
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#     }

#     # data = pd.read_csv('/home/faizan/albaseer/Al-Baseer-Backend/Easy_pay_leads_comments.csv')
#     data = pd.read_csv('/home/faizan/albaseer/Al-Baseer-Backend/support_failed_easy_pay_comments.csv')

#     support_emails = ['ahsan.ali@alnafi.edu.pk','haider.raza@alnafi.edu.pk','mehtab.sharif@alnafi.edu.pk','mujtaba.jawed@alnafi.edu.pk','mutahir.hassan@alnafi.edu.pk','salman.amjad@alnafi.edu.pk','zeeshan.mehr@alnafi.edu.pk']

#     post_url = 'https://crm.alnafi.com/api/resource/Comment'

#     for index, row in data.iterrows():
#         failed_leads = []

#         # parent = row['parent']
#         # owner = row['owner']
#         # note = row['note']
#         # form = row['form']

#         parent = row['parent']
#         owner = row['comment_by']
#         note = row['content']
#         form = row['form']
#         source = row['source']

#         get_url = f'https://crm.alnafi.com/api/resource/Suppport?fields=["*"]&filters=[["Suppport","customer_email","=","{parent}"],["Suppport","source","=","{source}"]]'
       
#         if owner in support_emails:
#             get_response = requests.get(get_url, headers=headers)
#             lead_data = get_response.json()
#             data = {
#                 'comment_type':'Comment',
#                 'reference_doctype': 'Suppport',
#                 'comment_email': owner,
#                 'comment_by': owner,
#                 'content': note,
#             }

            
#             # try:
#             support_id = lead_data['data'][0]['name']
#             support_id_exists = True
#             data['reference_name'] = support_id
#             # except:
#             #     data['parent'] = parent
#             #     # failed_leads.append(data)
#             #     support_id_exists = False
         
#             # try:
            
#             if support_id_exists:   
#                 response = requests.post(post_url, headers=headers, json=data)

#                 if response.status_code != 200:
#                     print(f"Response Status Code: {response.status_code}")
#                     print(f"Response Text: {response.text}")
#                     data['parent'] = parent
#                     # failed_leads.append(data)
#                 else:
#                     print(f"Data sent for index {index}: {data} {parent}")
#                     # print("comment added")

#         # if failed_leads:
#         #     # print("failed leads exits")
#         #     with open('support_failed_easy_pay_comments.csv', 'a', newline='') as csvfile:
#         #         fieldnames = failed_leads[0].keys()
#         #         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#         #         # Check if the file is empty, and write header only if it's a new file
#         #         if csvfile.tell() == 0:
#         #             writer.writeheader()

#         #         for lead in failed_leads:
#         #             writer.writerow(lead)


# if __name__ == "__main__":
#     crmnote()

#===================================================================================

#SCRIPT TO match two csv file where parent matches take that form value and put it in error file



import pandas as pd

# # Load the first CSV file into a DataFrame
# file1 = pd.read_csv('/home/faizan/albaseer/Al-Baseer-Backend/Easy_pay_leads_comments.csv')

# # Load the second CSV file into a DataFrame
# file2 = pd.read_csv('/home/faizan/albaseer/Al-Baseer-Backend/support_failed_easy_pay_comments.csv')

# # Merge the DataFrames based on the 'email' column
# merged_df = pd.merge(file2, file1[['parent', 'source']], on='parent', how='left')

# # Save the merged DataFrame to a new CSV file
# merged_df.to_csv('merged_file.csv', index=False)

#=====================================================================================

# import pandas as pd
# from datetime import datetime

# def get_data_from_leads():
#     print("running")
#     user_api_key = '4e7074f890507cb'
#     user_secret_key = 'c954faf5ff73d31'

#     headers = {
#         'Authorization': f'token {user_api_key}:{user_secret_key}',
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#     }
# # # Read the CSV file into a DataFrame
# # file_path = '/home/faizan/albaseer/Al-Baseer-Backend/Easy_format_leads.csv' # Replace with the actual path to your CSV file
# # output_file_path = '/home/faizan/albaseer/Al-Baseer-Backend/Again_Easy_format_leads.csv'  # Replace with the actual path to your CSV file

#     # Construct the URL to get leads
#     get_url = f'https://crm.alnafi.com/api/resource/Lead?fields=["email_id","status","date","lead_creator","first_name", "mobile_no", "source", "product_names_list"]&limit_start=0&limit_page_length=10000000'

#     # Make the API request
#     response = requests.get(get_url, headers=headers)
#     # print(response.text)

#     if response.status_code == 200:
#         leads_data = response.json()
#         # print(leads_data)

#         if 'data' in leads_data:
#             leads = leads_data['data']

#             # Get today's date
#             today_date = datetime.date.today()

#             # Calculate 3 days before today
#             three_days_before = today_date - datetime.timedelta(days=3)

#             # Group leads by lead_creator
#             leads_by_creator = {}
#             for lead in leads:
#                 if lead.get('status') == 'Lead' and lead.get('date') is not None:
#                     lead_date = datetime.datetime.strptime(lead.get('date'), '%Y-%m-%d').date()
#                     if lead_date == three_days_before and lead.get('lead_creator') != 'haider.raza@alnafi.edu.pk':
#                         lead_creator = lead.get('lead_creator')
#                         if lead_creator not in leads_by_creator:
#                             leads_by_creator[lead_creator] = []
#                         leads_by_creator[lead_creator].append(lead)
            
#             print("leads_by_creator",leads_by_creator )
#             print(f"Total number of leads with status 'Lead' and date 3 days before today: {len(leads_by_creator)}")

#             # Delete leads that meet the criteria (no note and specific email)
#             for lead_creator, leads_list in leads_by_creator.items():
#                 for lead in leads_list:
#                     # if not lead['note']:
#                         email = lead['email_id']
#                         delete_url = f'https://crm.alnafi.com/api/resource/Lead/{email}'
#                         response = requests.delete(delete_url, headers=headers)
#                         print(response.text)
#             post_url = 'https://crm.alnafi.com/api/resource/Lead'
#             keys ={
#                "muzammil.raees@alnafi.edu.pk": ["b6d818ef8024f5a", "ce1749a7dcf8577"],
#                 "ribal.shahid@alnafi.edu.pk": ["39d14c9d602fa09", "216de0a015e7fd1"],
#                "waqas.shah@alnafi.edu.pk": ["b09d1796de6444a", "9ac70da03e4c23c"],
#                "shoaib.akhtar@alnafi.edu.pk": ["484f3e9978c00f3", "f61de5c03b3935d"],
#                "saad.askari@alnafi.edu.pk": ["e31afcb884def7e", "cb799e6913b57f9"],
#                "saima.ambreen@alnafi.edu.pk": ["3da0a250742fa00", "5ec8bb8e1e94930"],
#               "hamza.jamal@alnafi.edu.pk": ["dd3d10e83dfbb6b", "a1a50d549455fe3"],
#               "wamiq.siddiqui@alnafi.edu.pk": ["31c85c7e921b270", "845aff8197932c3"],
#               "suleman.masroor@alnafi.edu.pk": ["3f6d0f005e4fccc", "bbcaef6140205d2"],
#               "sunil.toto@alnafi.edu.pk": ["9d37a29d966277f", "018c3f6127c43cc"],
#             }
#             header_post = {
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#     }

#     fields_to_extract = ['email_id', 'status', 'date', 'mobile_no', 'first_name', 'source', 'product_names_list']

#     for lead_creator, leads_list in leads_by_creator.items():
#         for lead in leads_list:
#             # Initialize lead_data as a dictionary for each lead
#             lead_data = {field: '' for field in fields_to_extract}

#             for field in fields_to_extract:
#                 if field == 'date':
#                     lead_data[field] = str(datetime.date.today())
#                 else:
#                     lead_data[field] = lead.get(field) if lead.get(field) else ''

#             # Convert 'lead_data' to JSON format
#             lead_data_json = json.dumps(lead_data)

#             # Randomly select a key for each POST request
#             random_key = random.choice(list(keys.keys()))
#             header_post['Authorization'] = f'token {keys[random_key][0]}:{keys[random_key][1]}'

#             # Make the POST request
#             post_response = requests.post(post_url, headers=header_post, data=lead_data_json)
#             print(post_response.text)

# get_data_from_leads()





#==================================================================================


# # Read the CSV file into a DataFrame
# df = pd.read_csv('/home/faizan/albaseer/Al-Baseer-Backend/Easy_format_leads.csv')

# # Function to convert the date format
# def convert_date(date_str):
#     # Parse the input date string
#     # dt_object = datetime.strptime(date_str, '%d-%b-%y')
#     dt_object = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')

#     # Format the date as 'yyyy-mm-dd'
#     formatted_date = dt_object.strftime('%Y-%m-%d')

#     return formatted_date

# def convert_assign_date(date_str):
#     # Parse the input date string
#     dt_object = datetime.strptime(date_str, '%d-%b-%y')

#     # Format the date as 'yyyy-mm-dd'
#     formatted_date = dt_object.strftime('%Y-%m-%d')

#     return formatted_date

# # Apply the conversion function to the 'date' column
# df['formatted_date'] = df['created_at'].apply(convert_date)
# df['formatted_assigned_date'] = df['assigned_date'].apply(convert_assign_date)
# # Save the modified DataFrame to a new CSV file
# df.to_csv(output_file_path, index=False)


#==================================================================================

# from user.models import Main_User
# from user.constants import COUNTRY_CODES
# from payment.models import Main_Payment
# from secrets_api.algorithem import round_robin_exam

#Import eduqual level 5 and 6 bands

# def send_payment_exam_module():
#     data = pd.read_csv('/home/faizan/albaseer/Al-Baseer-Backend/Active Users - Faizan - final (copy).csv')

#     for index, row in data.iterrows():
#         email = row['email']
#         product_name = row['name']

#         filtered_payments = Main_Payment.objects.filter(user__email=email, product__product_name=product_name, source__in=['Easypaisa', 'UBL_IPG','UBL_DD','Stripe']).values("amount","product__product_name","currency","user__email","user__phone","user__first_name","user__last_name","user__country","internal_source","source")

#         order_datetime = row['payment_date']
#         amount = filtered_payments[0]['amount']
#         source = filtered_payments[0]['source']
#         currency = filtered_payments[0]['currency']
#         phone = filtered_payments[0]['user__phone']
#         country_code = filtered_payments[0]['user__country']

#         first_name = filtered_payments[0]['user__first_name']
#         last_name = filtered_payments[0]['user__last_name']

#         order_datetime_str = order_datetime
#         order_datetime_str_without_tz = order_datetime_str[:-6]  # Remove the last 6 characters (+0500)
#         order_datetime = datetime.fromisoformat(order_datetime_str_without_tz)
#         formatted_order_date = order_datetime.strftime('%Y-%m-%d')

#         expire_datetime_str = row['expiry_date']

#         if country_code:
#             for name, code in COUNTRY_CODES.items():
#                 if code == country_code:
#                     country_name = name
#                     break

#         customer_data = {
#             "first_name": first_name,
#             "last_name": last_name,
#             "contact_no": phone,
#             "customer_email": email,
#             "country": country_name,
#             "product_name": product_name,
#             "amount": amount,
#             "currency":currency,
#             "payment_source": source,
#             "payment": formatted_order_date,
#             "expiration_date": expire_datetime_str,
#             "expiration_status": 'Active',
#         }

#         api_key, api_secret = round_robin_exam()

#         headers = {
#             'Authorization': f'token {api_key}:{api_secret}',
#             "Content-Type": "application/json",
#             "Accept": "application/json",
#         }

#         customer_url = 'https://crm.alnafi.com/api/resource/Exam 5 6 Leads'
#         response = requests.post(customer_url, headers=headers, json=customer_data)
#         if response.status_code != 200:
#             print(response.text)
#         else:
#             print("data sent to exam doctype")
                    
# send_payment_exam_module()
            


#=======================================================================================
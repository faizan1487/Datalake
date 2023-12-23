# import os
# import django
# from faker import Faker
# import random
# from datetime import datetime, timedelta

# # Set up Django environment
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "albaseer.settings")  # Replace with your project's settings module
# django.setup()

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




#+++++=============================================================================
# from datetime import datetime
# import requests
# from datetime import datetime
import requests
# import pandas as pd

# def crmnote():
#     user_api_key = '2a1d467717681df'
#     user_secret_key = '39faa082ac5f258'

#     headers = {
#         'Authorization': f'token {user_api_key}:{user_secret_key}',
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#     }

#     data = pd.read_csv('/home/faizan/albaseer/Al-Baseer-Backend/tabCRM Note_export_2023-11-02_102731.csv')

#     for index, row in data.iterrows():
#         name = row['name']
#         creation = row['creation']
#         modified = row['modified']
#         modified_by = row['modified_by']
#         owner = row['owner']
#         docstatus = row['docstatus']
#         idx = row['idx']
#         note = row['note']
#         added_by = row['added_by']
#         parent = row['parent']
#         parentfield = row['parentfield']
#         parenttype = row['parenttype']

#         added_on = row['added_on']
#         if pd.isna(added_on):  # Check for "nan"
#             added_on = None

#         # Convert creation and modified datetime strings to ISO format
#         creation = datetime.fromisoformat(creation).isoformat()
#         modified = datetime.fromisoformat(modified).isoformat()

#         # try:
#         data = {
#             'name': name,
#             'parent': parent,
#             'creation': creation,
#             'modified': modified,
#             'modified_by': modified_by,
#             'owner': owner,
#             'docstatus': docstatus,
#             'idx': idx,
#             'note': note,
#             'added_by': added_by,
#             'added_on': added_on,
#             'parentfield': parentfield,
#             'parenttype': parenttype,
#         }
#         print(data)

#         post_url = 'https://crm.alnafi.com/api/resource/CRM Note'
#         response = requests.post(post_url, headers=headers, json=data)

#         print(f"Data sent for index {index}: {data}")
#         print(f"Response Status Code: {response.status_code}")
#         print(f"Response Text: {response.text}")

#         # except Exception as e:
#         #     print(f"Error processing data for index {index}: {str(e)}")

# if __name__ == "__main__":
#     crmnote()



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


import csv
import datetime
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

# =========================================================================================================

#extract leads from crm with status lead and with no comments
#then delete them from crm or send put request and assign those leads to admin
#or send delete request with id to delete those leads

from datetime import datetime
import requests
import pandas as pd
import csv
import json


def fetch_idol_leads():
    print("fetch_idol_leads")
    # Admin keys
    user_api_key = '4e7074f890507cb'
    user_secret_key = 'c954faf5ff73d31'
    
    # url = 'https://crm.alnafi.com/api/resource/Lead?fields=["first_name","status","lead_creator","phone","country","email_id","form","advert_detail","product_names_list","source","notes","`tabCRM Note`.note","`tabCRM Note`.added_on","`tabCRM Note`.added_by"]&filters=[["Lead","status","=","Lead"]]&limit_start=0&limit_page_length=10000000'


    url = 'https://crm.alnafi.com/api/resource/Lead?fields=["first_name","status","lead_creator","phone","date","country","email_id","form","product_names_list","demo_product","enrollment","interest","qualification","cv_link","source","notes","`tabCRM Note`.note","`tabCRM Note`.added_on","`tabCRM Note`.added_by"]&filters=[["Lead","status","=","Lead"]]&limit_start=0&limit_page_length=10000000'


    
    headers = {
        'Authorization': f'token {user_api_key}:{user_secret_key}',
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers)
    lead_data = json.loads(response.text)

    if 'data' in lead_data:
        lead_data = lead_data['data']

        if lead_data:
            # Create an empty dictionary to store data
            data_dict = {}

            # Loop through the response data
            for item in lead_data:
                for key, value in item.items():
                    if key in data_dict:
                        data_dict[key].append(value)
                    else:
                        data_dict[key] = [value]

            # Create a DataFrame from the dictionary
            df = pd.DataFrame(data_dict)

            # Define the CSV file name
            csv_filename = 'all_lead_data.csv'

            # Save the data to a CSV file with column names
            df.to_csv(csv_filename, index=False)

            print(f"Data saved to {csv_filename}")
        else:
            print("No data found in the response.")
    else:
        print(response.text)
        print("The 'data' key is missing in the response.")



    #Loop over the leads data and delete those leads which don't have a comment
        
    # data = response.json()
    # for i in data['data']:
    #     if not i['note']:
    #         email = i['email_id']  
    #         delete_url = f'https://crm.alnafi.com/api/resource/Lead/{email}'
    #         response = requests.delete(delete_url, headers=headers)
    #         print(response.text)















fetch_idol_leads()
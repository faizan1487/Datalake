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


# import csv
# import datetime
# import requests

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



    #Loop over the leads data and delete those leads which don't have a comment
        
    # data = response.json()
    # for i in data['data']:
    #     if not i['note']:
    #         email = i['email_id']  
    #         delete_url = f'https://crm.alnafi.com/api/resource/Lead/{email}'
    #         response = requests.delete(delete_url, headers=headers)
    #         print(response.text)



import datetime
import requests
import json
import random



def get_data_from_leads():
    print("running")
    user_api_key = '4e7074f890507cb'
    user_secret_key = 'c954faf5ff73d31'

    headers = {
        'Authorization': f'token {user_api_key}:{user_secret_key}',
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    # Construct the URL to get leads
    get_url = f'https://crm.alnafi.com/api/resource/Lead?fields=["email_id","status","date","lead_creator","first_name", "mobile_no", "source", "product_names_list"]&limit_start=0&limit_page_length=10000000'

    # Make the API request
    response = requests.get(get_url, headers=headers)
    # print(response.text)

    if response.status_code == 200:
        leads_data = response.json()
        # print(leads_data)

        if 'data' in leads_data:
            leads = leads_data['data']

            # Get today's date
            today_date = datetime.date.today()

            # Calculate 3 days before today
            three_days_before = today_date - datetime.timedelta(days=3)

            # Group leads by lead_creator
            leads_by_creator = {}
            for lead in leads:
                if lead.get('status') == 'Lead' and lead.get('date') is not None:
                    lead_date = datetime.datetime.strptime(lead.get('date'), '%Y-%m-%d').date()
                    if lead_date == three_days_before and lead.get('lead_creator') != 'haider.raza@alnafi.edu.pk':
                        lead_creator = lead.get('lead_creator')
                        if lead_creator not in leads_by_creator:
                            leads_by_creator[lead_creator] = []
                        leads_by_creator[lead_creator].append(lead)
            
            print("leads_by_creator",leads_by_creator )
            print(f"Total number of leads with status 'Lead' and date 3 days before today: {len(leads_by_creator)}")

            # Delete leads that meet the criteria (no note and specific email)
            for lead_creator, leads_list in leads_by_creator.items():
                for lead in leads_list:
                    # if not lead['note']:
                        email = lead['email_id']
                        delete_url = f'https://crm.alnafi.com/api/resource/Lead/{email}'
                        response = requests.delete(delete_url, headers=headers)
                        print(response.text)
            post_url = 'https://crm.alnafi.com/api/resource/Lead'
            keys ={
               "muzammil.raees@alnafi.edu.pk": ["b6d818ef8024f5a", "ce1749a7dcf8577"],
                "ribal.shahid@alnafi.edu.pk": ["39d14c9d602fa09", "216de0a015e7fd1"],
               "waqas.shah@alnafi.edu.pk": ["b09d1796de6444a", "9ac70da03e4c23c"],
               "shoaib.akhtar@alnafi.edu.pk": ["484f3e9978c00f3", "f61de5c03b3935d"],
               "saad.askari@alnafi.edu.pk": ["e31afcb884def7e", "cb799e6913b57f9"],
               "saima.ambreen@alnafi.edu.pk": ["3da0a250742fa00", "5ec8bb8e1e94930"],
              "hamza.jamal@alnafi.edu.pk": ["dd3d10e83dfbb6b", "a1a50d549455fe3"],
              "wamiq.siddiqui@alnafi.edu.pk": ["31c85c7e921b270", "845aff8197932c3"],
              "suleman.masroor@alnafi.edu.pk": ["3f6d0f005e4fccc", "bbcaef6140205d2"],
              "sunil.toto@alnafi.edu.pk": ["9d37a29d966277f", "018c3f6127c43cc"],
            }
            header_post = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    fields_to_extract = ['email_id', 'status', 'date', 'mobile_no', 'first_name', 'source', 'product_names_list']

    for lead_creator, leads_list in leads_by_creator.items():
        for lead in leads_list:
            # Initialize lead_data as a dictionary for each lead
            lead_data = {field: '' for field in fields_to_extract}

            for field in fields_to_extract:
                if field == 'date':
                    lead_data[field] = str(datetime.date.today())
                else:
                    lead_data[field] = lead.get(field) if lead.get(field) else ''

            # Convert 'lead_data' to JSON format
            lead_data_json = json.dumps(lead_data)

            # Randomly select a key for each POST request
            random_key = random.choice(list(keys.keys()))
            header_post['Authorization'] = f'token {keys[random_key][0]}:{keys[random_key][1]}'

            # Make the POST request
            post_response = requests.post(post_url, headers=header_post, data=lead_data_json)
            print(post_response.text)

get_data_from_leads()


import csv
import datetime
import requests
import random
import json
import pandas as pd


#### For Creating Files Of 3 days Before Lead ####
# def get_and_save_all_lead_data():
#     user_api_key = '4e7074f890507cb'
#     user_secret_key = 'c954faf5ff73d31'
    

#     headers = {
#         'Authorization': f'token {user_api_key}:{user_secret_key}',
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#     }

#     # Construct the URL to get leads
#     get_url = f'https://crm.alnafi.com/api/resource/Lead?fields=["email_id","status","phone","date","lead_creator"]&limit_start=0&limit_page_length=10000000'

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
#                     fieldnames = ['Email', 'Status', 'Assigned Date', 'Lead Owner', 'Phone']
#                     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#                     writer.writeheader()
#                     for lead in creator_leads:
#                         lead_id = lead.get('email_id')
#                         lead_status = lead.get('status')
#                         lead_date = lead.get('date')
#                         lead_creator = lead.get('lead_creator')
#                         lead_phone = lead.get('phone')
#                         writer.writerow({'Email': lead_id, 'Status': lead_status, 'Assigned Date': lead_date, 'Lead Owner': lead_creator, 'Phone': lead_phone })

#                 print(f"Filtered leads data for {creator} saved to '{filename}'")
#         else:
#             print("No leads found in the response.")
#     else:
#         print("Failed to fetch data. Status code:", response.status_code)

# get_and_save_all_lead_data()



#=============================================================================================

### For Reassigning 3 Days before lead ####

# def get_data_from_leads():
#     print("running")
#     user_api_key = '4e7074f890507cb'
#     user_secret_key = 'c954faf5ff73d31'

#     headers = {
#         'Authorization': f'token {user_api_key}:{user_secret_key}',
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#     }
#     get_url = f'https://crm.alnafi.com/api/resource/Lead?fields=["email_id","status","date","lead_creator","first_name", "mobile_no", "source", "product_names_list", "form", "advert_detail"]&limit_start=0&limit_page_length=10000000'

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
#                     if lead_date == three_days_before and lead.get('lead_creator') not in ['haider.raza@alnafi.edu.pk','Administrator']:
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
#                 "ribal.shahid@alnafi.edu.pk": ["39d14c9d602fa09", "216de0a015e7fd1"],
#                "waqas.shah@alnafi.edu.pk": ["b09d1796de6444a", "9ac70da03e4c23c"],
#                "shoaib.akhtar@alnafi.edu.pk": ["484f3e9978c00f3", "f61de5c03b3935d"],
#                "saad.askari@alnafi.edu.pk": ["e31afcb884def7e", "cb799e6913b57f9"],
#                "saima.ambreen@alnafi.edu.pk": ["3da0a250742fa00", "5ec8bb8e1e94930"],
#               "hamza.jamal@alnafi.edu.pk": ["dd3d10e83dfbb6b", "a1a50d549455fe3"],
#               "wamiq.siddiqui@alnafi.edu.pk": ["31c85c7e921b270", "845aff8197932c3"],
#               "suleman.masroor@alnafi.edu.pk": ["3f6d0f005e4fccc", "bbcaef6140205d2"],
#               "sunil.toto@alnafi.edu.pk": ["9d37a29d966277f", "018c3f6127c43cc"],
#               "maarij.najam@alnafi.edu.pk": ["b3bb7a167ec651a", "449cd28cd263361"],
#             }
#             header_post = {
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#     }

#     fields_to_extract = ['email_id', 'status', 'date', 'mobile_no', 'first_name', 'source', 'product_names_list', 'form', 'advert_detail']

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


### For Single Lead Upload To Someone ######
from datetime import datetime
def upload_sales_lead():
    url = 'https://crm.alnafi.com/api/resource/Lead'
    user_api_key = 'b3bb7a167ec651a'
    user_secret_key = '449cd28cd263361'

    headers = {
        'Authorization': f'token {user_api_key}:{user_secret_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    data = pd.read_csv('/home/uzair/Documents/Al-Baseer-Backend/Special.csv')
    for index, row in data.iterrows():
        first_name = str(row['First Name'])
        email = str(row['Email'])
        phone = str(row['Phone'])
        source = str(row['Source'])
        status = 'Lead'
        form = str(row['Form'])
        advert = str(row['Advert'])
        date = datetime.now().date().isoformat()
        print(source)
        lead = {
            'first_name': first_name,
            'email_id': email,
            'source': source,
            'status': status,
            'phone': phone,
            'advert': advert,
            'form': form,
            'date' : date,
        }
        print("lead", lead)
        response = requests.post(url, headers=headers, json=lead)
        print(response.status_code)
        print(response.text)
upload_sales_lead()

### For Creating Files Of Particular Sales Member ####
import csv
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
#     get_url = f'https://crm.alnafi.com/api/resource/Lead?fields=["email_id","status","date","lead_creator","first_name", "mobile_no", "source", "product_names_list", "form", "advert_detail"]&limit_start=0&limit_page_length=10000000'

#     # Make the API request
#     response = requests.get(get_url, headers=headers)
#     # print(response.text)

#     if response.status_code == 200:
#         leads_data = response.json()

#         if 'data' in leads_data:
#             leads = leads_data['data']

#             # Filter leads for 'Converted' status and lead_creator 'muzammil.raees@alnafi.edu.pk'
#             filtered_leads = [
#                 lead for lead in leads
#                 if lead.get('status') != 'Converted'
#                 and lead.get('lead_creator') == 'muzammil.raees@alnafi.edu.pk'
#             ]
#             print("Data", len(filtered_leads))
#             # Specify the CSV file path
#             csv_file_path = 'muzammil_leads.csv'

#             # Write the leads to the CSV file
#             with open(csv_file_path, mode='w', newline='') as csv_file:
#                 fieldnames = leads[0].keys() if leads else []
#                 writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

#                 # Write header
#                 writer.writeheader()

#                 # Write data
#                 writer.writerows(filtered_leads)

#             print(f"Leads data for muzammil.raees@alnafi.edu.pk saved to {csv_file_path}")

#             # Extract email addresses of leads saved to the CSV file
#             emails_to_delete = [lead['email_id'] for lead in filtered_leads]

#             # Delete only the leads saved to the CSV file
#             for email in emails_to_delete:
#                 delete_url = f'https://crm.alnafi.com/api/resource/Lead/{email}'
#                 delete_response = requests.delete(delete_url, headers=headers)
#                 print(f"Lead with email {email} deleted. Response: {delete_response.text}")

#     else:
#         print(f"Failed to retrieve leads. Status code: {response.status_code}")

# get_and_save_all_lead_data()


# from datetime import datetime
# def upload_sales_lead():
#     url = 'https://crm.alnafi.com/api/resource/Lead'
#     keys ={
#             "ribal.shahid@alnafi.edu.pk": ["39d14c9d602fa09", "216de0a015e7fd1"],
#             "waqas.shah@alnafi.edu.pk": ["b09d1796de6444a", "9ac70da03e4c23c"],
#             "shoaib.akhtar@alnafi.edu.pk": ["484f3e9978c00f3", "f61de5c03b3935d"],
#             "saad.askari@alnafi.edu.pk": ["e31afcb884def7e", "cb799e6913b57f9"],
#             "saima.ambreen@alnafi.edu.pk": ["3da0a250742fa00", "5ec8bb8e1e94930"],
#             "hamza.jamal@alnafi.edu.pk": ["dd3d10e83dfbb6b", "a1a50d549455fe3"],
#             "wamiq.siddiqui@alnafi.edu.pk": ["31c85c7e921b270", "845aff8197932c3"],
#             "suleman.masroor@alnafi.edu.pk": ["3f6d0f005e4fccc", "bbcaef6140205d2"],
#             "sunil.toto@alnafi.edu.pk": ["9d37a29d966277f", "018c3f6127c43cc"],
#             "maarij.najam@alnafi.edu.pk": ["b3bb7a167ec651a", "449cd28cd263361"],
#         }
#     header_post = {
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#     }
#     data = pd.read_csv('/home/uzair/Documents/Al-Baseer-Backend/muzammil_leads.csv')
#     for index, row in data.iterrows():
#         first_name = str(row['First Name'])
#         email = str(row['email'])
#         phone = str(row['phone'])
#         source = str(row['source'])
#         status = str(row['status'])
#         advert_detail = str(row['advert_detail'])
#         form = str(row['Form'])
#         date = datetime.now().date().isoformat()
        
#         lead = {
#             'first_name': first_name,
#             'advert_detail': advert_detail if advert_detail else None,
#             'email_id': email,
#             'source': source,
#             'status': status,
#             'phone': phone,
#             'form': form,
#             'date': date,
#         }
#         print("lead", lead)
#         random_key = random.choice(list(keys.keys()))
#         header_post['Authorization'] = f'token {keys[random_key][0]}:{keys[random_key][1]}'

#         # Make the POST request
#         post_response = requests.post(url, headers=header_post, data=json.dumps(lead))

#         # Check the status code
#         if post_response.status_code == 200:
#             print("Lead created successfully.")
#         else:
#             print(f"Failed to create lead. Status code: {post_response.status_code}")
#             print("Response text:", post_response.text)

# upload_sales_lead()


#### Script For Saving Lead in Csv ##
# def get_and_save_all_lead_data():
#     user_api_key = '4e7074f890507cb'
#     user_secret_key = 'c954faf5ff73d31'
    
#     headers = {
#         'Authorization': f'token {user_api_key}:{user_secret_key}',
#         "Content-Type": "application/json",
#         "Accept": "application/json",
#     }

#     # Construct the URL to get leads
#     get_url = f'https://crm.alnafi.com/api/resource/Lead?fields=["email_id","status","date","lead_creator","first_name", "mobile_no", "source", "product_names_list", "form", "advert_detail"]&limit_start=0&limit_page_length=10000000'

#     # Make the API request
#     response = requests.get(get_url, headers=headers)
#     # print(response.text)

#     if response.status_code == 200:
#         leads_data = response.json()

#         if 'data' in leads_data:
#             leads = leads_data['data']

#             filtered_leads = [
#                 lead for lead in leads
#                 if lead.get('status') == 'Lead'
#             ]
#             print("Data", len(filtered_leads))
#             # print("Data", filtered_leads)
#             # csv_file_path = 'Lead_with_status_lead.csv'

#             # with open(csv_file_path, mode='w', newline='') as csv_file:
#             #     fieldnames = filtered_leads[0].keys() if filtered_leads else []
#             #     writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

#             #     writer.writeheader()

#             #     writer.writerows(filtered_leads)

#             # print(f"Filtered leads data saved to {csv_file_path}")
#             for lead in filtered_leads:
#                 email = lead.get('email_id')
#                 delete_url = f'https://crm.alnafi.com/api/resource/Lead/{email}'
#                 response = requests.delete(delete_url, headers=headers)
#                 print(f"Lead with email {email} deleted. Response: {response.text}")

# get_and_save_all_lead_data()

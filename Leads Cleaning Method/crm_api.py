import requests
from urllib.parse import urlencode
import os
import pandas as pd
from datetime import datetime


# For CRM API All Leads Emails:
def crm_all_leads_emails():
    base_url = 'https://crm.alnafi.com/api/resource/Lead'
    params = {
        'fields': '["email_id"]',
        'limit_start': 0,
        'limit_page_length': 10000000  # Adjust the limit as needed
    }
    encoded_params = urlencode(params)
    get_url = f'{base_url}?{encoded_params}'

    
    headers = {
        'Authorization': f'token {user_api_key}:{user_secret_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    try:
        response = requests.get(get_url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        response_data = response.json()
        list_of_emails = [data['email_id'] for data in response_data.get('data', [])]
        return list_of_emails
    except requests.exceptions.RequestException as e:
        return f'Request failed: {str(e)}'

# For Cleaning Leads:
def clean_leads(dataframe, output_file_name):
    # Get today's date
    today = datetime.today().strftime('%d-%m-%Y')
    
    # Define output file path
    main_folder = os.path.join(os.getcwd(), today, 'Clean_Leads')
    output_file_path = os.path.join(main_folder, f"{output_file_name}.csv")

    # Check if the output file already exists, delete it if so
    if os.path.exists(output_file_path):
        os.remove(output_file_path)
        print(f"Previous {output_file_name} file found and removed.")

    list_of_leads_emails = dataframe['email'].tolist()

    # Get the list of emails from the CRM:
    list_of_CRM_leads_emails = crm_all_leads_emails()

    # Create a new DataFrame to store the results:
    unique_records = pd.DataFrame(columns=dataframe.columns)

    for email in list_of_leads_emails:
        if email not in list_of_CRM_leads_emails:
            rows_matching_email = dataframe.loc[dataframe['email'] == email]
            unique_records = pd.concat([unique_records, rows_matching_email])

    # Write the results DataFrame to a new file
    unique_records.to_csv(output_file_path, index=False)
    print(f"Unique records saved in '{output_file_path}'.")

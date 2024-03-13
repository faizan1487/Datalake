import pandas as pd

def process_excel_data(file_path, city, form, country, source, advert, assigned_date):
    # Read the excel file
    sheet_data = pd.read_excel(file_path)[["full_name", "phone_number", "email", "created_time"]]

    # Drop duplicates based on email column
    sheet_data = sheet_data.drop_duplicates(subset=['email'], keep='first')

    # Rename headers
    sheet_data.rename(columns={'full_name': 'full_name',
                               'phone_number': 'phone',
                               'email': 'email',
                               'created_time': 'created_at'
                               }, inplace=True)

    # Remove 'p:' from the phone numbers
    sheet_data['phone'] = sheet_data['phone'].str.replace('p:', '')

    # Add a new column and set its values for all rows
    sheet_data['city'] = city
    sheet_data['form'] = form
    sheet_data['country'] = country
    sheet_data['source'] = source
    sheet_data['advert'] = advert
    sheet_data['assigned_date'] = assigned_date

    # Reorder columns
    sheet_data = sheet_data[['full_name', 'email', 'phone', 'city', 'form', 'country', 'source', 'advert', 'created_at', 'assigned_date']]

    return sheet_data



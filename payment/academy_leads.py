import requests
from datetime import date



def academy_leads():
    # Your API endpoint to fetch data
    url = "https://api.alnafi.com/pay/expiry_data/"
    # url = "http://127.0.0.1:8000/pay/expiry_data/"

    # Fetch data from the API
    response = requests.get(url)
    if response.status_code != 200:
        return None

    data = response.json()

    url = 'https://crm.alnafi.com/api/resource/Renewal Leads'
    
    headers = {
        'Authorization': f'token {user_api_key}:{user_secret_key}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    for entry in data:
        serial_data = {
            "phone": entry.get('user_phone', ''),
            "user_id": entry.get('user_email', ''),
            "date_joined": entry.get('user_date_joined', ''),
            "first_name": entry.get('user_username', ''),
            "product_id": entry.get('product_id', ''),
            "payment_date": entry.get('payment_date', ''),
            "expiration_date": entry.get('expiry_date', ''),
            "product_name": entry.get('product_name', ''),
            "status": 'Active',
            "country": 'Unknown',
            "assigned_date": str(date.today()),
        }

        response = requests.post(url, headers=headers, json=serial_data)
        # print(response.text)
        if response.status_code == 200:
            print('Data successfully sent!')
        else:
            print(f'Failed to send data. Status code: {response.status_code}')




if __name__ == "__main__":
    academy_leads()
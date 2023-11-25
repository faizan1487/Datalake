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




# import pandas as pd

# # Load your CSV file into a DataFrame
# df = pd.read_csv("/home/faizan/albaseer/Al-Baseer-Backend/Leads - Al Baseer to CRM - O Levels.csv")

# # Parse the date_joined column into datetime objects
# df['date_joined'] = pd.to_datetime(df['date_joined'], format='%Y-%m-%dT%H:%M:%S%z')

# # Convert the datetime objects to the "yyyy-mm-dd" format
# df['date_joined'] = df['date_joined'].dt.strftime('%Y-%m-%d')

# # Save the DataFrame back to a CSV file
# df.to_csv("/home/faizan/albaseer/Al-Baseer-Backend/new_file.csv", index=False)

from datetime import datetime
import requests
import pandas as pd

def crmnote():
    user_api_key = '2a1d467717681df'
    user_secret_key = '39faa082ac5f258'

    headers = {
        'Authorization': f'token {user_api_key}:{user_secret_key}',
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    data = pd.read_csv('/home/faizan/albaseer/Al-Baseer-Backend/tabCRM Note_export_2023-11-02_102731.csv')

    for index, row in data.iterrows():
        name = row['name']
        creation = row['creation']
        modified = row['modified']
        modified_by = row['modified_by']
        owner = row['owner']
        docstatus = row['docstatus']
        idx = row['idx']
        note = row['note']
        added_by = row['added_by']
        parent = row['parent']
        parentfield = row['parentfield']
        parenttype = row['parenttype']

        added_on = row['added_on']
        if pd.isna(added_on):  # Check for "nan"
            added_on = None

        # Convert creation and modified datetime strings to ISO format
        creation = datetime.fromisoformat(creation).isoformat()
        modified = datetime.fromisoformat(modified).isoformat()

        # try:
        data = {
            'name': name,
            'parent': parent,
            'creation': creation,
            'modified': modified,
            'modified_by': modified_by,
            'owner': owner,
            'docstatus': docstatus,
            'idx': idx,
            'note': note,
            'added_by': added_by,
            'added_on': added_on,
            'parentfield': parentfield,
            'parenttype': parenttype,
        }
        print(data)

        post_url = 'https://crm.alnafi.com/api/resource/CRM Note'
        response = requests.post(post_url, headers=headers, json=data)

        print(f"Data sent for index {index}: {data}")
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")

        # except Exception as e:
        #     print(f"Error processing data for index {index}: {str(e)}")

if __name__ == "__main__":
    crmnote()
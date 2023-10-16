import os
import django
from faker import Faker
import random
from datetime import datetime, timedelta

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "albaseer.settings")  # Replace with your project's settings module
django.setup()

# Import your model
from payment.models import Main_Payment  # Replace 'your_app' with the name of your Django app
from user.models import Main_User
from products.models import Main_Product
# Create a Faker instance
fake = Faker()

# Define a function to add fake data to the Main_Payment model
def add_fake_payment_data(num_records,products,users):
    for _ in range(num_records):
        user_instance = random.choice(users)  # Select a random user from the list
        payment = Main_Payment(
            source_payment_id=fake.uuid4(),
            alnafi_payment_id=fake.uuid4(),
            easypaisa_ops_id=fake.uuid4(),
            easypaisa_customer_msidn=fake.phone_number(),
            card_mask=fake.credit_card_number(card_type="mastercard"),
            user=user_instance,  # You may need to create user instances and assign them here
            amount=fake.random_int(min=1, max=1000),
            currency=fake.currency_code(),
            source=fake.word(),
            internal_source=fake.word(),
            status=random.choice(["Pending", "Successful", "Failed"]),
            order_datetime=fake.date_time_between(start_date="-1y", end_date="now"),
            expiration_datetime=fake.date_time_between(start_date="now", end_date="+1y"),
            activation_datetime=fake.date_time_between(start_date="now", end_date="+1y"),
            token_paid_datetime=fake.date_time_between(start_date="now", end_date="+1y"),
            easypaisa_fee_pkr=fake.random_int(min=1, max=100),
            easypaisa_fed_pkr=fake.random_int(min=1, max=100),
            ubl_captured=fake.word(),
            ubl_reversed=fake.word(),
            ubl_refund=fake.word(),
            ubl_approval_code=fake.word(),
            description=fake.sentence(),
            qarz=fake.boolean(),
            remarks=fake.text(),
            payment_proof=fake.uri(),
            send_invoice=fake.boolean(),
            pk_invoice_number=fake.random_int(min=1000, max=9999),
            us_invoice_number=fake.random_int(min=1000, max=9999),
            sponsored=fake.boolean(),
            coupon_code=fake.word(),
            is_upgrade_payment=fake.boolean(),
            affiliate=fake.word(),
            candidate_name=fake.name(),
            ubl_depositor_name=fake.name(),
            candidate_phone=fake.phone_number(),
            bin_bank_name=fake.word(),
            error_reason=fake.sentence(),
        )

        payment.save()
        # Assign one or more Main_Product instances to the product field
        product_list = list(products)
        random_products = random.sample(product_list, k=random.randint(1, len(product_list)))
        payment.product.set(random_products)
        payment.save()

if __name__ == "__main__":
    num_records_to_create = 100  # Adjust the number of records you want to create
    products = Main_Product.objects.all()
    users = Main_User.objects.all()
    add_fake_payment_data(num_records_to_create,products,users)
    print(f"Added {num_records_to_create} fake Main_Payment records.")
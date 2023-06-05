import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "albaseer.settings")

import django

django.setup()

# import random
# from thinkific.models import Thinkific_User, Thinkific_Users_Enrollments
# from faker import Faker
# import datetime
# fake = Faker()
# from decimal import Decimal

from django.contrib.auth import get_user_model
from faker import Faker
from datetime import datetime
from user.models import Main_User
import random

faker = Faker()
User = get_user_model()
num_fake_data = 90  # Number of fake data to create

for _ in range(num_fake_data):
    first_name = faker.name()
    email = faker.email()
    source = 'Newsletter'
    phone = faker.phone_number()
    created_at = faker.date_time_between(start_date='-1y', end_date='now')

    user = Main_User.objects.create(
        first_name=first_name,
        email=email,
        source=source,
        phone=phone,
        created_at=created_at,
    )


# def populate(value):
#     for i in range(value):
#         id=fake.random_int()
#         email=fake.email()
#         username = fake.user_name()
#         user_id = fake.random_int()
#         course_name = fake.words()
#         course_id=fake.random_int()
#         percentage_completed = fake.pydecimal(left_digits=1, right_digits=2, positive=True)
#         expired = fake.pybool()
#         is_free_trial = fake.pybool()
#         completed = fake.pybool()
#         started_at=fake.date_time_this_decade()
#         activated_at = fake.date_time_this_decade()
#         completed_at = fake.date_time_this_decade()
#         updated_at = fake.date_time_this_decade()
#         expiry_date = fake.date_time_this_decade()
#         obj = Thinkific_Users_Enrollments.objects.get_or_create(id=id,username=username,     
#                                                    email=email,user_id=user_id,course_name=course_name,course_id=course_id,percentage_completed=percentage_completed,expired=expired,is_free_trial=is_free_trial,completed=completed,started_at=started_at,activated_at=activated_at,completed_at=completed_at,updated_at=updated_at,expiry_date=expiry_date)
        
# def main():
#     no = int(input("no of records: "))
#     populate(no)
    
    
# if __name__ == "__main__":
#     main()
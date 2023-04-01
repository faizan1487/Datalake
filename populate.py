import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "albaseer.settings")

import django

django.setup()

import random
from thinkific.models import Thinkific_User, Thinkific_Users_Enrollments
from faker import Faker
import datetime
fake = Faker()
from decimal import Decimal

def populate(value):
    for i in range(value):
        id=fake.random_int()
        email=fake.email()
        username = fake.user_name()
        user_id = fake.random_int()
        course_name = fake.words()
        course_id=fake.random_int()
        percentage_completed = fake.pydecimal(left_digits=1, right_digits=2, positive=True)
        expired = fake.pybool()
        is_free_trial = fake.pybool()
        completed = fake.pybool()
        started_at=fake.date_time_this_decade()
        activated_at = fake.date_time_this_decade()
        completed_at = fake.date_time_this_decade()
        updated_at = fake.date_time_this_decade()
        expiry_date = fake.date_time_this_decade()
        obj = Thinkific_Users_Enrollments.objects.get_or_create(id=id,username=username,     
                                                   email=email,user_id=user_id,course_name=course_name,course_id=course_id,percentage_completed=percentage_completed,expired=expired,is_free_trial=is_free_trial,completed=completed,started_at=started_at,activated_at=activated_at,completed_at=completed_at,updated_at=updated_at,expiry_date=expiry_date)
        
def main():
    no = int(input("no of records: "))
    populate(no)
    
    
if __name__ == "__main__":
    main()
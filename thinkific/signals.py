from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from .models import Thinkific_User, Thinkific_Users_Enrollments
from requests.exceptions import RequestException
from user.constants import COUNTRY_CODES
import environ
from secrets_api.algorithem import round_robin

env = environ.Env()
env.read_env()
api_key = env("FRAPPE_API_KEY")
api_secret = env("FRAPPE_API_SECRET")

DEBUG = env('DEBUG',cast=bool)

@receiver(post_save, sender=Thinkific_Users_Enrollments)
def send_lead_post_request(sender, instance, **kwargs):
    # return
    print("signal running")
    source='Thinkific'
    thinkific_user = usersignal(instance,source)
        

def usersignal(instance,source):
    # post_save.disconnect(send_lead_post_request, sender=Thinkific_Users_Enrollments)
    # if instance.is_processing:
    #     return

    
    try:
        if instance.course_name.lower().startswith("demo"):
            user = instance.user_id
            user_enrollments = user.user_enrollments.all()

            products = ""
            for enrollment in user_enrollments:
                # print(enrollment.course_name)
                if enrollment.course_name.lower().startswith("demo"):
                    products += enrollment.course_name + ", "


            products = products.rstrip(", ")


            # if DEBUG:
            #     api_key = '2768f34bb4bb7f7'
            #     api_secret = '21754cee8dc0f42'
            #     url = f'http://3.142.247.16/api/resource/Lead?fields=["name","email_id"]&filters=[["Lead","email_id","=","{user.email}"]]'
            # else:
            
            url = f'https://crm.alnafi.com/api/resource/Lead?fields=["name","email_id"]&filters=[["Lead","email_id","=","{user.email}"]]'
            
            user_api_key, user_secret_key = round_robin()


            headers = {
                'Authorization': f'token {user_api_key}:{user_secret_key}',
                "Content-Type": "application/json",
                "Accept": "application/json",
            }    


            country_code = getattr(user, 'country', "Unknown")
            country_name = None

            if country_code:
                for name, code in COUNTRY_CODES.items():
                    if code == country_code:
                        country_name = name
                        break
            
            # if DEBUG:
            #     data = {
            #             "first_name": user.first_name or None,
            #             "last_name": user.last_name if hasattr(user, 'last_name') else None,
            #             "email_id": user.email or None,
            #             "mobile_no": user.phone if hasattr(user, 'phone') else None,
            #             "country": country_name,
            #             "source": source,
            #             "product": products if hasattr(instance, 'course_name') else None,
            #             # Add other fields from the Main_User model to the data dictionary as needed
            #         }
            # else:
            data = {
                "first_name": user.first_name or None,
                "last_name": user.last_name if hasattr(user, 'last_name') else None,
                "email_id": user.email or None,
                "mobile_no": user.phone if hasattr(user, 'phone') else None,
                "country": country_name,
                "source": source,
                "product_name": products if hasattr(instance, 'course_name') else None,
                # Add other fields from the Main_User model to the data dictionary as needed
            }
            
            
            response = requests.get(url, headers=headers)
            lead_data = response.json()
            
            already_existed = len(lead_data["data"]) > 0


            if already_existed:
                lead_id = lead_data['data'][0]['name']

                # if DEBUG:
                #     url = f'http://3.142.247.16/api/resource/Lead/{lead_id}'
                # else:
                url = f'https://crm.alnafi.com/api/resource/Lead/{lead_id}'

                response = requests.put(url, headers=headers, json=data)
                user.erp_lead_id = lead_data['data'][0]['name']
                user.save(update_fields=['erp_lead_id'])
                print("lead updadted")
            else:

                # if DEBUG:
                #     url = 'http://3.142.247.16/api/resource/Lead'
                # else:
                url = 'https://crm.alnafi.com/api/resource/Lead'

                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
                if response.status_code == 200:
                    lead_data = response.json()
                    erp_lead_id = lead_data['data']['name']
                    if erp_lead_id:
                        user.erp_lead_id = erp_lead_id
                        user.save(update_fields=['erp_lead_id'])
                        print("lead created")
    except Exception as e:
        print('Error occurred while creating lead:')      
        print('Error:', response.status_code)
        print('Error:', response.text)
        print(e)
    # post_save.connect(send_lead_post_request, sender=Thinkific_Users_Enrollments)
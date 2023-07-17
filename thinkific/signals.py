from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from .models import Thinkific_User, Thinkific_Users_Enrollments
from requests.exceptions import RequestException
from user.constants import COUNTRY_CODES

@receiver(post_save, sender=Thinkific_Users_Enrollments)
def send_lead_post_request(sender, instance, created, **kwargs):
    source='Thinkific'
    thinkific_user = usersignal(instance,source)
        
#thinkific user par signal laga jab user bane phir uski eenrollemnt check kar phir agar enrollment
#ho to phir enrolllment ka course check kar phir lead bana
#agar product demo he to phir enrollment lead he

def usersignal(instance,source):
    post_save.disconnect(send_lead_post_request, sender=Thinkific_Users_Enrollments)
    # if instance.is_processing:
    #     return

    # print("instance", instance.user_enrollments.all())
    # print(enrollment[0])
    try:
        # enrollment = instance.user_enrollments.all()
        user = instance.user_id
        if instance.course_name.startswith("demo"):
            api_key = '2b4b9755ecc2dc7'
            api_secret = '8d71fb9b172e2aa'
            headers = {
                'Authorization': f'token {api_key}:{api_secret}',
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
            
            data = {
                    "first_name": user.first_name or None,
                    "last_name": user.last_name if hasattr(user, 'last_name') else None,
                    "email_id": user.email or None,
                    "mobile_no": user.phone if hasattr(user, 'phone') else None,
                    "country": country_name,
                    "source": source,
                    "product_name": instance.course_name if hasattr(instance, 'course_name') else None,
                    # Add other fields from the Main_User model to the data dictionary as needed
                }
            url = f'https://crm.alnafi.com/api/resource/Lead?fields=["name","email_id"]&filters=[["Lead","email_id","=","{user.email}"]]'
            response = requests.get(url, headers=headers)
            lead_data = response.json()
            # print(lead_data['data'])
            
            already_existed = len(lead_data["data"]) > 0
            # print(already_existed)
            if already_existed:
                url = 'https://crm.alnafi.com/api/resource/Lead'
                response = requests.put(url, headers=headers, json=data)
                print(response.json())
                user.erp_lead_id = lead_data['data'][0]['name']
                print("lead updated")
                user.save(update_fields=['erp_lead_id'])
            else:
                print("in else")
                post_url = 'https://crm.alnafi.com/api/resource/Lead'
                response = requests.post(post_url, headers=headers, json=data)
                response.raise_for_status()
                # print("response.status_code",response.status_code)
                if response.status_code == 200:
                    lead_data = response.json()
                    erp_lead_id = lead_data['data']['name']
                    if erp_lead_id:
                        print("lead id exists")
                        user.erp_lead_id = erp_lead_id
                        user.save(update_fields=['erp_lead_id'])
                        print("Lead created successfully!")   
    except Exception as e:
        # print('Error occurred while creating lead:')      
        # print('Error:', response.status_code)
        # print('Error:', response.text)
        print(e)
    post_save.connect(send_lead_post_request, sender=Thinkific_Users_Enrollments)
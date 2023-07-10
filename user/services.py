from django.middleware import csrf
from django.shortcuts import render
from .models import AlNafi_User, IslamicAcademy_User, Main_User, User
from django.db.models import Q
from django.conf import settings
from django.utils.timezone import is_naive, make_aware, utc
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date, datetime, timedelta
from payment.models import UBL_IPG_Payment, Stripe_Payment, Easypaisa_Payment, Main_Payment
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .serializers import AlnafiUserSerializer, IslamicAcademyUserSerializer, MainUserSerializer  
import threading
import boto3
import environ
from datetime import datetime
from calendar import monthrange
from django.db.models import Q
from rest_framework.response import Response


env = environ.Env()
env.read_env()

def search_employees(q):
    employees = User.objects.all().values()
    return employees



def upload_csv_to_s3(df,file_name):
    s3 = boto3.client('s3')
    bucket_name = env("AWS_STORAGE_BUCKET_NAME")
    object_name = file_name
    upload_to_s3 = s3.put_object(Bucket=bucket_name, Key=object_name, Body=df)
    print(upload_to_s3)
    return s3

def paying_users_details(query_time, is_converted):
    converted_users = []
    converted = []
    # return Response("vdfidfjk")
    all_paid_users_products = list(Main_Payment.objects.filter(source='Al-Nafi').values("user__email", "product__product_name"))
    # return Response("vdfidfjk")
    # print(all_paid_users_products)
    all_paid_users_ids = list(Main_Payment.objects.filter(source='Al-Nafi').values_list("user__id", flat=True))
    # return Response("vdfidfjk")
    all_paid_users = query_time.filter(id__in=all_paid_users_ids).values("id","username","email", "first_name", "last_name","source","phone","address","country","created_at")    
    # return Response("vdfidfjk")
    
    all_unpaid_users = query_time.exclude(id__in=all_paid_users_ids)
    if is_converted =='true':
        for user in all_paid_users:
            converted_users.append(user)
            converted.append(True)
    elif is_converted == 'false':
        for user in all_unpaid_users:
            converted_users.append(user)
            converted.append(False)
    else:
        for user in all_paid_users:
            converted_users.append(user)
            converted.append(True)
            
        for user in all_unpaid_users:
            converted_users.append(user)
            converted.append(False) 
       
    response = {"converted_users":converted_users, "converted": converted, "products":all_paid_users_products}
    return response


def search_users(q, start_date, end_date, is_converted,source):
    # users = Main_User.objects.all().values()
    users = Main_User.objects.values(
        "id", "email", "username", "first_name", "last_name", "source", "internal_source",
        "phone", "address", "country", "language", "created_at", "modified_at", "verification_code",
        "isAffiliate", "how_did_you_hear_about_us", "affiliate_code", "isMentor", "is_paying_customer",
        "role", "erp_lead_id"
    )
    # print(users)
    if source:
        users = users.filter(source=source)
    
    if not start_date:
        first_user = users.exclude(created_at=None).last()
        # date_time_obj = first_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        date_time_obj = first_user['created_at'].strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")     
        start_date = new_date_obj

    if not end_date:
        last_user = users.exclude(created_at=None).first()
        # date_time_obj = last_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        date_time_obj = last_user['created_at'].strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")      
        end_date = new_date_obj
        
        
    if q:
        users = users.filter(
            Q(email__iexact=q) | Q(username__iexact=q) | Q(first_name__iexact=q)| Q(id__iexact=q))   
    users = users.filter(Q(created_at__date__lte = end_date) & Q(created_at__date__gte = start_date))
    users = paying_users_details(users, is_converted)
    return users 




def no_users_month(users):
    current_month = datetime.now().month
    current_year = datetime.now().year

    _, num_days = monthrange(current_year, current_month)

    dates = [datetime(current_year, current_month-1, day).date() for day in range(1, num_days + 1)]

    users = users.filter(created_at__date__in=dates)
    converted_users = paying_users_details(users, None)
    serializer = MainUserSerializer(converted_users['converted_users'], many=True)
    for i in range(len(serializer.data)):
        serializer.data[i]['is_paying_customer'] = converted_users['converted'][i]

    paid_users = [data for data in serializer.data if data['is_paying_customer']]
    unpaid_users = [data for data in serializer.data if not data['is_paying_customer']]

    paid_user_dict = {user['created_at'].split('T')[0]: [] for user in paid_users}
    unpaid_user_dict = {user['created_at'].split('T')[0]: [] for user in unpaid_users}
    user_dict = {user.created_at.date(): [] for user in users}

    for user in paid_users:
        paid_user_dict[user['created_at'].split('T')[0]].append(user)

    for user in unpaid_users:
        unpaid_user_dict[user['created_at'].split('T')[0]].append(user)

    for user in users:
        user_dict[user.created_at.date()].append(user)

    response_data = []
    total_users = 0

    for date in dates:
        str_date_key = str(date)[:10]
        paid_users_for_date = paid_user_dict.get(str_date_key, [])
        unpaid_users_for_date = unpaid_user_dict.get(str_date_key, [])
        all_users_for_date = user_dict.get(date, [])

        serialized_users = MainUserSerializer(all_users_for_date, many=True).data
        total_users += len(serialized_users)
        response_data.append({
            'date': date,
            'paid_users': len(paid_users_for_date),
            'unpaid_users': len(unpaid_users_for_date),
            'all_users': len(serialized_users)
        })

    response_data.insert(0, {'total_users': total_users})
    response_data.insert(1, {'converted_users': len(paid_users)})
    response_data.insert(2, {'unconverted_users': len(unpaid_users)})

    return response_data






    

def loginUser(request, response, user, sameDomain):
    if not response.data:
        response.data = {}
    data = get_tokens_for_user(user)
    if sameDomain:
        response = set_auth_token(
            response, settings.SIMPLE_JWT['AUTH_COOKIE'], data["access"])
        response = set_auth_token(
            response, settings.SIMPLE_JWT['REFRESH_COOKIE'], data["refresh"])
    else:
        response.data[settings.SIMPLE_JWT['AUTH_COOKIE']] = data["access"]
        response.data[settings.SIMPLE_JWT['REFRESH_COOKIE']] = data["refresh"]
    csrf.get_token(request)
    # print("response_data", response.data)
    response.data["Success"] = "Login successfully"
    return response

def set_auth_token(response, key, value):
    # print("key", key)
    # print("value", value)
    # print("response data", response.data)
    response.set_cookie(
        key=key,
        value=value,
        expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
    )
    return response


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
def checkSameDomain(request):
    backendDomain = request.get_host().split(":")[0]
    print("request meta",request.META)
    sameDomain = False
    if 'HTTP_ORIGIN' in request.META:
        frontendDomain = request.META['HTTP_ORIGIN'].split(":")[0]
        print("frontendDomain",frontendDomain)
        if (frontendDomain == backendDomain):
            sameDomain = True
    return sameDomain

def make_utc(dt):
    if settings.USE_TZ and is_naive(dt):
        return make_aware(dt, timezone=utc)
    return dt

def aware_utcnow():
    return make_utc(datetime.utcnow())

class GroupPermission(BasePermission):
    def has_permission(self, request, view):
        required_groups = getattr(view, 'required_groups', None)  # Change to 'required_groups'
        if required_groups is None:
            return True
        user_groups = request.user.groups.values_list('name', flat=True)  # Get the names of all user groups
        if any(group in user_groups for group in required_groups):  # Check if any required group is present in user_groups
            return True
        else:
            data = {
                "detail": "You do not have permission to access this API.",
                "has_perm": False
            }
            raise PermissionDenied(data)






# from django.db.models import Subquery, OuterRef

# def paying_users_details(query_time, is_converted):
#     converted_users = []
#     converted = []

#     all_paid_users = query_time.filter(
#         id__in=Main_Payment.objects.filter(source='Al-Nafi').values_list('user_id', flat=True)
#     ).values('id', 'username', 'email', 'first_name', 'last_name', 'source', 'phone', 'address', 'country', 'created_at')

#     all_unpaid_users = query_time.exclude(source='Al-Nafi')

#     if is_converted == 'true':
#         converted_users = list(all_paid_users)
#         converted = [True] * len(converted_users)
#     elif is_converted == 'false':
#         converted_users = list(all_unpaid_users)
#         converted = [False] * len(converted_users)
#     else:
#         converted_users = list(all_paid_users) + list(all_unpaid_users)
#         converted = [True] * len(all_paid_users) + [False] * len(all_unpaid_users)

#     all_paid_users_products = Main_Payment.objects.filter(
#         source='Al-Nafi', user_id__in=all_paid_users.values_list('id', flat=True)
#     ).values('user__email', 'product__product_name')

#     response = {"converted_users": converted_users, "converted": converted, "products": all_paid_users_products}
#     return response



# def search_users(q, start_date, end_date, is_converted, source):
#     users = Main_User.objects.all().values()

#     if source:
#         users = users.filter(source=source)

#     if not start_date:
#         first_user = users.exclude(created_at=None).last()
#         date_time_obj = first_user['created_at'].strftime("%Y-%m-%d %H:%M:%S.%f%z")
#         new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")
#         start_date = new_date_obj

#     if not end_date:
#         last_user = users.exclude(created_at=None).first()
#         date_time_obj = last_user['created_at'].strftime("%Y-%m-%d %H:%M:%S.%f%z")
#         new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")
#         end_date = new_date_obj

#     if q:
#         users = users.filter(
#             Q(email__iexact=q) | Q(username__iexact=q) | Q(first_name__iexact=q) | Q(id__iexact=q))

#     users = users.filter(Q(created_at__date__lte=end_date) & Q(created_at__date__gte=start_date))
#     converted_users = paying_users_details(users, is_converted)
    
#     converted_dict = {user['email']: converted for user, converted in zip(users, converted_users)}

#     response = {"converted_users": users, "converted": converted_dict, "products": converted_users['products']}
#     return response


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
    return s3

def paying_users_details(query_time, is_converted):
    converted_users = []
    converted = []
    all_paid_users_ids = list(Main_Payment.objects.all().values_list("user__id", flat=True))
    all_paid_users = query_time.filter(id__in=all_paid_users_ids).values("id","username","email", "first_name", "last_name","source","phone","address","country","created_at")    
    print("all_paid_users",all_paid_users)
    all_unpaid_users = query_time.exclude(id__in=all_paid_users_ids)
    print("all_unpaid_users",all_unpaid_users)
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
                     
    
    # for user in query_time:
    #     paying_user = Main_Payment.objects.filter(user=user).exists()      
    #     if is_converted == 'true':
    #         if paying_user:
    #             converted_users.append(user)
    #             converted.append(True)
    #     elif is_converted == 'false':
    #         if not paying_user:
    #             converted_users.append(user)
    #             converted.append(False)
    #     else:
    #         if paying_user:
    #             converted_users.append(user)
    #             converted.append(True)
    #         else:
    #             converted_users.append(user)
    #             converted.append(False)   
    print("converted_users",converted_users)            
    response = {"converted_users":converted_users, "converted": converted}
    return response


def search_users(q, start_date, end_date, is_converted,source):
    users = Main_User.objects.all()
    if source:
        users = users.filter(source=source)
    
    if not start_date:
        first_user = users.exclude(created_at=None).last()
        date_time_obj = first_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")     
        start_date = new_date_obj

    if not end_date:
        last_user = users.exclude(created_at=None).first()
        date_time_obj = last_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")      
        end_date = new_date_obj
        
        
    if q:
        users = users.filter(
            Q(email__iexact=q) | Q(username__iexact=q) | Q(first_name__iexact=q)| Q(id__iexact=q))   
    print(users)
    users = users.filter(Q(created_at__date__lte = end_date) & Q(created_at__date__gte = start_date))
    print(users)
    users = paying_users_details(users, is_converted)

    return users 

def alnafi_user(q, start_date, end_date, is_converted):
    if not start_date:
        first_user = Main_User.objects.exclude(created_at=None).first()
        date_time_obj = first_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")     
        start_date = new_date_obj

    if not end_date:
        last_user = Main_User.objects.exclude(created_at=None).last()
        date_time_obj = last_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")      
        end_date = new_date_obj

    if q:
        queryset = Main_User.objects.filter(
            Q(email__iexact=q) | Q(username__iexact=q) | Q(first_name__iexact=q))
        query_time = queryset.filter(Q(created_at__date__lte = end_date) & Q(created_at__date__gte = start_date))
        paying_user_queryset = paying_users_details(query_time, is_converted)
    else:
        query_time = Main_User.objects.filter(created_at__date__gte = start_date, created_at__date__lte = end_date)
        paying_user_queryset = paying_users_details(query_time, is_converted)
        
    return paying_user_queryset

def islamic_user(q, start_date, end_date, is_converted): 
    if not start_date:
        first_user = IslamicAcademy_User.objects.exclude(created_at=None).first()
        date_time_obj = first_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")                                                                                      
        start_date = new_date_obj
    
    if not end_date:
        last_user = IslamicAcademy_User.objects.exclude(created_at=None).last()
        date_time_obj = last_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")      
        end_date = new_date_obj  
         
    if q:
        if is_converted == 'true':
            paying_users = IslamicAcademy_User.objects.filter(is_paying_customer=True)
            queryset = paying_users.filter(
            Q(email__iexact=q) | Q(username__iexact=q)| Q(first_name__iexact=q)) 
            query_time = queryset.filter(Q(created_at__date__gte = start_date) & Q(created_at__date__lte = end_date))
        elif is_converted == 'false':
            paying_users = IslamicAcademy_User.objects.filter(is_paying_customer=False)
            queryset = paying_users.filter(
            Q(email__iexact=q) | Q(username__iexact=q)| Q(first_name__iexact=q)) 
            query_time = queryset.filter(Q(created_at__date__gte = start_date) & Q(created_at__date__lte = end_date))
        else:
            queryset = IslamicAcademy_User.objects.filter(
            Q(email__iexact=q) | Q(username__iexact=q)| Q(first_name__iexact=q)) 
            query_time = queryset.filter(Q(created_at__gte = start_date) & Q(created_at__lte = end_date))
            
        
    else:
        if is_converted == 'true':
            paying_users = IslamicAcademy_User.objects.filter(is_paying_customer=True)
            query_time = paying_users.filter(Q(created_at__gte = start_date) & Q(created_at__lte = end_date))
        elif is_converted == 'false':
            paying_users = IslamicAcademy_User.objects.filter(is_paying_customer=False)
            query_time = paying_users.filter(Q(created_at__gte = start_date) & Q(created_at__lte = end_date))
        else:
            queryset = IslamicAcademy_User.objects.all()
            query_time = queryset.filter(Q(created_at__gte = start_date) & Q(created_at__lte = end_date))
            
    return query_time




def no_of_users(start_date,end_date,source):
    users = Main_User.objects.all().values()
    if source:
        users = users.filter(source=source)
        
    if not start_date:
        first_user = users.exclude(created_at=None).first()
        date_time_obj = first_user['created_at'].strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")     
        start_date = str(new_date_obj.date())
      
    
    if not end_date:
        last_user = users.exclude(created_at=None).last()
        date_time_obj = last_user['created_at'].strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")      
        end_date = str(new_date_obj.date())  
          
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date() 
    
    # print(start_date)
    # print(end_date)      
    delta = end_date_obj - start_date_obj
    dates = []
    for i in range(delta.days + 1):
        date = start_date_obj + timedelta(days=i)
        dates.append(date)
    
    users = users.filter(created_at__date__in=dates)
    user_dict = {}
    for user in users:
        if user.created_at.date() in user_dict:
            user_dict[user.created_at.date()].append(user)
        else:
            user_dict[user.created_at.date()] = [user]
    response_data = []
    
    for date in dates:
        if date in user_dict:
            users_for_date = user_dict[date]
            # serialized_users = MainUserSerializer(users_for_date, many=True).data
        else:
            users_for_date = []

        response_data.append({
            'date': date,
            'users': len(users_for_date)
        })
    print(response_data)
    return response_data

def alnafi_no_users(start_date,end_date):
    if not start_date:
        first_user = AlNafi_User.objects.exclude(created_at=None).first()
        date_time_obj = first_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")     
        start_date = str(new_date_obj.date())
        
    if not end_date:
        last_user = AlNafi_User.objects.exclude(created_at=None).last()
        date_time_obj = last_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")      
        end_date = str(new_date_obj.date())
        
    # print("start_date", start_date)
    # print("end_date", end_date)
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()       
    delta = end_date_obj - start_date_obj
    dates = []
    for i in range(delta.days + 1):
        date = start_date_obj + timedelta(days=i)
        dates.append(date)
        
    users = AlNafi_User.objects.filter(created_at__date__in=dates)
    user_dict = {}
    for user in users:
        if user.created_at.date() in user_dict:
            user_dict[user.created_at.date()].append(user)
        else:
            user_dict[user.created_at.date()] = [user]
    response_data = []
    
    
    for date in dates:
        if date in user_dict:
            users_for_date = user_dict[date]
            serialized_users = AlnafiUserSerializer(users_for_date, many=True).data
        else:
            serialized_users = []

        response_data.append({
            'date': date,
            'users': len(serialized_users)
        })
    return response_data

def islamic_no_users(start_date,end_date):
    if not start_date:
        first_user = IslamicAcademy_User.objects.first()
        date_time_obj = first_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")     
        start_date = str(new_date_obj.date())
        
    if not end_date:
        last_user = IslamicAcademy_User.objects.last()
        date_time_obj = last_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")      
        end_date = str(new_date_obj.date())
    
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()       
    delta = end_date_obj - start_date_obj
    dates = []
    for i in range(delta.days + 1):
        date = start_date_obj + timedelta(days=i)
        dates.append(date)
        
    users = IslamicAcademy_User.objects.filter(created_at__date__in=dates)
    user_dict = {}
    for user in users:
        if user.created_at.date() in user_dict:
            user_dict[user.created_at.date()].append(user)
        else:
            user_dict[user.created_at.date()] = [user]
            
    response_data = []
    for date in dates:
        if date in user_dict:
            users_for_date = user_dict[date]
            serialized_users = IslamicAcademyUserSerializer(users_for_date, many=True).data
        else:
            serialized_users = []

        response_data.append({
            'date': date,
            'users': len(serialized_users)
        })
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


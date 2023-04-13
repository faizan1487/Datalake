from django.middleware import csrf
from django.shortcuts import render
from .models import AlNafi_User, IslamicAcademy_User
from django.db.models import Q
from django.conf import settings
from django.utils.timezone import is_naive, make_aware, utc
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date, datetime, timedelta
from payment.models import UBL_IPG_Payment, Stripe_Payment, Easypaisa_Payment
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .serializers import AlnafiUserSerializer, IslamicAcademyUserSerializer    
import threading

def islamic_Paying_user(isPaying, exact,date):
    if date:
        pass
    else:
        first_user = IslamicAcademy_User.objects.first()
        date_time_obj = first_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")     
        date = new_date_obj
    if exact =='True':
        queryset = IslamicAcademy_User.objects.filter(created_at__date=date)
    else:   
        queryset = IslamicAcademy_User.objects.filter(created_at__date__gte=date) 
        
    if isPaying == 'True':
        queryset = queryset.filter(is_paying_customer=True)
        return queryset
    elif isPaying == 'False':
        queryset = queryset.filter(is_paying_customer=False)    
        return queryset
    return queryset
        

def alnafi_Paying_user(isPaying, exact, date):
    if date:
        pass
    else:
        first_user = AlNafi_User.objects.first()
        date_time_obj = first_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")     
        date = new_date_obj    
    if exact =='True':
        query_time = AlNafi_User.objects.filter(created_at__date=date)
    else:  
        query_time = AlNafi_User.objects.filter(created_at__date__gte=date)
    paying_user_queryset = paying_user(query_time, isPaying)
    return paying_user_queryset

def alnafi_user(q, start_date, end_date, isPaying):
    if start_date:
        pass
    else:
        first_user = AlNafi_User.objects.first()
        date_time_obj = first_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")     
        start_date = new_date_obj
    if end_date:
        pass
    else:
        last_user = AlNafi_User.objects.last()
        date_time_obj = last_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")      
        end_date = new_date_obj
    
    if q:
        queryset = AlNafi_User.objects.filter(
            Q(email__iexact=q) | Q(username__iexact=q) | Q(first_name__iexact=q))
        query_time = queryset.filter(Q(created_at__date__lte = end_date) & Q(created_at__date__gte = start_date))
        paying_user_queryset = paying_users_details(query_time, isPaying)

    else:
        query_time = AlNafi_User.objects.filter(created_at__date__gte = start_date, created_at__date__lte = end_date)
        paying_user_queryset = paying_users_details(query_time, isPaying)
    return paying_user_queryset

def islamic_user(q, start_date, end_date, isPaying): 
    if start_date:
        pass
    else:
        first_user = IslamicAcademy_User.objects.first()
        date_time_obj = first_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")                                                                                      
        start_date = new_date_obj
    if end_date:
        pass
    else:
        last_user = IslamicAcademy_User.objects.last()
        date_time_obj = last_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")      
        end_date = new_date_obj   
    if q:
        if isPaying == 'True':
            paying_users = IslamicAcademy_User.objects.filter(is_paying_customer=True)
            queryset = paying_users.filter(
            Q(email__iexact=q) | Q(username__iexact=q)| Q(first_name__iexact=q)) 
            query_time = queryset.filter(Q(created_at__date__gte = start_date) & Q(created_at__date__lte = end_date))
        elif isPaying == 'False':
            paying_users = IslamicAcademy_User.objects.filter(is_paying_customer=False)
            queryset = paying_users.filter(
            Q(email__iexact=q) | Q(username__iexact=q)| Q(first_name__iexact=q)) 
            query_time = queryset.filter(Q(created_at__date__gte = start_date) & Q(created_at__date__lte = end_date))
        else:
            queryset = IslamicAcademy_User.objects.filter(
            Q(email__iexact=q) | Q(username__iexact=q)| Q(first_name__iexact=q)) 
            query_time = queryset.filter(Q(created_at__gte = start_date) & Q(created_at__lte = end_date))
    else:
        if isPaying == 'True':
            paying_users = IslamicAcademy_User.objects.filter(is_paying_customer=True)
            query_time = paying_users.filter(Q(created_at__gte = start_date) & Q(created_at__lte = end_date))
        elif isPaying == 'False':
            paying_users = IslamicAcademy_User.objects.filter(is_paying_customer=False)
            query_time = paying_users.filter(Q(created_at__gte = start_date) & Q(created_at__lte = end_date))
        else:
            queryset = IslamicAcademy_User.objects.all()
            query_time = queryset.filter(Q(created_at__gte = start_date) & Q(created_at__lte = end_date))
            
    return query_time


def alnafi_no_users(start_date,end_date):
    if start_date:
            pass
    else:
        first_user = AlNafi_User.objects.first()
        date_time_obj = first_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")     
        start_date = str(new_date_obj.date())
        
    if end_date:
        pass
    else:
        last_user = AlNafi_User.objects.last()
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
    if start_date:
            pass
    else:
        first_user = IslamicAcademy_User.objects.first()
        date_time_obj = first_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")     
        start_date = str(new_date_obj.date())
        
    if end_date:
        pass
    else:
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
    sameDomain = False
    if 'HTTP_ORIGIN' in request.META:
        frontendDomain = request.META['HTTP_ORIGIN'].split(":")[0]
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
        required_group = getattr(view, 'required_group', None)
        if required_group is None:
            return True
        if request.user.groups.filter(name=required_group).exists():
            return True
        else:
            data = {
                "detail": "You do not have permission to access this API.",
                "has_perm": False
                }
            raise PermissionDenied(data)

def paying_users_details(query_time, isPaying):
    if isPaying:
        paying_users = []
        for user in query_time:
            ubl_user = UBL_IPG_Payment.objects.filter(customer_email=user.email)
            # easypaisa_user = Easypaisa_Payment.objects.filter(customer_email=user.email)
            # stripe_user = Stripe_Payment.objects.filter(customer_email=user.email)        
            if isPaying == 'True':
                #  or easypaisa_user or stripe_user
                if ubl_user:
                    paying_users.append(user)
            else:
                #  or easypaisa_user or stripe_user
                if ubl_user:
                    pass
                else:
                    paying_users.append(user)
        return paying_users
    else:
        return query_time


def paying_user(query_time, isPaying):
    paying_users = []
    is_paying = []
    for user in query_time:
        ubl_user = UBL_IPG_Payment.objects.filter(customer_email=user.email)
        # easypaisa_user = Easypaisa_Payment.objects.filter(customer_email=user.email)
        # stripe_user = Stripe_Payment.objects.filter(customer_email=user.email)
        # for payment in ubl_user:
        # or easypaisa_user or stripe_user
        if ubl_user:
            paying_users.append(user)
            is_paying.append('True')
        else:
            paying_users.append(user)
            is_paying.append('False')
            
    response = {"paying_users":paying_users,
                "is_paying": is_paying}
    
    return response


# def paying_user(query_time, isPaying):
#     paying_users = []
#     is_paying = []
#     def process_user(user):
#         ubl_user = UBL_IPG_Payment.objects.filter(customer_email=user.email)
#         # for payment in ubl_user:
#         if ubl_user:
#             paying_users.append(user)
#             is_paying.append('True')
#         else:
#             paying_users.append(user)
#             is_paying.append('False')
#     def process_user2(user):
#         easypaisa_user = Easypaisa_Payment.objects.filter(customer_email=user.email)
#         # for payment in ubl_user:
#         if easypaisa_user:
#             paying_users.append(user)
#             is_paying.append('True')
#         else:
#             paying_users.append(user)
#             is_paying.append('False')
    
#     def process_user3(user):
#         stripe_user = Stripe_Payment.objects.filter(customer_email=user.email)
#         # for payment in ubl_user:
#         if stripe_user:
#             paying_users.append(user)
#             is_paying.append('True')
#         else:
#             paying_users.append(user)
#             is_paying.append('False')
            
#     # Create a list of threads
#     threads = []

#     # Iterate over the users and create a thread for each user
#     for user in query_time:
#         threading.Thread(target=process_user, args=(user,)).start()
#         threading.Thread(target=process_user2, args=(user,)).start()
#         threading.Thread(target=process_user3, args=(user,)).start()
    
        
#     response = {"paying_users":paying_users,
#                 "is_paying": is_paying
#                 }
#     return response
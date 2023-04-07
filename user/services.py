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


def paying_users(query_time, isPaying):
    paying_users = []
    for user in query_time:
        pay_users = []
        ubl_user = UBL_IPG_Payment.objects.filter(customer_email=user.email)
        easypaisa_user = Easypaisa_Payment.objects.filter(customer_email=user.email)
        stripe_user = Stripe_Payment.objects.filter(customer_email=user.email)
        pay_users.append(ubl_user)
        pay_users.append(easypaisa_user)
        pay_users.append(stripe_user)
        for pay_user in pay_users:
            if isPaying: 
                for p_user in pay_user:
                    if isPaying:
                        if p_user.customer_email == user.email:
                            paying_users.append(user)
                        else:
                            pass
                    else:
                        if p_user.customer_email != user.email:
                            paying_users.append(user)
            else:
                return query_time                   
    return paying_users
    
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
        paying_user_queryset = paying_users(query_time, isPaying)

    else:
        query_time = AlNafi_User.objects.filter(created_at__date__gte = start_date, created_at__date__lte = end_date)
        paying_user_queryset = paying_users(query_time, isPaying)
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
    print("make_utc",make_utc(datetime.utcnow()))
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


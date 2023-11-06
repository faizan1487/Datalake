from django.middleware import csrf
from django.shortcuts import render
from numpy import source
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
from django.db.models import Prefetch


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
    # print(upload_to_s3)
    return s3

def paying_users_details(query_time, is_converted):
    converted_users = []
    converted = []
    sources = ['Al-Nafi','NEW ALNAFI']
    all_paid_users_products = list(Main_Payment.objects.filter(source__in=sources).values("user__email", "product__product_name"))
    all_paid_users_ids = list(Main_Payment.objects.filter(source__in=sources).values_list("user__id", flat=True))
    all_paid_users = query_time.filter(id__in=all_paid_users_ids).values("id","username","email", "first_name", "last_name","source","phone","address","country","created_at","academy_demo_access","internal_source")    
    
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
       
    # response = {"converted_users":converted_users, "converted": converted}
    response = {"converted_users":converted_users, "converted": converted, "products":all_paid_users_products}
    return response

def search_users(q, start_date, req_end_date, is_converted,source,request,phone,academy_demo_access):
    users = Main_User.objects.exclude(email__endswith="yopmail.com").values(
        "id", "email", "username", "first_name", "last_name", "source", "internal_source",
        "phone", "address", "country", "language", "created_at", "modified_at", "verification_code",
        "isAffiliate", "how_did_you_hear_about_us", "affiliate_code", "isMentor", "is_paying_customer",
        "role", "erp_lead_id","academy_demo_access"
    )
    if source:
        if source == 'Academy':
            users = users.filter(Q(internal_source='Academy') | Q(academy_demo_access=True))
        elif source == 'Al-Nafi':
            users = users.filter(Q(source='Al-Nafi') & ~Q(internal_source='Al-Nafi') & Q(academy_demo_access=False))
        else:
            users = users.filter(source=source)

    if academy_demo_access:
        users = users.filter(academy_demo_access=academy_demo_access)
    

    
    
    if users:
        if not start_date:
            first_user = users.exclude(created_at=None).last()
            if first_user and first_user['created_at']:
                date_time_obj = first_user['created_at'].strftime("%Y-%m-%d %H:%M:%S.%f")
                new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")
                start_date = new_date_obj

       
        if not req_end_date:
            last_user = users.exclude(created_at=None).first()
            if last_user and last_user['created_at']:
                date_time_obj = last_user['created_at'].strftime("%Y-%m-%d %H:%M:%S.%f")
                new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")
                end_date = new_date_obj

        # print(request.user)
        if req_end_date:
            end_date = datetime.strptime(req_end_date, "%Y-%m-%d")
            end_date = end_date + timedelta(days=1)

        if q:
            users = users.filter(
                Q(email__icontains=q) | Q(username__icontains=q) | Q(first_name__icontains=q)| Q(id__icontains=q))   
            
        if q:
            if request.user.is_admin:
                users = users.filter(email__icontains=q)
            else:
                users = users.filter(email__iexact=q)

        if phone:
            phone = phone.strip()
            if phone.startswith("92"):
                phone = "+" + phone
            if request.user.is_admin:
                users = users.filter(phone__icontains=phone)
            else:
                users = users.filter(phone__iexact=phone)

        users = users.filter(Q(created_at__lte = end_date) & Q(created_at__gte = start_date))
        users = paying_users_details(users, is_converted)
    return users 


#PRoduction
def search_active_users(q, start_date, req_end_date, is_converted,source,request,phone,academy_demo_access,page):
    users = Main_User.objects.exclude(email__endswith="yopmail.com")
    # print(users)
    # exclude(user__email__endswith="yopmail.com")

    # if request.user.is_admin:
    if q:
        users = users.filter(email__iexact=q)

    # else:
    #     if q:
    #         users = users.filter(email__iexact=q) if request.user.is_admin else users.filter(email__iexact=q)
    #     else:
    #         response = {'success':False}
    #         return response
    
    # print("users after q", users)

    if source:
        if source == 'Academy':
            users = users.filter(source='Al-Nafi', internal_source='Academy', academy_demo_access=True)
        elif source == 'Al-Nafi':
            # print("source isalnafi")
            users = users.filter(Q(source='Al-Nafi') & ~Q(internal_source='Al-Nafi') & Q(academy_demo_access=False))
            # users = users.filter(source='Al-Nafi', internal_source!='Al-Nafi', academy_demo_access=False)
        else:
            users = users.filter(source=source)

    if academy_demo_access:
        users = users.filter(academy_demo_access=academy_demo_access)
       
    if users:
        if not start_date:
            first_user = users.exclude(created_at=None).last()
            if first_user and first_user.created_at:
                date_time_obj = first_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f")
                new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")
                start_date = new_date_obj
       
        if not req_end_date:
            last_user = users.exclude(created_at=None).first()
            if last_user and last_user.created_at:
                date_time_obj = last_user.created_at.strftime("%Y-%m-%d %H:%M:%S.%f")
                new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")
                end_date = new_date_obj

        if req_end_date:
            end_date = datetime.strptime(req_end_date, "%Y-%m-%d")
            end_date = end_date + timedelta(days=1)
            
        # if q:
            # users = users.filter(email__iexact=q) if request.user.is_admin else users.filter(email__iexact=q)

        if phone:
            phone = phone.strip()
            if phone.startswith("92"):
                phone = "+" + phone
            if request.user.is_admin:
                users = users.filter(phone__icontains=phone)
            else:
                users = users.filter(phone__iexact=phone)

     
        users = users.filter(Q(created_at__lte=end_date) & Q(created_at__gte=start_date))

        # print("users after date filter",users)


        page_size = 10  # Number of payments per page
        # Calculate the start and end indices for slicing
        start_index = (page - 1) * page_size
        end_index = start_index + page_size

        sliced_users = users[start_index:end_index]
        paying_users = active_paying_users_details(sliced_users, is_converted)
        users = {"converted_users":paying_users['users'], "count":paying_users['count'], 'success':True}
        return users
    else:
        users = {"converted_users": users, "count": 0, 'success':False}
        return users


#PRODUCTION
def active_paying_users_details(query_time,is_converted):
    user_list = []
    if is_converted =='true':
        # all_paid_users_products = list(Main_Payment.objects.filter(source='Al-Nafi').values("user__email", "product__product_name"))
        sources = ['Al-Nafi','NEW ALNAFI']
        all_paid_users_ids = list(Main_Payment.objects.filter(source__in=sources).values_list("user__id", flat=True))
        # print("all_paid_users_ids",all_paid_users_ids)
        all_paid_users = []
        for i in range(len(query_time)):
            for j in range(len(all_paid_users_ids)):
                if query_time[i].id == all_paid_users_ids[j]:
                    # print("all_paid_users_ids[j]",all_paid_users_ids[j])
                    # print("query_time[i].id",query_time[i].id)
                    all_paid_users.append(query_time[i])
        # print("all_paid_users",all_paid_users)

        users_count = len(all_paid_users_ids)
        # print(users_count)

        for user in all_paid_users:
            payments = user.user_payments.all().values()
            # print("payments",payments)
            # payments = payments.exclude(expiration_datetime__isnull=True).order_by('-order_datetime')
            payments = payments.order_by('-order_datetime')
            # print("user payments",payments)
            if payments:
                # print(user)
                user_dict = {
                    'username': user.username,
                    'phone': user.phone,
                    'academy_demo_access': user.academy_demo_access,
                    'address': user.address,
                    'affiliate_code': user.affiliate_code,
                    'blocked': user.blocked,
                    'country': user.country,
                    'created_at': user.created_at,
                    'date_joined': user.date_joined,
                    'easypaisa_number': user.easypaisa_number,
                    'email': user.email,
                    'erp_lead_id': user.erp_lead_id,
                    'facebook_user_id': user.facebook_user_id,
                    'first_name': user.first_name,
                    'google_user_id': user.google_user_id,
                    'how_did_you_hear_about_us': user.how_did_you_hear_about_us,
                    'id': user.id,
                    'source': user.source,
                    'internal_source': user.internal_source,
                    'isAffiliate': user.isAffiliate,
                    'isMentor': user.isMentor,
                    'is_active': user.is_active,
                    'is_paying_customer': user.is_paying_customer,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser,
                    'language': user.language,
                    'last_name': user.last_name,
                    'meta_data': user.meta_data,
                    'modified_at': user.modified_at
                }

                # if latest_payment.date() > date.today():
                user_dict['is_paying_customer'] = True

                products = list(payments.values('product__product_name'))
                plans = list(payments.values('product__product_plan'))
                payment_list = list(payments)
                for i in range(len(payment_list)):
                    # try:
                    payment_list[i]['user_id'] = user.email
                    payment_list[i]['product_id'] = products[i]['product__product_name']
                    payment_list[i]['plan'] = plans[i]['product__product_plan']
                    # except Exception as e:
                    #     print(e)
                # print(payment_list)
                user_dict['product'] = payment_list[0]['product_id']
                user_dict['plan'] = payment_list[0]['plan']
                user_dict['expiry_date'] = payment_list[0]['expiration_datetime']

                user_list.append(user_dict)
    
    # print("user list", user_list)
    response = {"users":user_list, "count":users_count}
    return response


#LOCAL
# def search_active_users(q, start_date, req_end_date, is_converted, source, request, phone, academy_demo_access, page):
#     users = Main_User.objects.all()

#     if q:
#         users = users.filter(Q(email__iexact=q))

#     if users:
#         users = users.prefetch_related('user_payments')

#         page_size = 10  # Number of payments per page
#         # Calculate the start and end indices for slicing
#         start_index = (page - 1) * page_size
#         end_index = start_index + page_size

#         users = users[start_index:end_index]
#         paying_users = active_paying_users_details(users)
#         users = {"converted_users": paying_users, 'success': True}
#     return users


#LOCAL
# def active_paying_users_details(users):
#     user_list = []

#     for user in users:
#         payments = user.user_payments.exclude(expiration_datetime__isnull=True).order_by('-order_datetime')
#         if payments:
#             payment = payments[0]  # Only interested in the first payment
#             products = payment.product.all()
#             # print(products)
#             # print(products)
#             user_dict = {
#                 'username': user.username,
#                 'phone': user.phone,
#                 'academy_demo_access': user.academy_demo_access,
#                 'address': user.address,
#                 'affiliate_code': user.affiliate_code,
#                 'blocked': user.blocked,
#                 'country': user.country,
#                 'created_at': user.created_at,
#                 'date_joined': user.date_joined,
#                 'easypaisa_number': user.easypaisa_number,
#                 'email': user.email,
#                 'erp_lead_id': user.erp_lead_id,
#                 'facebook_user_id': user.facebook_user_id,
#                 'first_name': user.first_name,
#                 'google_user_id': user.google_user_id,
#                 'how_did_you_hear_about_us': user.how_did_you_hear_about_us,
#                 'id': user.id,
#                 'source': user.source,
#                 'internal_source': user.internal_source,
#                 'isAffiliate': user.isAffiliate,
#                 'isMentor': user.isMentor,
#                 'is_active': user.is_active,
#                 'is_paying_customer': user.is_paying_customer,
#                 'is_staff': user.is_staff,
#                 'is_superuser': user.is_superuser,
#                 'language': user.language,
#                 'last_name': user.last_name,
#                 'meta_data': user.meta_data,
#                 'modified_at': user.modified_at,
#                 'product': products[0].product_name if products else None,  # Assuming Payment has a foreign key to Product
#                 'plan': products[0].product_plan if products else None, # Assuming Payment has a foreign key to
#                 'expiry_date': payment.expiration_datetime,
#             }

#             user_dict['is_paying_customer'] = True

#             user_list.append(user_dict)

#     return user_list




def active_payments(user):
    # print(user)
    payments = user[0].user_payments.all().values()
    # print(payments)
    payments = payments.exclude(expiration_datetime__isnull=True).order_by('-order_datetime')
    # latest_payment = payments.order_by('-order_datetime')[0]['expiration_datetime']
    # latest_payment = payments.order_by('-order_datetime')
    # print(latest_payment[0])
    user = dict(user.values()[0])

    # if latest_payment.date() > date.today():
    user['is_paying_customer'] = True

    def json_serializable(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()  # Convert datetime to ISO 8601 format
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

    products = list(payments.values('product__product_name'))
    plans = list(payments.values('product__product_plan'))
    payment_list = list(payments)
    for i in range(len(payment_list)):
        try:
            payment_list[i]['user_id'] = user['email']
            payment_list[i]['product_id'] = products[i]['product__product_name']
            payment_list[i]['plan'] = plans[i]['product__product_plan']
        except Exception as e:
            print(e)



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
    # print("request meta",request.META)
    sameDomain = False
    if 'HTTP_ORIGIN' in request.META:
        frontendDomain = request.META['HTTP_ORIGIN'].split(":")[0]
        # print("frontendDomain",frontendDomain)
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
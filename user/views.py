from threading import Thread
from django.shortcuts import render
from django.utils.encoding import smart_bytes
from numpy import full
from rest_framework.views import APIView
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from rest_framework.response import Response
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMultiAlternatives
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import logout
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
import jwt
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.html import strip_tags
from jwt.exceptions import ExpiredSignatureError
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.contrib.auth import authenticate
import os
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import pandas as pd
from datetime import datetime

from .models import AlNafi_User, IslamicAcademy_User, Main_User, NavbarLink,PSWFormRecords, Marketing_PKR_Form, Moc_Leads, New_AlNafi_User, CvForms
from .serializers import (AlnafiUserSerializer,UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,
                          SendPasswordResetEmailSerializer,UserPasswordResetSerializer,NavbarSerializer,GroupsSerailizer,MainUserCreateSerializer,
                          NewAlnafiUserSerializer)
from .services import (set_auth_token, checkSameDomain,loginUser,aware_utcnow,no_users_month,
                       upload_csv_to_s3,search_users,search_employees,search_active_users)
from .renderers import UserRenderer
from functools import reduce
import json
from django.http import HttpResponse
from user.constants import COUNTRY_CODES
import csv
from rest_framework.parsers import MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import time
from user.models import Moc_Leads, User
from rest_framework import generics
import environ, requests 
from secrets_api.algorithem import round_robin

env = environ.Env()
env.read_env()
import pandas as pd

class UploadMocLeads(APIView):
    def post(self,request):
        # Read the CSV file into a DataFrame
        data = pd.read_csv('/home/faizan/albaseer/Al-Baseer-Backend/user/MOC Leads - Al Baseer to CRM - Facebook.csv')

        # data = pd.read_csv('/home/faizan/albaseer/Al-Baseer-Backend/user/view_failed_affiliate.csv')
        # data = pd.read_csv('/home/faizan/albaseer/Al-Baseer-Backend/user/failed_affiliate_from_signal.csv')
        # data = pd.read_csv('/home/faizan/albaseer/Al-Baseer-Backend/user/MOC Leads - Al Baseer to CRM - Easy Pay Program.csv')

        # Iterate over rows in the DataFrame
        for index, row in data.iterrows():
            failed_leads = []
            # Extracting data from the row
            full_name = row['full_name']
            email = row['email']
            phone = row['phone']
            country = row['country']
            login_source = row['source']
            created_at_str = row['created_at']    
            if pd.isna(created_at_str):
                created_at = datetime.now()
            else:
                created_at = pd.to_datetime(created_at_str, format="%Y-%m-%d %H:%M:%S.%f%z")
        

            #from signal error file
            # full_name = row['first_name']
            # email = row['email_id']
            # phone = row['mobile_no']
            # country = row['country']
            # login_source = row['source']
            # created_at_str = row['date_joined']    

            form = row['form']
            form = None if pd.isna(form) else form
            advert = row['advert']
            # advert = row['advert detail']
            # created_at = pd.to_datetime(created_at_str, format="%Y/%m/%d %H:%M:%S")
            # try:
            moc, created = Moc_Leads.objects.get_or_create(email=email, defaults={
                'first_name': full_name,
                'phone': phone,
                'email': email,
                'form': form,
                'country': country,
                'login_source': login_source,
                'created_at': created_at,
                'advert': advert,
            })

            if not created:
                moc.first_name = full_name
                moc.email = email
                moc.phone = phone
                moc.form = form
                moc.country = country
                moc.login_source = login_source
                moc.created_at = created_at
                moc.advert = advert
                moc.save()
        # except Exception as e:
            data = {
                'full_name':row['full_name'],
                'email':row['email'],
                'phone': row['phone'],
                'country': row['country'],
                'login_source':row['source'],
                'created_at_str': row['created_at'], 
                'form': row['form'],
                'advert': row['advert']
            }
            failed_leads.append(data)

            # if failed_leads:
            #     with open('view_failed_affiliate.csv', 'a', newline='') as csvfile:
            #         fieldnames = failed_leads[0].keys()
            #         writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            #         if csvfile.tell() == 0:
            #             writer.writeheader()

            #         for lead in failed_leads:
            #             writer.writerow(lead)

        return Response({"msg":"done"})
    

class o_level_leads_moc_model(APIView):
    def post(self,request):
        data = pd.read_csv('/home/uzair/Documents/Al-Baseer-Backend/user/MOC Leads - Al Baseer to CRM - O Levels.csv')
        lst = []
        
        for index, row in data.iterrows():
            full_name = row['full_name']
            phone = row['phone']
            email = row['email']
            form = row['form']
            country = row['country']
            login_source = row['source']
            created_at_str = row['created_at']
            assigned_date = row['assigned_date']
            advert = row["advert"]
            
            assigned_date = datetime.strptime(assigned_date, '%d %b %Y')
            formatted_date = assigned_date.strftime('%Y-%m-%d')

            # You can adjust the format string as needed
            # created_at = pd.to_datetime(created_at_str, format="%m/%d/%Y %H:%M:%S")
            created_at = pd.to_datetime(created_at_str, format="%Y/%m/%d %H:%M:%S")

            # try:
            user, created = Moc_Leads.objects.get_or_create(email=email, defaults={
                'first_name': full_name,
                'phone': phone,
                'email': email,
                'form': form,
                'login_source':login_source,
                'country': country,
                'created_at': created_at,
                'assigned_at':formatted_date,
                'advert': advert
            })

            # If the object was not created (i.e., it already existed), update its attributes
            if not created:
                user.first_name = full_name
                user.email = email
                user.phone = phone
                user.form = form
                user.login_source = login_source
                user.country = country
                user.created_at = created_at
                user.assigned_at = assigned_date
                user.advert = advert
                user.save()

            # except Exception as e:
            #     print(e)
            #     lst.append(row['email'])

        data_Frame = pd.DataFrame(lst)
        data_Frame.to_csv("error.csv")


        return Response("Leads created")


# Create your views here.
class MyPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100


class PSWFormRecord(APIView):
    def post(self,request):
        hear_about_us = request.data['hear_about_us']
        know_about_alnafi = request.data['know_about_alnafi']
        full_name = request.data['full_name']
        gender = request.data['gender']
        study_field = request.data['study_field']
        email_address = request.data['email_address']
        contact_number = request.data['contact_number']
        university_name = request.data['university_name']
        level_of_education = request.data['level_of_education']
        title_of_degree = request.data['title_of_degree']
        user_status_of_PSW = request.data['user_status_of_PSW']
        student_visa_expiry = request.data['student_visa_expiry']
        skillset = request.data['skillset']
        language = request.data['language']
        nationality = request.data['nationality']
        move_another_country = request.data['move_another_eu_country']
        living_country = request.data['living_country']
        resume = request.data['resume']

        form = PSWFormRecords.objects.create(
            hear_about_us=hear_about_us,
            know_about_alnafi=know_about_alnafi,
            first_name=full_name,
            gender=gender,
            study_field=study_field,
            email=email_address,
            phone=contact_number,
            university_name=university_name,
            level_of_education=level_of_education,
            title_of_degree=title_of_degree,
            user_status_of_PSW=user_status_of_PSW,
            student_visa_expiry=student_visa_expiry,
            skillset=skillset,
            language=language,
            nationality=nationality,
            move_another_country=move_another_country,
            country=living_country,
            resume=resume
        )
        try:
            if form:
                form.save()
                return Response({"message":"Form Submitted Successfully"})
            else:
                return Response({"message":"Something went wrong"})
        except Exception as e:
            return Response({"message":"Something went wrong"})

class Marketing_Pkr_Form(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self,request):
        # print(request.data)
        inner_dict = request.data.get('{"gender": "Male", "full_name": "test leads 3", "email_address": "test3@gmail.com", "contact_number": "7539485739", "what_is_your_field_of_study": "Business and Management", "your_level_of_education": "FSc / Intermediate", "university_name": "Capital University of Science \': [\'\'], \' Technology", "university_name_other": "", "title_of_the_degree": "BSCS", "in_which_country_would_you_like_to_work": "United Arab Emirates", "n_which_domain_would_you_like_to_develop_your_skillset": "Offensive Security", "how": "18,500 PKR - 28,000 PKR", "what_languages_can_you_speak": "English", "do_you_require_financial_sponsorship": "No", "submit_your_resume_word__pdf_only": "/private/files/sample.pdf", "preferred_medium_of_communication": "Email", "do_you_know_about_al_nafi": "Yes", "how_did_you_hear_about_us": "Facebook"}', {})
        gender = request.data.get('')
        # gender = inner_dict.get('gender')
        full_name = inner_dict.get('full_name')
        email_address = inner_dict.get('email_address')
        contact_number = inner_dict.get('contact_number')
        field_of_study = inner_dict.get('what_is_your_field_of_study')
        level_of_education = inner_dict.get('your_level_of_education')
        university_name = inner_dict.get('university_name')
        university_name_other = inner_dict.get('university_name_other')
        title_of_degree = inner_dict.get('title_of_the_degree')
        move_another_country = inner_dict.get('in_which_country_would_you_like_to_work')
        skillset = inner_dict.get('in_which_domain_would_you_like_to_develop_your_skillset')
        skillset_budget = inner_dict.get('how')
        language = inner_dict.get('what_languages_can_you_speak')
        financial_sponsorship = inner_dict.get('do_you_require_financial_sponsorship')
        resume = inner_dict.get('submit_your_resume_word__pdf_only')
        communication = inner_dict.get('preferred_medium_of_communication')
        know_about_alnafi = inner_dict.get('do_you_know_about_al_nafi')
        hear_about_us = inner_dict.get('how_did_you_hear_about_us')

        # print(inner_dict)
        # print(financial_sponsorship)
        # print(know_about_alnafi)

        form = Marketing_PKR_Form.objects.create(
            gender=gender,
            full_name=full_name,
            email=email_address,
            phone = contact_number,
            study_field = field_of_study,
            level_of_education = level_of_education,
            university_name = university_name,
            # university_name_othe =
            title_of_degree = title_of_degree,
            move_another_country = move_another_country,
            skillset = skillset,
            skillset_budget = skillset_budget,
            language = language,
            financial_sponsorship = financial_sponsorship,
            resume = resume,
            communication = communication,
            know_about_alnafi = know_about_alnafi,
            hear_about_us = hear_about_us
        )
        try:
            if form:
                form.save()
                return Response({"message":"Form Submitted Successfully"})
            else:
                return Response({"message":"Something went wrong"})
        except Exception as e:
            return Response({"message":"Something went wrong"})


#Signal for mainsite user
class AlnafiUser(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        email_string = self.request.GET.get('emails', None) or None
        if email_string:
            emails = email_string.split(',')
            users = AlNafi_User.objects.filter(email__in=emails)
        else:
            users = AlNafi_User.objects.all()

        for user in users:
            # print("user.email")
            # user.save()
            # emails = ['suhaibt021@gmail.com','mirza_rehan@hotmail.com','owais.azad@annaafi.org', 'haider.ghaznavi@gmail.com','shabanas786@gmail.com','hamidashraf87@gmail.com']
            # if user.email not in emails:
            # try:
            user.save(force_update=True, force_insert=False)
            # except Exception as e:
                # print(e)

        return Response("Working")

    
    def post(self, request):
        data = request.data
        # print(data)
        email = data.get("email")
        try:
            instance = AlNafi_User.objects.filter(email=email)
            # print("in update")
            serializer = AlnafiUserSerializer(instance.first(), data=data)
        except Exception as e:
            # print(e)
            # print("in post")
            serializer = AlnafiUserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



#Signal for newsite user
class NewAlnafiUser(APIView): 
    def post(self, request):
        data = request.data
        # print(data)
        email = data.get("email")
        try:
            instance = New_AlNafi_User.objects.filter(email=email)
            # print("in update")
            serializer = NewAlnafiUserSerializer(instance.first(), data=data)
        except Exception as e:
            # print(e)
            # print("in post")
            serializer = NewAlnafiUserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#Optimized
class GetUsers(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        q = self.request.GET.get('q', None) or None
        is_converted = self.request.GET.get('is_converted', None) or None
        start_date = self.request.GET.get('start_date', None) or None
        req_end_date = self.request.GET.get('end_date', None) or None
        source = self.request.GET.get('source', None) or None
        export = self.request.GET.get('export', None) or None
        product = self.request.GET.get('product', None) or None
        phone = self.request.GET.get('phone', None)
        academy_demo_access = self.request.GET.get('academy_demo_access', None)

        users = search_users(q,start_date,req_end_date,is_converted,source,request,phone,academy_demo_access)
        if users:
            if export =='true':
                for i in range(len(users['converted_users'])):
                    users['converted_users'][i]['Converted'] = users['converted'][i]

                for info in users['products']:
                    email = info.get('user__email')
                    product_name = info.get('product__product_name')

                    for user_dict in users['converted_users']:
                        if user_dict.get('email') == email:
                            user_dict['product'] = product_name
                try:
                    file_name = f"Users_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
                    # Build the full path to the media directory
                    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                    df = pd.DataFrame(users['converted_users'])
                    df_str = df.to_csv(index=False)
                    s3 = upload_csv_to_s3(df_str,file_name)
                    data = {'file_link': file_path,'export':'true'}
                    return Response(data)
                except Exception as e:
                    return Response(e)
            else:
                email_product_map = {}
                for info in users['products']:
                    email = info.get('user__email')
                    product_name = info.get('product__product_name')
                    email_product_map[email] = product_name

                # Assign 'is_paying_customer' and 'product' to each user in 'converted_users'
                for i, user_dict in enumerate(users['converted_users']):
                    email = user_dict.get('email')
                    product_name = email_product_map.get(email)
                    is_paying_customer = users['converted'][i]  # Access the 'is_paying_customer' at the same index as 'user_dict'

                    user_dict['is_paying_customer'] = is_paying_customer
                    user_dict['product'] = product_name

                paginator = MyPagination()
                # paginated_queryset = paginator.paginate_queryset(users, request)
                paginated_queryset = paginator.paginate_queryset(users['converted_users'], request)
                return paginator.get_paginated_response(paginated_queryset)
        else:
            response_data = {
                "count": 0,
                "next": None,
                "previous": None,
                "results": []
            }
            return Response(response_data)


#Optimized
class GetActiveUsers(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        page = int(self.request.GET.get('page', 1))
        q = self.request.GET.get('q', None) or None
        is_converted = self.request.GET.get('is_converted', None) or None
        start_date = self.request.GET.get('start_date', None) or None
        req_end_date = self.request.GET.get('end_date', None) or None
        source = self.request.GET.get('source', None) or None
        export = self.request.GET.get('export', None) or None
        product = self.request.GET.get('product', None) or None
        phone = self.request.GET.get('phone', None)
        academy_demo_access = self.request.GET.get('academy_demo_access', None)
        url = request.build_absolute_uri()

        users = search_active_users(q,start_date,req_end_date,is_converted,source,request,phone,academy_demo_access,page)
        # print("users",users)
        if users['success'] == True:
            if export =='true':
                try:
                    file_name = f"Users_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
                    # Build the full path to the media directory
                    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                    df = pd.DataFrame(users['converted_users'])
                    df_str = df.to_csv(index=False)
                    s3 = upload_csv_to_s3(df_str,file_name)
                    data = {'file_link': file_path,'export':'true'}
                    return Response(data)
                except Exception as e:
                    return Response(e)
            else:
                if q:
                    num_pages = (users['count'] + 30 - 1) // 30

                    return Response({
                        'count': users['count'],
                        'num_pages': num_pages,
                        'results': users['converted_users'],
                    })
                else:
                    return Response({
                        'count': 0,
                        'num_pages': 0,
                        'results': users['converted_users'],
                    })

        else:
            return Response({
                'count': 0,
                'num_pages': 0,
                'results': users['converted_users'],
                })
            # return Response("Please enter email")


class GetUser(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        user_id = id
        url = request.build_absolute_uri()
        user = Main_User.objects.filter(id=user_id)


        try:
            payments = user[0].user_payments.filter(source__in=['Al-Nafi', 'New Alnafi']).values()
            payments = payments.order_by('-order_datetime')
        
            user = dict(user.values()[0])
            user['is_paying_customer'] = True

            def json_serializable(obj):
                if isinstance(obj, datetime):
                    return obj.isoformat()  # Convert datetime to ISO 8601 format
                raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

            products = list(payments.values('product__product_name','id'))
            plans = list(payments.values('product__product_plan'))
            payment_list = list(payments)

            for product_info in products:
                for i in range(len(payment_list)):
                    if payment_list[i]['id'] == product_info['id']:
                        if 'product_id' in payment_list[i]:
                            payment_list[i]['product_id'].append(product_info['product__product_name'])
                        else:
                            payment_list[i]['product_id'] = [product_info['product__product_name']]
                    
                    payment_list[i]['user_id'] = user['email']
                    payment_list[i]['plan'] = plans[i]['product__product_plan']
            
            payment_json = json.dumps(payment_list, default=json_serializable)  # Serialize the list to JSON with custom encoder
            payment_objects = json.loads(payment_json)


            response_data = {"user": user, "user payments": payment_objects,"no_of_payments": payments.count(),"Message":"Success"}
            return Response(response_data)
        except Exception as e:            
            user = dict(user.values()[0])
            response_data = {"user": user, "user payments": None, "no_of_payments": 0, "Message":"No payments data found"}
            return Response(response_data)


class GetNoOfUsersMonth(APIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [GroupPermission]
    # required_groups = ['Support', 'Admin']
    def get(self, request):
        source = self.request.GET.get('source', None) or None
        url = request.build_absolute_uri()
        if source == 'alnafi':
            # alnafi_no_of_users = cache.get(url)
            # if alnafi_no_of_users is None:
            users = Main_User.objects.filter(source='Al-Nafi')
            no_of_users = no_users_month(users)
                # cache.set(url, alnafi_no_of_users)
            response_data = {"alnafi_no_of_users": no_of_users}
        elif source == 'islamicacademy':
            users = Main_User.objects.filter(source='Islamic Academy')
            no_of_users = no_users_month(users)
            response_data = {"islamic_accademy_no_of_users": no_of_users}
        else:
            # alnafi_no_of_users = cache.get(url+'alnafi')
            # if alnafi_no_of_users is None:
            alnafi_users = Main_User.objects.filter(source='Al-Nafi')
            islamic_users = Main_User.objects.filter(source='Islamic Academy')
            alnafi_no_of_users = no_users_month(alnafi_users)
            islamic_no_of_users = no_users_month(islamic_users)
            total_users = alnafi_no_of_users[0]['total_users'] + islamic_no_of_users[0]['total_users']
            total_converted_users = alnafi_no_of_users[1]['converted_users'] + islamic_no_of_users[1]['converted_users']
            total_unconverted_users = alnafi_no_of_users[2]['unconverted_users'] + islamic_no_of_users[2]['unconverted_users']
                # cache.set(url+'alnafi', alnafi_no_of_users)

            response_data = {"total_users": total_users,
                            "total_converted_users": total_converted_users,
                            "total_unconverted_users": total_unconverted_users,
                            "alnafi_no_of_users": alnafi_no_of_users,
                            'islamic_no_of_users':islamic_no_of_users}

        return Response(response_data)


class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        response = Response()
        response.data = {}
        sameDomain = checkSameDomain(request)
        response.data["sameDomain"] = sameDomain
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            response = loginUser(request, response, user, sameDomain)
            groups = user.groups.all()
            serialized_data = GroupsSerailizer(groups,many=True).data
            user = UserLoginSerializer(user).data
            user['groups'] = serialized_data
            response.data["user"] = user
            return response
        else:
            # return(response.text)
            # return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'error': 'Email or Password is not Valid'}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def User_logout(request):

    request.user.auth_token.delete()

    logout(request)

    return Response('User Logged out successfully')


class Navbar(APIView):
    def get(self,request):
        user = request.user
        groups = user.groups.all()
        tabs = NavbarLink.objects.filter(group__in=groups).distinct()
        serializer = NavbarSerializer(tabs, many=True)
        return Response(serializer.data)


class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        response = Response()
        response.data = {}
        serializer = UserProfileSerializer(request.user)
        response.data["user"] = serializer.data
        return response
        # return Response(serializer.data, status=status.HTTP_200_OK)


def processAccessToken(response: Response, refresh_token, sameDomain):
    try:
        cookie = jwt.decode(
            refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
        access = AccessToken()
        access.set_exp(from_time=aware_utcnow())
        no_copy_claims = (
            settings.SIMPLE_JWT["TOKEN_TYPE_CLAIM"],
            "exp",
            settings.SIMPLE_JWT["JTI_CLAIM"],
            "jti",
        )
        no_copy = no_copy_claims
        for claim, value in cookie.items():
            if claim in no_copy:
                continue
            access[claim] = value
        response.data["message"] = "Token refreshed successfully"
        if sameDomain:
            response = set_auth_token(
                response, settings.SIMPLE_JWT['AUTH_COOKIE'], access)
        else:
            response.data[settings.SIMPLE_JWT['AUTH_COOKIE']] = str(access)
        return response
    except ExpiredSignatureError:
        return Response({"message": "Token has been expired"}, status=403)


class TokenRefreshView(APIView):
    def post(self, request: Request):
        sameDomain = checkSameDomain(request)
        response = Response()
        response.data = {}
        response.data["sameDomain"] = sameDomain

        if sameDomain:
            if(settings.SIMPLE_JWT['REFRESH_COOKIE'] in request.COOKIES):
                refresh_token = request.COOKIES[settings.SIMPLE_JWT['REFRESH_COOKIE']]
                response = processAccessToken(
                    response, refresh_token, sameDomain)
            else:
                response = Response(
                    {"message": "User is not logged in same domain"}, status=403)
        else:
            if "refresh_token" in request.data:
                refresh_token = request.data["refresh_token"]
                response = processAccessToken(
                    response, refresh_token, sameDomain)
            else:
                response = Response(
                    {"message": "User is not logged in different domain"}, status=403)
        return response


class UserPasswordCheckTokenAPI(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        id = smart_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        sameDomain = None
        try:
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                response = Response({'success': True, "message": "Credential is valid",
                                    'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
                response = loginUser(request, response, user, sameDomain)
                response.data["user"] = user.email
                return response

        except DjangoUnicodeDecodeError as e:
            return Response({'error': 'Token is not valid, remove your password'})

class SendPasswordResetEmailView(APIView):
    def post(self, request, format=None):
        try:
            user = User.objects.filter(email=request.data.get("email")).first()

            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            site_domain = 'http://localhost:3000/reset-password/' if settings.DEBUG else env('RESET_PASSWORD_URL')
            absUrl = site_domain + "?uuid=" + uidb64 + "&token=" + token

            email_body = f"<h2>Hi {user.name},</h2><p>Please verify your email by clicking the link below, to reset your password. If you haven't requested to change your password you can ignore this email.<p><a href='{absUrl}'>Reset Password</a>"
            text_content = strip_tags(email_body)

            msg = EmailMultiAlternatives("Reset Your Password", text_content, env('MAIL_FROM_ADDRESS'), [user.email])
            msg.attach_alternative(email_body, "text/html")
            msg.send()

            return Response({'success': "We have sent you a link to reset your password"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'success': False, 'message': "Email not found"}, status=status.HTTP_404_NOT_FOUND)
        
class UserSetNewPasswordAPIView(APIView):
    def post(self, request):
        try:
            id = smart_str(urlsafe_base64_decode(request.data["uuid"]))
            user = User.objects.get(id=id)
            
            new_password = request.data.get("password")
            confirm_password = request.data.get("confirm_password")
            reset_token = request.data.get("token")

            if new_password != confirm_password:
                return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

            if PasswordResetTokenGenerator().check_token(user, reset_token):
                user.set_password(new_password)
                user.save()
                
                serialized_user = UserLoginSerializer(user).data
                return Response({
                    'success': True,
                    'message': 'Password reset successfully',
                    'user': serialized_user
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Token is not valid, remove your password'
                }, status=status.HTTP_400_BAD_REQUEST)
        except (DjangoUnicodeDecodeError, User.DoesNotExist) as e:
            return Response({
                'error': 'Token or user ID is not valid'
            }, status=status.HTTP_400_BAD_REQUEST)


class MainUserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        file = request.FILES['file']
        df = pd.read_csv(file)
        # print(int(df.to_dict('records')[0]['product']))

        # Replace non-finite values with NaN
        # df['product'] = pd.to_numeric(df['product'], errors='coerce')

        # Convert NaN values to None (null) instead of a default value
        # df['product'] = np.where(pd.isnull(df['product']), None, df['product'])

        serializer = MainUserCreateSerializer(data=df.to_dict('records'), many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status= 400)


class AllEmployees(APIView):
    # permission_classes = [IsAuthenticated]
    # permission_classes = [GroupPermission]
    # required_groups = ['Admin']
    def get(self, request):
        q = self.request.GET.get('q', None) or None
        url = request.build_absolute_uri()


        # employees = cache.get(url)
        if employees is None:
            employees = search_employees(q)
            # cache.set(url, employees)

        paginator = MyPagination()
        paginated_queryset = paginator.paginate_queryset(employees, request)
        return paginator.get_paginated_response(paginated_queryset)
    

class getUsser(APIView):
    def get(self,request):
        user = Moc_Leads.objects.all()
        for us in user:
            time.sleep(1)
            us.save()
        return Response(status=200)
    

class UsersDelete(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        objs = AlNafi_User.objects.all()
        objs.delete()
        return Response('deleted')
    

class IslamicUser(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        Thread(target=self.get_thread, args=(request,)).start()
        return HttpResponse("working")

    def get_thread(self, request):
        email_string = self.request.GET.get('emails', None) or None
        if email_string:
            emails = email_string.split(',')
            users = IslamicAcademy_User.objects.filter(email__in=emails)
        else:
            users = IslamicAcademy_User.objects.all()

        for user in users:
            # print(user)
            user.save()


class Moc_leads_upload(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        csv_file = request.FILES['file']
        decoded_file = csv_file.read().decode('utf-8')
        csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')

        for row in csv_data:
            _, created = Moc_Leads.objects.update_or_create(
                email=row[3],
                defaults={
                    "username": row[0],
                    "first_name": row[1],
                    "last_name": row[2],
                    "phone": row[4],
                    "address": row[5],
                    "country": row[6],
                    "language": row[7],
                    "verification_code": row[8],
                    "isAffiliate": row[9].lower() == 'true',
                    "how_did_you_hear_about_us": row[10],
                    "affiliate_code": row[11],
                    "isMentor": row[12].lower() == 'true',
                    "login_source": row[14],
                    "erp_lead_id": row[15],
                }
            )

        response_dict = {'status': status.HTTP_201_CREATED, 'message': 'leads created'}
        return Response(response_dict)


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except Exception as _:
            # print(_)
            return Response({"Invalid": "user with this username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.instance
        response = Response({"message": "User created successfully"})
        sameDomain = checkSameDomain(request)
        response = loginUser(request, response, user, sameDomain)
        response.data["sameDomain"] = sameDomain
        response.data["user"] = serializer.data
        return response
    

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        

class CvFormsApi(APIView):
    def post(self, request, format=None):
        data = request.data

        cv_form = CvForms(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            nationality=data.get('nationality'),
            cnic_no=data.get('cnic_no'),
            gender=data.get('gender'),
            martial_status=data.get('martial_status'),
            city=data.get('city'),
            province=data.get('province'),
            zip_code=data.get('zip_code'),
            phone_number_1=data.get('phone_number_1'),
            phone_number_2=data.get('phone_number_2'),
            updated_resume=request.FILES.get('updated_resume'),
            your_picture=request.FILES.get('your_picture'),
            job=data.get('job'),
            qualification=data.get('qualification'),
            certificate=data.get('certificate'),
            work_history=data.get('work_history'),
            skills=data.get('skills'),
            refrences=data.get('refrences')
        )
        cv_form.save()

        return Response({'message': 'CvForms created successfully'}, status=status.HTTP_201_CREATED)


class GetDataCV(APIView):
    def get(self, request, format=None):
        cv_forms = CvForms.objects.all()
        data = []
        for form in cv_forms:
            form_data = {
                'first_name': form.first_name,
                'last_name': form.last_name,
                'email': form.email,
                'nationality': form.nationality,
                'cnic_no': form.cnic_no,
                'gender': form.gender,
                'martial_status': form.martial_status,
                'city': form.city,
                'province': form.province,
                'zip_code': form.zip_code,
                'phone_number_1': form.phone_number_1,
                'phone_number_2': form.phone_number_2,
                'updated_resume': form.updated_resume.url,
                'your_picture': form.your_picture.url,
                'job': form.job,
                'qualification': form.qualification,
                'certificate': form.certificate,
                'work_history': form.work_history,
                'skills': form.skills,
                'refrences': form.refrences,
            }
            data.append(form_data)

        return Response(data)
    



from datetime import datetime, timedelta

#Export user signups of new main site
class ExportDataAPIView(APIView):
    def get(self, request):
        # Get data based on the created_at condition
        # start_time = timezone.make_aware(datetime(2024, 2, 6, 10, 0, 0))  
        # end_time = timezone.now()

        end_time = timezone.now()

        # Set start time to yesterday
        start_time = end_time - timedelta(days=1) #stop from 28 feb

        start_time = start_time.replace(hour=0, minute=0, second=0, microsecond=0)

        
        filtered_data = Main_User.objects.filter(
            created_at__range=(start_time, end_time),
        ).exclude(
            internal_source__in=["Academy Signup", "Academy"],
            source="Islamic Academy"
        ).exclude(
            email__endswith="@yopmail.com"
        ).exclude(
            email__contains="youpmail.com"
        ).values("first_name","last_name","email","phone","country","source","created_at")
        if not filtered_data:
            return Response({"msg": "No data found."})

        fieldnames = ['email', 'phone', 'country', 'source', 'created_at', 'full_name']

        # Prepare data for CSV
        with open('filtered_data.csv', 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if csvfile.tell() == 0:
                writer.writeheader()

            unique_emails = set()  # Keep track of unique emails
            for data in filtered_data:
                # Concatenate "first_name" and "last_name" into a single "full_name" field
                data['full_name'] = f"{data['first_name']} {data['last_name']}"
                del data['first_name']
                del data['last_name']
                # Ensure uniqueness for the "email" field
                if data['email'] not in unique_emails:
                    writer.writerow(data)
                    unique_emails.add(data['email'])

        return Response({"msg": "done"})

class GetAuthDataLead(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        email_filter = request.GET.get('q', '')
        source_filter = request.GET.get('source', '')
        export = request.GET.get('export', '')
        page_number = request.GET.get('page', '')
        campaign = request.GET.get('campaign', '')
        # url = "http://127.0.0.1:8000/api/v1.0/all-forms/get_leaddata/"
        # url = env('AUTH_SERVICE_LEAD_DATA')
        url = f"{env('AUTH_SERVICE_LEAD_DATA')}?email={email_filter}&source={source_filter}&campaign={campaign}&export={export}&page={page_number}"
        # url=f'http://127.0.0.1:8000/api/v1.0/all-forms/get_leaddata/?email={email_filter}&source={source_filter}&campaign={campaign}&export={export}&page={page_number}'
        response = requests.get(url)
        json_data = response.json()
        # print(json_data)
        return Response(json_data)
       

from threading import Thread
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import logout
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
import jwt
from jwt.exceptions import ExpiredSignatureError
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.contrib.auth import authenticate
import os
import pandas as pd
from datetime import datetime

from .models import AlNafi_User, IslamicAcademy_User, Main_User, NavbarLink,PSWFormRecords, Marketing_PKR_Form, Moc_Leads, New_AlNafi_User
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
from user.models import Moc_Leads
import pandas as pd

class UploadMocLeads(APIView):
    def post(self,request):
        # Read the CSV file into a DataFrame
        data = pd.read_csv('/home/faizan/albaseer/Al-Baseer-Backend/user/MOC Leads - Al Baseer to CRM - Facebook.csv')
        lst = []

        # Iterate over rows in the DataFrame
        for index, row in data.iterrows():
            # Extracting data from the row
            full_name = row['full_name']
            email = row['email']
            phone = row['phone']
            form = row['form']
            country = row['country']
            login_source = row['source']
            created_at_str = row['created_at']    
            advert = row['advert']      

            # Assuming the original format is "%m/%d/%Y %H:%M:%S"
            # You can adjust the format string as needed
            # created_at = pd.to_datetime(created_at_str, format="%d/%m/%Y %H:%M:%S")
            created_at = pd.to_datetime(created_at_str, format="%Y/%m/%d %H:%M:%S")
            # try:
            #     print(email)
            #     moc = Moc_Leads.objects.create(
            #         full_name=full_name,
            #         email=email,
            #         phone=phone,
            #         form=form,
            #         country= country,
            #         source=source,
            #         created_at=created_at,
            #         cv_link=cv_link
            #     )
            # except Exception as e:
            #     print(e)
            #     lst.append(row['email'])
            try:
                # Try to get or create an Moc_Leads object based on the email
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

                # If the object was not created (i.e., it already existed), update its attributes
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

            except Exception as e:
                # If an error occurs, add the email to the list for further analysis
                print(e)
                lst.append(row['email'])

        # Create a DataFrame from the list of emails with errors
        data_Frame = pd.DataFrame(lst)
        data_Frame.to_csv("error.csv")

        return Response({"msg":"done"})


class o_level_leads_alnafi_model(APIView):
    def post(self,request):
        data = pd.read_csv('/home/faizan/albaseer/Al-Baseer-Backend/user/MOC Leads - Al Baseer to CRM - O Levels.csv')
        lst = []

        for index, row in data.iterrows():
            full_name = row['full_name']
            email = row['email']
            phone = row['phone']
            form = row['form']
            login_source = row['source']
            country = row['country']
            created_at_str = row['created_at']
            assigned_date = row['assigned_date']

            assigned_date = datetime.strptime(assigned_date, '%d %b %Y')
            formatted_date = assigned_date.strftime('%Y-%m-%d')

            # You can adjust the format string as needed
            # created_at = pd.to_datetime(created_at_str, format="%m/%d/%Y %H:%M:%S")
            created_at = pd.to_datetime(created_at_str, format="%Y/%m/%d %H:%M:%S")
            try:
                user, created = AlNafi_User.objects.get_or_create(email=email, defaults={
                    'first_name': full_name,
                    'phone': phone,
                    'email': email,
                    'form': form,
                    'login_source':login_source,
                    'country': country,
                    'created_at': created_at,
                    'assigned_date':formatted_date
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
                    user.assigned_date = assigned_date
                    user.save()

            except Exception as e:
                print(e)
                lst.append(row['email'])

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
        url = request.build_absolute_uri()

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
        # email = self.request.GET.get('email', None) or None
        # export = self.request.GET.get('export', None) or None
        url = request.build_absolute_uri()
        # print("id",id)
        user = Main_User.objects.filter(id=user_id)
        # print("user",user)
        try:
            payments = user[0].user_payments.all().values()
            # print(payments)
            payments = payments.order_by('-order_datetime')
            # latest_payment = payments.order_by('-order_datetime')[0]['expiration_datetime']
            # latest_payment = payments.order_by('-order_datetime')
            # print(latest_payment[0])
            # print(user)
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


class UserChangePasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)


class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset link send. Please check your Email'}, status=status.HTTP_200_OK)


class UserPasswordResetView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format=None):
        serializer = UserPasswordResetSerializer(data=request.data, context={'uid':uid, 'token':token})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Reset Successfully'}, status=status.HTTP_200_OK)




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


# import os
# import csv
# from users.models import User
# import pandas as pd





# class CleanLeadData(APIView):
#     def get(self, request):
#         data = pd.read_csv('/home/faizan/Main-Site-API/users/Haider Bahi Leads - Lead.csv.csv')

#         academy_csv_filename = "academy.csv"
#         alnafi_csv_filename = "alnafi.csv"
#         users_not_found_in_mainsite = "users_not_found_in_mainsite.csv"
#         with open(academy_csv_filename, 'w', newline='') as output_file:
#             writer = csv.writer(output_file)
#             writer.writerow(['Status', 'Email','Source','First Name', 'Middle Name', 'Last Name', 'Date Joined', 'Submit Your Question If Any', 'Full Name', 'Job Title',
#                               'Gender', 'Interest', 'Qualification', 'Form', 'How Did You Hear About Us', 
#                               'Product Names List', 'Plan', 'Languages', 'Converted Date', 'Lead Type', 'Product Name', 'CV Link', 'Demo Product', 'Enrollment',
#                                 'From Customer', 'Website', 'Mobile No', 'WhatsApp', 'Request Type', 'Country', 'Phone', 'First Renewal', 
#                                 'Second Renewal', 'Third Renewal', 'Fourth Renewal', 'Fifth Renewal', 'Sixth Renewal', 'Seventh Renewal', 'Eighth Renewal', 
#                              'Ninth Renewal', 'Tenth Renewal', 'Eleventh Renewal', 'Twelth Renewal', 'First Proof', 'Second Proof', 'Third Proof', 
#                              'Fourth Proof', 'Fifth Proof', 'Sixth Proof', 'Seventh Proof', 'Eighth Proof', 'Ninth Proof', 'Tenth Proof', 
#                              'Eleventh Proof', 'Twelth Proof', 'Salutation', 'Organization Name', 'No of Employees', 'Annual Revenue', 'Industry', 
#                              'Market Segment', 'Territory', 'Fax', 'City', 'State', 'Qualification Status', 'Qualified By', 'Qualified on', 
#                              'Campaign Name', 'Company', 'Print Language', 'Image', 'Title', 'Disabled', 'Unsubscribed', 'Blog Subscriber', 
#                              'ID (Notes)', 'Note (Notes)', 'Added By (Notes)', 'Added On (Notes)'])

#         with open(alnafi_csv_filename, 'w', newline='') as output_file:
#             writer = csv.writer(output_file)
#             writer.writerow(['Status', 'Email', 'Source','First Name', 'Middle Name', 'Last Name', 'Date Joined', 'Submit Your Question If Any', 'Full Name', 'Job Title',
#                              'Gender', 'Interest', 'Qualification','Form', 'How Did You Hear About Us', 
#                             'Product Names List', 'Plan', 'Languages', 'Converted Date', 'Lead Type', 'Product Name', 'CV Link', 'Demo Product', 'Enrollment',
#                             'From Customer', 'Website', 'Mobile No', 'WhatsApp', 'Request Type', 'Country', 'Phone', 'First Renewal', 
#                             'Second Renewal', 'Third Renewal', 'Fourth Renewal', 'Fifth Renewal', 'Sixth Renewal', 'Seventh Renewal', 'Eighth Renewal', 
#                              'Ninth Renewal', 'Tenth Renewal', 'Eleventh Renewal', 'Twelth Renewal', 'First Proof', 'Second Proof', 'Third Proof', 
#                              'Fourth Proof', 'Fifth Proof', 'Sixth Proof', 'Seventh Proof', 'Eighth Proof', 'Ninth Proof', 'Tenth Proof', 
#                              'Eleventh Proof', 'Twelth Proof', 'Salutation', 'Organization Name', 'No of Employees', 'Annual Revenue', 'Industry', 
#                              'Market Segment', 'Territory', 'Fax', 'City', 'State', 'Qualification Status', 'Qualified By', 'Qualified on', 
#                              'Campaign Name', 'Company', 'Print Language', 'Image', 'Title', 'Disabled', 'Unsubscribed', 'Blog Subscriber', 
#                              'ID (Notes)', 'Note (Notes)', 'Added By (Notes)', 'Added On (Notes)'])
        
#         with open(users_not_found_in_mainsite, 'w', newline='') as output_file:
#             writer = csv.writer(output_file)
#             writer.writerow(['Status', 'Email', 'Source','First Name', 'Middle Name', 'Last Name', 'Date Joined', 'Submit Your Question If Any', 'Full Name', 'Job Title',
#                              'Gender', 'Interest', 'Qualification','Form', 'How Did You Hear About Us', 
#                             'Product Names List', 'Plan', 'Languages', 'Converted Date', 'Lead Type', 'Product Name', 'CV Link', 'Demo Product', 'Enrollment',
#                             'From Customer', 'Website', 'Mobile No', 'WhatsApp', 'Request Type', 'Country', 'Phone', 'First Renewal', 
#                             'Second Renewal', 'Third Renewal', 'Fourth Renewal', 'Fifth Renewal', 'Sixth Renewal', 'Seventh Renewal', 'Eighth Renewal', 
#                              'Ninth Renewal', 'Tenth Renewal', 'Eleventh Renewal', 'Twelth Renewal', 'First Proof', 'Second Proof', 'Third Proof', 
#                              'Fourth Proof', 'Fifth Proof', 'Sixth Proof', 'Seventh Proof', 'Eighth Proof', 'Ninth Proof', 'Tenth Proof', 
#                              'Eleventh Proof', 'Twelth Proof', 'Salutation', 'Organization Name', 'No of Employees', 'Annual Revenue', 'Industry', 
#                              'Market Segment', 'Territory', 'Fax', 'City', 'State', 'Qualification Status', 'Qualified By', 'Qualified on', 
#                              'Campaign Name', 'Company', 'Print Language', 'Image', 'Title', 'Disabled', 'Unsubscribed', 'Blog Subscriber', 
#                              'ID (Notes)', 'Note (Notes)', 'Added By (Notes)', 'Added On (Notes)'])

#         for index, row in data.iterrows():
#             status=row['Status']
#             email=row['Email']
#             source=row['Source']
#             first_name=row['First Name']
#             middle_name=row['Middle Name']
#             last_name=row['Last Name']
#             date_joined=row['Date Joined']
#             question=row['Submit Your Question If Any']
#             full_name=row['Full Name']
#             job_title=row['Job Title']
#             gender=row['Gender']
#             interest=row['Interest']
#             qualification=row['Qualification']
#             form=row['Form']
#             how_heard=row['How Did You Hear About Us']
#             product_names=row['Product Names List']
#             plan=row['Plan']
#             languages=row['Languages']
#             converted_date=row['Converted Date']
#             lead_type=row['Lead Type']
#             product_name=row['Product Name']
#             cv_link=row['CV Link']
#             demo_product=row['Demo Product']
#             enrollment=row['Enrollment']
#             from_customer=row['From Customer']
#             website=row['Website']
#             mobile_no=row['Mobile No']
#             whatsapp=row['WhatsApp']
#             request_type=row['Request Type']
#             country=row['Country']
#             phone=row['Phone']
#             first_renewal=row['First Renewal']
#             second_renewal=row['Second Renewal']
#             third_renewal=row['Third Renewal']
#             fourth_renewal=row['Fourth Renewal']
#             fifth_renewal=row['Fifth Renewal']
#             sixth_renewal=row['Sixth Renewal']
#             seventh_renewal=row['Seventh Renewal']
#             eighth_renewal=row['Eighth Renewal']
#             ninth_renewal=row['Ninth Renewal']
#             tenth_renewal=row['Tenth Renewal']
#             eleventh_renewal=row['Eleventh Renewal']
#             twelfth_renewal=row['Twelth Renewal']
#             first_proof=row['First Proof']
#             second_proof=row['Second Proof']
#             third_proof=row['Third Proof']
#             fourth_proof=row['Fourth Proof']
#             fifth_proof=row['Fifth Proof']
#             sixth_proof=row['Sixth Proof']
#             seventh_proof=row['Seventh Proof']
#             eighth_proof=row['Eighth Proof']
#             ninth_proof=row['Ninth Proof']
#             tenth_proof=row['Tenth Proof']
#             eleventh_proof=row['Eleventh Proof']
#             twelfth_proof=row['Twelth Proof']
#             salutation=row['Salutation']
#             organization_name=row['Organization Name']
#             num_employees=row['No of Employees']
#             annual_revenue=row['Annual Revenue']
#             industry=row['Industry']
#             market_segment=row['Market Segment']
#             territory=row['Territory']
#             fax=row['Fax']
#             city=row['City']
#             state=row['State']
#             qualification_status=row['Qualification Status']
#             qualified_by=row['Qualified By']
#             qualified_on=row['Qualified on']
#             campaign_name=row['Campaign Name']
#             company=row['Company']
#             print_language=row['Print Language']
#             image=row['Image']
#             title=row['Title']
#             disabled=row['Disabled']
#             unsubscribed=row['Unsubscribed']
#             blog_subscriber=row['Blog Subscriber']
#             id_notes=row['ID (Notes)']
#             notes=row['Note (Notes)']
#             added_by_notes=row['Added By (Notes)']
#             added_on_notes=row['Added On (Notes)']



#             # Get the matching User object
#             user = self.get_user_by_email(email)
#             i = 1
#             if user:
#                 # Process the user as needed, e.g., print or save to a new CSV
#                 print(f"user {i}")
#                 i+=1
#                 # print(f"User: {user.username}, Source: {user.login_source}")
#                 # print("row_source",source)

#                 # Create separate CSV files for each source
#                 # for source in sources:

#                 if user.login_source == 'Academy':
#                     with open(academy_csv_filename, 'a', newline='') as academy_output_file:
#                         academy_writer = csv.writer(academy_output_file)
#                         academy_writer.writerow([status,email,user.login_source,first_name,middle_name,last_name,date_joined,question,full_name,
#                                                  job_title,gender,interest,qualification,form,how_heard,product_names,plan,languages,converted_date,
#                                                  lead_type,product_name,cv_link,demo_product,enrollment,from_customer,website,mobile_no,whatsapp,
#                                                  request_type,country,phone,first_renewal,second_renewal,third_renewal,fourth_renewal,fifth_renewal,
#                                                  sixth_renewal,seventh_renewal,eighth_renewal,ninth_renewal,tenth_renewal,eleventh_renewal,
#                                                  twelfth_renewal,first_proof,second_proof,third_proof,fourth_proof,fifth_proof,sixth_proof,
#                                                  seventh_proof,eighth_proof,ninth_proof,tenth_proof,eleventh_proof,twelfth_proof,salutation,
#                                                  organization_name,num_employees,annual_revenue,industry,market_segment,territory,fax,city,state,
#                                                  qualification_status,qualified_by,qualified_on,campaign_name,company,print_language,image,title,
#                                                  disabled,unsubscribed,blog_subscriber,id_notes,notes,added_by_notes,added_on_notes])
                        
#                 elif user.login_source == 'Al Nafi':
#                     with open(alnafi_csv_filename, 'a', newline='') as alnafi_output_file:
#                         alnafi_writer = csv.writer(alnafi_output_file)
#                         alnafi_writer.writerow([status,email,user.login_source,
#                                                 first_name,
#                                                 middle_name,
#                                                 last_name,
#                                                 date_joined,
#                                                 question,
#                                                 full_name,
#                                                 job_title,
#                                                 gender,
#                                                 interest,qualification,form,how_heard,product_names,plan,languages,converted_date,lead_type,
#                                                 product_name,cv_link,demo_product,enrollment,from_customer,website,mobile_no,whatsapp,request_type,
#                                                 country,phone,first_renewal,second_renewal,third_renewal,fourth_renewal,fifth_renewal,sixth_renewal,
#                                                 seventh_renewal,eighth_renewal,ninth_renewal,tenth_renewal,eleventh_renewal,twelfth_renewal,first_proof,
#                                                 second_proof,third_proof,fourth_proof,fifth_proof,sixth_proof,seventh_proof,eighth_proof,ninth_proof,
#                                                 tenth_proof,eleventh_proof,twelfth_proof,salutation,organization_name,num_employees,annual_revenue,
#                                                 industry,market_segment,territory,fax,city,state,qualification_status,qualified_by,qualified_on,
#                                                 campaign_name,company,print_language,image,title,disabled,unsubscribed,blog_subscriber,id_notes,
#                                                 notes,added_by_notes,added_on_notes])

#             else:
#                 with open(users_not_found_in_mainsite, 'a', newline='') as alnafi_output_file:
#                     alnafi_writer = csv.writer(alnafi_output_file)
#                     alnafi_writer.writerow([status,email,source,
#                                             first_name,
#                                             middle_name,
#                                             last_name,
#                                             date_joined,
#                                             question,
#                                             full_name,
#                                             job_title,
#                                             gender,
#                                             interest,qualification,form,how_heard,product_names,plan,languages,converted_date,lead_type,
#                                             product_name,cv_link,demo_product,enrollment,from_customer,website,mobile_no,whatsapp,request_type,
#                                             country,phone,first_renewal,second_renewal,third_renewal,fourth_renewal,fifth_renewal,sixth_renewal,
#                                             seventh_renewal,eighth_renewal,ninth_renewal,tenth_renewal,eleventh_renewal,twelfth_renewal,first_proof,
#                                             second_proof,third_proof,fourth_proof,fifth_proof,sixth_proof,seventh_proof,eighth_proof,ninth_proof,
#                                             tenth_proof,eleventh_proof,twelfth_proof,salutation,organization_name,num_employees,annual_revenue,
#                                             industry,market_segment,territory,fax,city,state,qualification_status,qualified_by,qualified_on,
#                                             campaign_name,company,print_language,image,title,disabled,unsubscribed,blog_subscriber,id_notes,
#                                             notes,added_by_notes,added_on_notes])



#         return Response("vdfvid")

#     def get_user_by_email(self, email):
#         try:
#             return User.objects.get(email=email)
#         except User.DoesNotExist:
#             print(f"{email} not found")
#             return None
        








from threading import Thread
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth import logout
from rest_framework import status
from payment.models import Main_Payment
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
import jwt
from jwt.exceptions import ExpiredSignatureError
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser, Group
from django.contrib.auth import authenticate
import os
import pandas as pd
from datetime import datetime, timedelta, date

from .models import AlNafi_User, IslamicAcademy_User, Main_User,User, NavbarLink,PSWFormRecords, Marketing_PKR_Form, Moc_Leads, New_AlNafi_User
from .serializers import (AlnafiUserSerializer, IslamicAcademyUserSerializer, UserRegistrationSerializer,
UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,SendPasswordResetEmailSerializer,
UserPasswordResetSerializer,NavbarSerializer,GroupsSerailizer,UsersCombinedSerializer, MainUserSerializer,MainUserCreateSerializer)
from .services import (set_auth_token, checkSameDomain, GroupPermission,
loginUser,get_tokens_for_user,aware_utcnow,no_users_month,upload_csv_to_s3,search_users,search_employees)
from .renderers import UserRenderer
from itertools import chain
from functools import reduce
import numpy as np
import json
import environ
from django.http import HttpResponse
from user.constants import COUNTRY_CODES
import requests
import csv
from rest_framework.parsers import MultiPartParser, FormParser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


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


class UsersDelete(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        objs = AlNafi_User.objects.all()
        objs.delete()
        return Response('deleted')

#Signal for mainsite user
class AlnafiUser(APIView):
    # def get(self, request):
    #     Thread(target=self.get_thread, args=(request,)).start()
    #     return HttpResponse("working")
    permission_classes = [IsAuthenticated]
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

#Optimized
class GetUsers(APIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [GroupPermission]
    # required_groups = ['Support', 'Admin','MOC']
    def get(self, request):
        q = self.request.GET.get('q', None) or None
        is_converted = self.request.GET.get('is_converted', None) or None
        start_date = self.request.GET.get('start_date', None) or None
        req_end_date = self.request.GET.get('end_date', None) or None
        source = self.request.GET.get('source', None) or None
        export = self.request.GET.get('export', None) or None
        product = self.request.GET.get('product', None) or None
        url = request.build_absolute_uri()

        users = search_users(q,start_date,req_end_date,is_converted,source)
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

class GetUser(APIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [GroupPermission]
    # required_groups = ['Support', 'Admin', 'MOC']
    def get(self, request, id):
        user_id = id
        # email = self.request.GET.get('email', None) or None
        # export = self.request.GET.get('export', None) or None
        url = request.build_absolute_uri()
        # user = cache.get(url)

        # if user is None:
        user = Main_User.objects.filter(id=user_id)
            # cache.set(url, user)
        try:
            payments = user[0].user_payments.all().values()
            payments = payments.exclude(expiration_datetime__isnull=True).order_by('-order_datetime')
            latest_payment = payments.order_by('-order_datetime')[0]['expiration_datetime']
            user = dict(user.values()[0])

            # if latest_payment.date() > date.today():
            user['is_paying_customer'] = True

            def json_serializable(obj):
                if isinstance(obj, datetime):
                    return obj.isoformat()  # Convert datetime to ISO 8601 format
                raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

            products = list(payments.values('product__product_name'))
            payment_list = list(payments)
            for i in range(len(payment_list)):
                try:
                    payment_list[i]['user_id'] = user['email']
                    payment_list[i]['product_id'] = products[i]['product__product_name']
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


class Navbar(APIView):
    def get(self,request):
        user = request.user
        groups = user.groups.all()
        tabs = NavbarLink.objects.filter(group__in=groups).distinct()
        serializer = NavbarSerializer(tabs, many=True)
        return Response(serializer.data)




class AllEmployees(APIView):
    # permission_classes = [IsAuthenticated]
    # permission_classes = [GroupPermission]
    # required_groups = ['Admin']
    def get(self, request):
        q = self.request.GET.get('q', None) or None
        url = request.build_absolute_uri()


        employees = cache.get(url)
        if employees is None:
            employees = search_employees(q)
            cache.set(url, employees)

        paginator = MyPagination()
        paginated_queryset = paginator.paginate_queryset(employees, request)
        return paginator.get_paginated_response(paginated_queryset)
    
class NewAlnafiUser(APIView):

    def post(self, request):
        email = request.data.get('email')
        student_email = request.data.get('student_email')
        student_email_id = request.data.get('student_email_id')
        verified= request.data.get('verified')
        blocked= request.data.get('blocked')
        created_at= request.data.get('created_at')
        phone = request.data.get('phone')
        meta_data = request.data.get('meta_data')
        facebook_user_id = request.data.get('facebook_user_id')
        google_user_id = request.data.get('google_user_id')
        provider = request.data.get('provider')
        affiliate_code = request.data.get('affiliate_code')
        source = request.data.get('source')
        easypaisa_number = request.data.get('easypaisa_number')
        created_at = request.data.get('created_at')
        user = New_AlNafi_User.objects.create(
            email=email,
            student_email=student_email,
            student_email_status=student_email_id,
            verified=verified,
            blocked=blocked,
            created_at=created_at,
            phone=phone,
            meta_data=meta_data,
            facebook_user_id=facebook_user_id,
            google_user_id=google_user_id,
            provider=provider,
            affiliate_code=affiliate_code,
            source=source,
            easypaisa_number=easypaisa_number
        )
        try:
            # Save the new user instance to the database
            user.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# env = environ.Env()
# env.read_env()
# DEBUG = env('DEBUG',cast=bool)
# import guacamole


# class Guacamoli(APIView):
#     def get(self, request):
#         url = env('GUACAMOLE_SERVER_URL')
#         source = env('GUACAMOLE_DATA_SOURCE')
#         username = env('GUACAMOLE_USERNAME')
#         password = env('GUACAMOLE_PASSWORD')



#         session = guacamole.session("https://lab.alnafi.com/","postgresql","nafisuperadminlabsalnafi", "IO*91^%82**/>,.;'=_-|||")
#         print(session.get_user("appinventorpak1@gmail.com"))
#         return Response("vbdisvu")

# class UserLogoutView(APIView):
#     authentication_classes = [JWTAuthentication]

#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh_token"]
#             token = RefreshToken(refresh_token)
#             user = request.user
#             print(user)
#             if not isinstance(user, AnonymousUser):
#                 user.outstanding_token_set.add(token)
#             return Response({"message": "Logout successful"}, status=200)
#         except Exception as e:
#             return Response({"error": str(e)}, status=400)



# class GetNoOfUsers(APIView):
#     # permission_classes = [IsAuthenticated]
#     # permission_classes = [GroupPermission]
#     # required_groups = ['Support', 'Admin']
#     def get(self, request):
#         start_date = self.request.GET.get('start_date', None) or None
#         end_date = self.request.GET.get('end_date', None) or None
#         source = self.request.GET.get('source', None) or None
#         url = request.build_absolute_uri()


#         # users = no_of_users(start_date,end_date,source)
#         # response_data = {"no_of_users": users}
#         # return Response(response_data)
#         if source == 'alnafiuser':
#             alnafi_no_of_users = cache.get(url)
#             if alnafi_no_of_users is None:
#                 alnafi_no_of_users = alnafi_no_users(start_date, end_date)
#                 cache.set(url, alnafi_no_of_users)
#             response_data = {"alnafi_no_of_users": alnafi_no_of_users}
#         elif source == 'islamicacademyuser':
#             academy_no_of_users = cache.get(url)
#             if academy_no_of_users is None:
#                 academy_no_of_users = islamic_no_users(start_date,end_date)
#                 cache.set(url, academy_no_of_users)
#             response_data = {"academy_no_of_users": academy_no_of_users,}
#         else:
#             alnafi_no_of_users = cache.get(url+'alnafi')
#             if alnafi_no_of_users is None:
#                 alnafi_no_of_users = alnafi_no_users(start_date, end_date)
#                 cache.set(url+'alnafi', alnafi_no_of_users)

#             academy_no_of_users = cache.get(url+'academy')
#             if academy_no_of_users is None:
#                 academy_no_of_users = islamic_no_users(start_date,end_date)
#                 cache.set(url+'academy', academy_no_of_users)

#             response_data = {"alnafi_no_of_users": alnafi_no_of_users,
#                             "academy_no_of_users": academy_no_of_users}

#         return Response(response_data)


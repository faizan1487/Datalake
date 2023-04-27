from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth import logout
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
import jwt
from jwt.exceptions import ExpiredSignatureError
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
import os
import pandas as pd
from datetime import datetime, timedelta, date

from .models import AlNafi_User, IslamicAcademy_User,User, NavbarLink
from .serializers import (AlnafiUserSerializer, IslamicAcademyUserSerializer, UserRegistrationSerializer,
UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,SendPasswordResetEmailSerializer,
UserPasswordResetSerializer,NavbarSerializer,GroupsSerailizer,UsersCombinedSerializer)
from .services import (alnafi_user, islamic_user, set_auth_token, checkSameDomain, GroupPermission,
loginUser,get_tokens_for_user,aware_utcnow,alnafi_no_users,islamic_no_users,upload_csv_to_s3)
from .renderers import UserRenderer
from itertools import chain
from django.core.cache import cache



# Create your views here.
class MyPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100

class UsersDelete(APIView):
    def get(self, request):
        objs = AlNafi_User.objects.all()
        objs.delete()
        return Response('deleted')

class AlnafiUser(APIView):
    def post(self, request):
        data = request.data
        serializer = AlnafiUserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserDetails(APIView):
    # permission_classes = [IsAuthenticated]
    # permission_classes = [GroupPermission]
    required_group = 'Support'
    def get(self, request):
        q = self.request.GET.get('q', None) or None
        is_converted = self.request.GET.get('is_converted', None) or None
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        source = self.request.GET.get('source', None) or None
        export = self.request.GET.get('export', None) or None
        url = request.build_absolute_uri()
        if source == 'alnafiuser':
            obj = cache.get(url)
            if obj is None:
                obj = alnafi_user(q, start_date, end_date, is_converted)
                cache.set(url, obj) 
            serializer = AlnafiUserSerializer(obj['converted_users'], many=True)
            if export =='True':
                try:
                    serializer = AlnafiUserSerializer(obj['converted_users'], many=True)
                    file_name = f"Alanfi_Users_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
                    # Build the full path to the media directory
                    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                    df = pd.DataFrame(serializer.data)
                    df_str = df.to_csv(index=False)
                    s3 = upload_csv_to_s3(df_str,file_name)
                    data = {'file_link': file_path}
                    return Response(data)
                except Exception as e:
                    return Response(e)
            else:
                for i in range(len(serializer.data)):
                    serializer.data[i]['is_paying_customer'] = obj['converted'][i]
                paginator = MyPagination()
                paginated_queryset = paginator.paginate_queryset(serializer.data, request)
                return paginator.get_paginated_response(paginated_queryset)
        elif source =='islamicacademyuser':
            obj = cache.get(url)
            if obj is None:
                obj = islamic_user(q, start_date, end_date, is_converted)
                cache.set(url, obj) 
            if export =='True':
                try:
                    serializer = IslamicAcademyUserSerializer(obj, many=True)
                    file_name = f"Islamic_Academy_Users_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
                    # Build the full path to the media directory
                    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                    df = pd.DataFrame(serializer.data).to_csv(index=False)
                    s3 = upload_csv_to_s3(df,file_name)
                    data = {'file_link': file_path}
                    return Response(data)
                except Exception as e:
                    return Response(e)
            else:
                paginator = MyPagination()
                paginated_queryset = paginator.paginate_queryset(obj, request)
                serializer = IslamicAcademyUserSerializer(paginated_queryset,many=True)
                return paginator.get_paginated_response(serializer.data)
        else:
            alnafi_obj = cache.get(url+'alnafi')
            islamic_obj = cache.get(url+'islamic')
            
            if alnafi_obj is None:
                alnafi_obj = alnafi_user(q, start_date, end_date, is_converted)
                cache.set(url+'alnafi', alnafi_obj)
                
            if islamic_obj is None: 
                islamic_obj = islamic_user(q, start_date, end_date,is_converted)
                cache.set(url+'islamic', islamic_obj)
            
            if export == 'True':
                alnafi_serializer = AlnafiUserSerializer(alnafi_obj, many=True)
                islamic_serializer = IslamicAcademyUserSerializer(islamic_obj, many=True)
                df1 = pd.DataFrame(alnafi_serializer.data)
                df2 = pd.DataFrame(islamic_serializer.data)
                # Merge dataframes
                file_name = f"USERS_DATA_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
                merged_df = pd.concat([df1, df2], axis=1).to_csv(index=False)
                s3 = upload_csv_to_s3(merged_df,file_name)
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                data = {'file_link': file_path}
                return Response(data)
            else:   
                alnafi_serialized_data = AlnafiUserSerializer(alnafi_obj['converted_users'], many=True)
                islamic_serialized_data = IslamicAcademyUserSerializer(islamic_obj, many=True)
                combined_data = {
                    'data1': alnafi_serialized_data.data,
                    'data2': islamic_serialized_data.data,
                }
                serialized_data = UsersCombinedSerializer(combined_data).data
                for i in range(len(serialized_data['data1'])):
                    serialized_data['data1'][i]['is_paying_customer'] = alnafi_obj['converted'][i]
                combined_queryset = list(chain(serialized_data['data1'], serialized_data['data2']))
                paginator = MyPagination()
                paginated_queryset = paginator.paginate_queryset(combined_queryset, request)
                return paginator.get_paginated_response(paginated_queryset)
            
                
                
                

  
class GetNoOfUsers(APIView):
    # permission_classes = [IsAuthenticated]
    # permission_classes = [GroupPermission]
    required_group = 'Support'
    def get(self, request):
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None   
        source = self.request.GET.get('source', None) or None 
        
        if source == 'alnafiuser':
            alnafi_no_of_users = cache.get('alnafi_no_of_users')
            if alnafi_no_of_users is None:
                alnafi_no_of_users = alnafi_no_users(start_date, end_date)
                cache.set('alnafi_no_of_users', alnafi_no_of_users)
        elif source == 'islamicacademyuser':
            academy_no_of_users = cache.get('academy_no_of_users')
            if academy_no_of_users is None:
                academy_no_of_users = islamic_no_users(start_date,end_date)
                cache.set('academy_no_of_users', academy_no_of_users) 
        else:
            islamic_users = islamic_no_users(start_date, end_date)   
            alnafi_users = alnafi_no_users(start_date,end_date)
            
            alnafi_no_of_users = cache.get('alnafi_no_of_users')
            if alnafi_no_of_users is None:
                alnafi_no_of_users = alnafi_no_users(start_date, end_date)
                cache.set('alnafi_no_of_users', alnafi_no_of_users) 
                    
            academy_no_of_users = cache.get('academy_no_of_users')
            if academy_no_of_users is None:
                academy_no_of_users = islamic_no_users(start_date,end_date)
                cache.set('academy_no_of_users', academy_no_of_users) 
            
            response_data = {"academy_no_of_users": academy_no_of_users,
                             "alnafi_no_of_users": alnafi_no_of_users
                             }
        return Response(response_data)
            
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except Exception as _:
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
            # print(serialized_data)
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
        sales = Group.objects.get(name='Sales')
        support = Group.objects.get(name='Support')
        admin = Group.objects.get(name='Admin')
        sales_support = Group.objects.get(name='Sales and Support')
        support_user = User.objects.filter(groups__name=support.name, email__iexact=user.email)
        sales_user = User.objects.filter(groups__name=sales.name, email__iexact=user.email)
        admin_user = User.objects.filter(groups__name=admin.name, email__iexact=user.email)
        # if support_user and
        if admin_user:
            obj = NavbarLink.objects.all()
        elif support_user:
            obj = NavbarLink.objects.filter(group='Support')
        elif sales_user:
            obj = NavbarLink.objects.filter(group='Sales')
        elif sales_support:
            obj = NavbarLink.objects.filter(group='Sales and Support')
        serializer = NavbarSerializer(obj, many=True)
        return Response(serializer.data)
    
    
# class GetPayingUser(APIView):
#     # permission_classes = [IsAuthenticated]
#     # permission_classes = [GroupPermission]
#     required_group = 'Support'
#     def get(self, request):
#         source = self.request.GET.get('source', None) or None
#         export = self.request.GET.get('export', None) or None
#         is_converted = self.request.GET.get('ispaying', None) or None
#         exact = self.request.GET.get('exact', None) or None
#         date = self.request.GET.get('date', None) or None
#         if source == 'islamicacademyuser':
#             obj = cache.get('islamic_paying_users')
#             if obj is None:
#                 obj = islamic_Paying_user(isPaying,exact,date)
#                 cache.set('islamic_paying_users', obj) 
                
#             serializer = IslamicAcademyUserSerializer(obj, many=True)
#             if export =='True':
#                 file_name = f"Alanfi_Users_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
#                     # Build the full path to the media directory
#                 file_path = os.path.join(settings.MEDIA_ROOT, file_name)
#                 df = pd.DataFrame(serializer.data).to_csv(index=False)
#                 s3 = upload_csv_to_s3(df,file_name)
#                 data = {'file_link': file_path}
#                 return Response(data)
#             else:
#                 paginator = MyPagination()
#                 paginated_queryset = paginator.paginate_queryset(serializer.data, request)
#                 return paginator.get_paginated_response(paginated_queryset)
#         elif source =='alnafiuser':
#             obj = cache.get('alnafi_paying_users')
#             if obj is None:
#                 obj = alnafi_Paying_user(isPaying, exact, date)
#                 cache.set('alnafi_paying_user', obj)
                         
#             serializer = AlnafiUserSerializer(obj['paying_users'], many=True)
#             if export =='True':
#                 file_name = f"Alanfi_Users_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
#                     # Build the full path to the media directory
#                 file_path = os.path.join(settings.MEDIA_ROOT, file_name)
#                 df = pd.DataFrame(serializer.data).to_csv(file_path, index=False)
#                 s3 = upload_csv_to_s3(df,file_name)
#                 data = {'file_link': file_path}
#                 return Response(data)
#             else:
#                 for i in range(len(serializer.data)):
#                     serializer.data[i]['is_paying'] = obj['is_paying'][i]
#                 paginator = MyPagination()
#                 paginated_queryset = paginator.paginate_queryset(serializer.data, request)
#                 return paginator.get_paginated_response(paginated_queryset)                
#         else:
#             alnafi_users = cache.get('alnafi_paying_users')
#             islamic_users = cache.get('islamic_paying_users')
#             if alnafi_users is None:
#                 alnafi_users = alnafi_Paying_user(isPaying, exact, date)
#                 cache.set('alnafi_paying_users', alnafi_users)
                
#             if islamic_users is None:
#                 islamic_users = islamic_Paying_user(isPaying,exact,date)
#                 cache.set('islamic_paying_users', islamic_users) 
                
                
#             alnafi_users = alnafi_Paying_user(isPaying,exact,date)
#             alnafi_serialized_data = AlnafiUserSerializer(alnafi_users['paying_users'], many=True)
#             islamic_serialized_data = IslamicAcademyUserSerializer(islamic_users, many=True)
#             if export == 'True':
#                 df1 = pd.DataFrame(alnafi_serialized_data.data)
#                 df2 = pd.DataFrame(islamic_serialized_data.data)
#                 # Merge dataframes
#                 file_name = f"USERS_DATA_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
#                 file_path = os.path.join(settings.MEDIA_ROOT, file_name)
#                 merged_df = pd.concat([df1, df2], axis=1).to_csv(index=False)
#                 s3 = upload_csv_to_s3(merged_df,file_name)
#                 data = {'file_link': file_path}
#                 return Response(data)
#             else:
#                 combined_data = {
#                     'data1': alnafi_serialized_data.data,
#                     'data2': islamic_serialized_data.data,
#                 }
#                 serialized_data = UsersCombinedSerializer(combined_data).data
#                 for i in range(len(serialized_data['data1'])):
#                     serialized_data['data1'][i]['is_paying'] = alnafi_users['is_paying'][i]
#                 combined_queryset = list(chain(serialized_data['data1'], serialized_data['data2']))
#                 paginator = MyPagination()
#                 paginated_queryset = paginator.paginate_queryset(combined_queryset, request)
#                 return paginator.get_paginated_response(paginated_queryset)

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


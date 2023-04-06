from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth import logout
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import authenticate
import os
import pandas as pd
from datetime import datetime

from .models import AlNafi_User, IslamicAcademy_User
from .serializers import (AlnafiUserSerializer, IslamicAcademyUserSerializer, UserRegistrationSerializer,
UserLoginSerializer,UserProfileSerializer,UserChangePasswordSerializer,SendPasswordResetEmailSerializer,
UserPasswordResetSerializer)
from .services import alnafi_user, islamic_user, set_auth_token, checkSameDomain, loginUser,get_tokens_for_user
from .renderers import UserRenderer
# Create your views here.
class MyPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100

class AlnafiUser(APIView):
    def post(self, request):
        data = request.data
        serializer = AlnafiUserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetUserDetails(APIView):
    def get(self, request):
        q = self.request.GET.get('q', None) or None
        isPaying = self.request.GET.get('ispaying', None) or None
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        source = self.request.GET.get('source', None) or None
        export = self.request.GET.get('export', None) or None

        if source == 'alnafiuser':
            obj = alnafi_user(q, start_date, end_date, isPaying)
            if export =='true':
                serializer = AlnafiUserSerializer(obj, many=True)
                file_name = f"Alanfi_Users_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
                # Build the full path to the media directory
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                pd.DataFrame(serializer.data).to_csv(file_path, index=False)
                data = {'file_link': file_path}
                return Response(data)
            else:
                paginator = MyPagination()
                paginated_queryset = paginator.paginate_queryset(obj, request)
                serializer = AlnafiUserSerializer(paginated_queryset,many=True)
                return paginator.get_paginated_response(serializer.data)
        elif source =='islamicacademyuser':
            obj = islamic_user(q, start_date, end_date, isPaying)
            if export =='true':
                serializer = IslamicAcademyUserSerializer(obj, many=True)
                file_name = f"Islamic_Academy_Users_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
                # Build the full path to the media directory
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                pd.DataFrame(serializer.data).to_csv(file_path, index=False)
                data = {'file_link': file_path}
                return Response(data)
            else:
                paginator = MyPagination()
                paginated_queryset = paginator.paginate_queryset(obj, request)
                serializer = IslamicAcademyUserSerializer(paginated_queryset,many=True)
                return paginator.get_paginated_response(serializer.data)
        else:
            if export == 'true':
                alnafi_obj = alnafi_user(q, start_date, end_date, isPaying)
                islamic_obj = islamic_user(q, start_date, end_date,isPaying)
                alnafi_serializer = AlnafiUserSerializer(alnafi_obj, many=True)
                islamic_serializer = IslamicAcademyUserSerializer(islamic_obj, many=True)

                df1 = pd.DataFrame(alnafi_serializer.data)
                df2 = pd.DataFrame(islamic_serializer.data)

                # Merge dataframes
                file_name = f"USERS_DATA_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                merged_df = pd.concat([df1, df2], axis=1)
                merged_df.to_csv(file_path, index=False)
                data = {'file_link': file_path}
                return Response(data)
            else:
                alnafi_obj = alnafi_user(q, start_date, end_date, isPaying)
                islamic_obj = islamic_user(q, start_date, end_date,isPaying)
                queryset = list(alnafi_obj) + list(islamic_obj)
                serializer_dict = {
                        AlNafi_User: AlnafiUserSerializer,
                        IslamicAcademy_User: IslamicAcademyUserSerializer,
                    }

                paginator = MyPagination()
                paginated_queryset = paginator.paginate_queryset(queryset, request)
                serializer = []
                for obj in paginated_queryset:
                    serializer_class = serializer_dict.get(obj.__class__)
                    serializer.append(serializer_class(obj).data)
                return paginator.get_paginated_response(serializer)




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
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        password = serializer.data.get('password')
        user = authenticate(email=email, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({'token':token, 'msg':'Login Success'}, status=status.HTTP_200_OK)
        else:
            return Response({'errors':{'non_field_errors':['Email or Password is not Valid']}}, status=status.HTTP_404_NOT_FOUND)
        
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
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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
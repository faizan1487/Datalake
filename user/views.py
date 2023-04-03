from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import AlNafi_User, IslamicAcademy_User
from .serializers import AlnafiUserSerializer, IslamicAcademyUserSerializer
from .services import alnafi_user, islamic_user
from rest_framework import status

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
        if source == 'alnafiuser':
            alnafi_obj = alnafi_user(q, start_date, end_date, isPaying)
            paginator = MyPagination()
            paginated_queryset = paginator.paginate_queryset(alnafi_obj, request)
            alnafi_serializer = AlnafiUserSerializer(paginated_queryset,many=True)
            return paginator.get_paginated_response(alnafi_serializer.data)
        elif source =='islamicacademyuser':
            islamic_obj = islamic_user(q, start_date, end_date, isPaying)
            paginator = MyPagination()
            paginated_queryset = paginator.paginate_queryset(islamic_obj, request)
            islamic_serializer = IslamicAcademyUserSerializer(paginated_queryset,many=True)
            return paginator.get_paginated_response(islamic_serializer.data)
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
        
        
        
        
# class RegisterView(APIView):
#     """
#     Register User
#     <h2>Body Format:-</h2> 
#     {
# "username":"new",
# "email":"new@gmail.com",
# "password":"admin123",
# "first_name":"new",
# "last_name":"user",
# "phone":"234324"
# }
#     """

#     # @staticmethod
#     def post(self, request):
#         password = request.data['password']
#         email = request.data['email']
#         request.data['country'] = getCountryISO(request)
#         serializer = UserSerializer(
#             data=request.data, action="deserialize")
#         serializer.is_valid(raise_exception=True)
#         # REAL_EMAIL_API_KEY = env('REAL_EMAIL_API_KEY')
        
#         # email_response = requests.get(
#         #     "https://isitarealemail.com/api/email/validate",
#         #     params = {'email': email},
#         #     headers = {'Authorization': "Bearer " + REAL_EMAIL_API_KEY })


#         # email_status = email_response.json()['status']
#         # if email_status == "invalid":
#         #     return Response({"Invalid": "Email is invalid"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             serializer.save()
#         except Exception as _:
#             return Response({"Invalid": "user with this username already exists."}, status=status.HTTP_400_BAD_REQUEST)

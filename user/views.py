from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import AlnafiUser, IslamicAcademyUser
from .serializers import AlnafiUserSerializer, IslamicAcademyUserSerializer
from .services import alnafi_user, islamic_user
# Create your views here.

class MyPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100   

class GetUserDetails(APIView):
    def get(self, request):
        q = self.request.GET.get('q')
        isPaying = self.request.GET.get('ispaying')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        source = self.request.GET.get('source')
        
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
            islamic_obj = islamic_user(q, start_date, end_date)
            queryset = list(alnafi_obj) + list(islamic_obj)
            serializer_dict = {
                    AlnafiUser: AlnafiUserSerializer,
                    IslamicAcademyUser: IslamicAcademyUserSerializer,
                }

            paginator = MyPagination()
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            serializer = []
            for obj in paginated_queryset:
                serializer_class = serializer_dict.get(obj.__class__)
                serializer.append(serializer_class(obj).data)
            
            return paginator.get_paginated_response(serializer)
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .models import Thinkific_Users_Enrollments, Thinkific_User
from .serializers import ThinkificUserSerializer,ThinkificUserEnrollmentSerializer
# Create your views here.
class MyPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100  


class DeleteEnroll(APIView):
    def get(self, request):
        objs = Thinkific_Users_Enrollments.objects.all()
        objs.delete()
        return Response("data deleted")   
    
    
class GetThinkificUsers(APIView):
    def get(self, request):
        queryset = Thinkific_User.objects.all()
        paginator = MyPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        thinkific_user_serializer = ThinkificUserSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(thinkific_user_serializer.data)
        
        
class GetUserEnrollments(APIView):
    def get(self, request):
        query = self.request.GET.get('q', None) or None
        queryset = Thinkific_Users_Enrollments.objects.filter(email__iexact=query)
        paginator = MyPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        user_enrollemnt_serializer = ThinkificUserEnrollmentSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(user_enrollemnt_serializer.data)
        
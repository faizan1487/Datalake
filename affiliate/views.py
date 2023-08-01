from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
# Create your views here.
from .models import AffiliateUser, AffiliateUniqueClick, AffiliateLead
from django.db.models import Q
from django.db.models import Count
from .serializers import AffiliateSerializer, AffiliateClickSerializer, AffiliateLeadSerializer
from rest_framework import status
from django.http import HttpResponse
from threading import Thread

class MyPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100  


class AffiliateUsers(APIView):
    # permission_classes = [IsAuthenticated]
    # permission_classes = [GroupPermission]
    # required_groups = ['Sales', 'Admin']
    def get(self, request):
        q = self.request.GET.get('q', None) or None
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        export = self.request.GET.get('export', None) or None
        url = request.build_absolute_uri()
        # payments = cache.get(url+'payments')
        # if payments is None:
        users = AffiliateUser.objects.annotate(user_clicks_count=Count('user_clicks')).values('first_name','last_name','email','phone','address','country','created_at','user_clicks_count')
        
        if q:
            users = users.filter(email__icontains=q)

        if not start_date:
            first_user = users.exclude(created_at=None).last()
            start_date = first_user['created_at'].date() if first_user else None

        if not end_date:
            last_user = users.exclude(created_at=None).first()
            end_date = last_user['created_at'].date() if last_user else None
        
        paginator = MyPagination()
        paginated_queryset = paginator.paginate_queryset(users, request)
        return paginator.get_paginated_response(paginated_queryset)
    


class CreateAffiliateUser(APIView):
    def post(self, request):
        data = request.data
        email = data.get("email")

        try:
            instance = AffiliateUser.objects.get(email=email)
            serializer = AffiliateSerializer(instance, data=data)
        except:
            serializer = AffiliateSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class CreateAffiliateLead(APIView):
    def post(self, request):
        data = request.data.copy()
        user  = AffiliateUser.objects.get(email=data['affiliate'])
        data['affiliate'] = user.id
        email = data.get("email")

        try:
            instance = AffiliateLead.objects.get(email=email)
            serializer = AffiliateLeadSerializer(instance, data=data)
        except:
            serializer = AffiliateLeadSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CreateAffiliateClick(APIView):
    def post(self, request):
        data = request.data
        serializer = AffiliateClickSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class UserDelete(APIView):
    def get(self, request):
        objs = AffiliateUniqueClick.objects.all()
        objs.delete()
        return Response('deleted')
    

class UpdateAffiliateUser(APIView):
    def get(self, request):
        Thread(target=self.get_thread, args=(request,)).start()
        return HttpResponse("working")
     
    def get_thread(self, request):
        email_string = self.request.GET.get('emails', None) or None
        if email_string:
            emails = email_string.split(',')
            users = AffiliateUser.objects.filter(email__in=emails)
        else:
            users = AffiliateUser.objects.all()

        for user in users:
            print(user)
            user.save()
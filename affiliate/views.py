from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
# Create your views here.
from .models import AffiliateUser, AffiliateUniqueClick, AffiliateLead, Commission
from django.db.models import Q
from django.db.models import Count
from .serializers import (AffiliateSerializer, AffiliateClickSerializer, AffiliateLeadSerializer,
                          CommissionSerializer)
from rest_framework import status
from django.http import HttpResponse
from threading import Thread
from datetime import date, datetime, timedelta
from rest_framework.permissions import IsAuthenticated

class MyPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100  
  
permission_classes = [IsAuthenticated]
class CreateAffiliateUser(APIView):
    def get(self, request):
        # q = self.request.GET.get('q', None) or None
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        email = self.request.GET.get('email', None) or None
        # export = self.request.GET.get('export', None) or None
        # url = request.build_absolute_uri()
        # payments = cache.get(url+'payments')
        # if payments is None:
        # users = AffiliateUser.objects.annotate(user_clicks_count=Count('affiliate_clicks'),affiliate_leads_count=Count('affiliate_leads')).values('first_name','last_name','email','phone','address','country','created_at','user_clicks_count','affiliate_leads_count')
        
        if email:
            affiliateusers = AffiliateUser.objects.filter(email=email)
        else:
            affiliateusers = AffiliateUser.objects.filter(email="testuser@gmail.com")
        
        for user in affiliateusers:
            leads = user.affiliate_leads.all().values("first_name","last_name","email",
                                                    "contact","address","country","created_at")
            clicks = user.affiliate_clicks.all().values("pkr_price","usd_price","created_at")
            commissions = user.affiliate_commission.all().values("order_id","product","source",
                                                                "amount_pkr","amount_usd",
                                                                "commission_usd","commission_pkr","is_paid","created_at")
            # print(commissions)
        if not start_date:
            first_lead = leads.exclude(created_at=None).first()
            start_date_lead = first_lead['created_at'].date() if first_lead else None
            first_click = clicks.exclude(created_at=None).first()
            start_date_click = first_click['created_at'].date() if first_click else None
            first_commission = commissions.exclude(created_at=None).first()
            # print("fursi commission", first_commission)
            start_date_commission = first_commission['created_at'].date() if first_commission else None
            
        if start_date:
            start_date_lead = start_date
            start_date_click = start_date
            start_date_commission = start_date

        if not end_date:
            last_lead = leads.exclude(created_at=None).last()
            end_date_lead = last_lead['created_at'].date() if last_lead else None
            end_date_lead += timedelta(days=1)
            last_click = clicks.exclude(created_at=None).last()
            end_date_click = last_click['created_at'].date() if last_click else None
            end_date_click += timedelta(days=1)
            last_commission = commissions.exclude(created_at=None).last()
            # print("last", last_commission)
            end_date_commission = last_commission['created_at'].date() if last_commission else None
            end_date_commission += timedelta(days=1)
        
        if end_date:
            end_date_lead = end_date
            end_date_click = end_date
            end_date_commission = end_date
        
        # print(commissions)
        # print(start_date_commission)
        # print(end_date_commission)
        leads = leads.filter(created_at__range=(start_date_lead, end_date_lead))
        clicks = clicks.filter(created_at__range=(start_date_click, end_date_click))
        # commissions = commissions.filter(Q(date__date__lte=end_date_commission) & Q(date__date__gte=start_date_commission))
        commissions = commissions.filter(date__range=(start_date_commission, end_date_commission))
        agent_data = {
            'agent_name': user.first_name,
            'agent_leads': leads,
            'agent_clicks': clicks,
            'affiliate_commissions': commissions
        }

        # paginator = MyPagination()
        # paginated_queryset = paginator.paginate_queryset(agent_data, request) 
        # return paginator.get_paginated_response(paginated_queryset)
        return Response(agent_data)
    
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
        data = request.data.copy()
        user  = AffiliateUser.objects.get(email=data['affiliate'])
        data['affiliate'] = user.id
        ip = data.get("ip")
        
        try:
            instance = AffiliateUniqueClick.objects.get(ip=ip)
            serializer = AffiliateClickSerializer(instance, data=data)
        except:
            serializer = AffiliateClickSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CreateCommission(APIView):
    def post(self, request):
        data = request.data.copy()
        user  = AffiliateUser.objects.get(email=data['affiliate'])
        data['affiliate'] = user.id
        order_id = data.get("order_id")

        try:
            instance = Commission.objects.get(order_id=order_id)
            serializer = CommissionSerializer(instance, data=data)
        except:
            serializer = CommissionSerializer(data=data)

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
            # print(user)
            user.save()
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
  
class CreateAffiliateUser(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Get query parameters from the request
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        email = self.request.GET.get('email', None) or None
        # export = self.request.GET.get('export', None) or None
        # url = request.build_absolute_uri()
        # payments = cache.get(url+'payments')
        # if payments is None:
        # users = AffiliateUser.objects.annotate(user_clicks_count=Count('affiliate_clicks'),affiliate_leads_count=Count('affiliate_leads')).values('first_name','last_name','email','phone','address','country','created_at','user_clicks_count','affiliate_leads_count')
        
        # Fetch AffiliateUser(s) based on the provided email or a default email if not provided
        if email:
            affiliateusers = AffiliateUser.objects.filter(email=email)
        else:
            affiliateusers = AffiliateUser.objects.filter(email="shawanakiyani10@gmail.com")

        # Iterate through each AffiliateUser and retrieve associated leads, clicks, and commissions
        for user in affiliateusers:
            leads = user.affiliate_leads.all().values("first_name","last_name","email",
                                                    "contact","address","country","created_at")
            clicks = user.affiliate_clicks.all().values("pkr_price","usd_price","created_at")
            commissions = user.affiliate_commission.all().values("order_id","product","source",
                                                                "amount_pkr","amount_usd",
                                                                "commission_usd","commission_pkr","is_paid","created_at")
            # print(commissions)

        # If start_date is not provided, set it to the earliest date among leads, clicks, and commissions
        if not start_date:
            first_lead = leads.exclude(created_at=None).first()
            start_date_lead = first_lead['created_at'].date() if first_lead else None
            first_click = clicks.exclude(created_at=None).first()
            start_date_click = first_click['created_at'].date() if first_click else None
            first_commission = commissions.exclude(created_at=None).first()
            start_date_commission = first_commission['created_at'].date() if first_commission else None

        # If start_date is provided, use it for all start_date values
        if start_date:
            start_date_lead = start_date
            start_date_click = start_date
            start_date_commission = start_date

        # If end_date is not provided, set it to the day after the latest date among leads, clicks, and commissions
        if not end_date:
            last_lead = leads.exclude(created_at=None).last()
            end_date_lead = last_lead['created_at'].date() if last_lead else None
            end_date_lead += timedelta(days=1)
            last_click = clicks.exclude(created_at=None).last()
            end_date_click = last_click['created_at'].date() if last_click else None
            end_date_click += timedelta(days=1)
            last_commission = commissions.exclude(created_at=None).last()
            end_date_commission = last_commission['created_at'].date() if last_commission else None
            end_date_commission += timedelta(days=1)

        # If end_date is provided, use it for all end_date values
        if end_date:
            end_date_lead = end_date
            end_date_click = end_date
            end_date_commission = end_date
        
     

        # Filter leads, clicks, and commissions based on the date ranges
        leads = leads.filter(created_at__range=(start_date_lead, end_date_lead))
        clicks = clicks.filter(created_at__range=(start_date_click, end_date_click))
        commissions = commissions.filter(date__range=(start_date_commission, end_date_commission))
    
        # Create a dictionary containing agent data
        agent_data = {
            'agent_name': user.first_name,
            'agent_leads': leads,
            'agent_clicks': clicks,
            'affiliate_commissions': commissions
        }

        # Return the agent_data dictionary as a response
        return Response(agent_data)
    
    def post(self, request):
        data = request.data
        email = data.get("email")  # Get the 'email' field from the data

        try:
            instance = AffiliateUser.objects.get(email=email)  # Try to get an existing AffiliateUser instance with the provided email
            serializer = AffiliateSerializer(instance, data=data)  # Create a serializer instance with the existing instance and new data
        except AffiliateUser.DoesNotExist:  # If the instance does not exist
            serializer = AffiliateSerializer(data=data)  # Create a new serializer instance with the provided data

        if serializer.is_valid():  # Check if the serializer data is valid
            serializer.save()  # Save the serializer data to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return the serialized data with a successful response status


 
class GetAffiliateUser(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Get query parameters from the request
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        email = self.request.GET.get('email', None) or None

        # Fetch all AffiliateUser instances and retrieve specific fields ("email", "username", "first_name")
        affiliate = AffiliateUser.objects.all().values("email","username","first_name")

        # Return the retrieved data as a response
        return Response(affiliate)

class CreateAffiliateLead(APIView):
    def post(self, request):
        # Copy the incoming data to avoid modifying the original request data
        data = request.data.copy()
        # Get the AffiliateUser instance associated with the provided 'affiliate' email
        user  = AffiliateUser.objects.get(email=data['affiliate'])
        # Replace the 'affiliate' field in data with the ID of the AffiliateUser instance
        data['affiliate'] = user.id
        # Get the 'email' field from the data
        email = data.get("email")

        try:
            # Try to get an existing AffiliateLead instance with the provided email
            instance = AffiliateLead.objects.get(email=email)
            # Create a serializer instance with the existing instance and new data
            serializer = AffiliateLeadSerializer(instance, data=data)
        except:
            # If the instance does not exist, create a new serializer instance with the provided data
            serializer = AffiliateLeadSerializer(data=data)

        if serializer.is_valid():
            # If serializer data is valid, save the data to the database
            serializer.save()
            # Return the serialized data with a successful response status
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # If serializer data is not valid, return the validation errors with a bad request response status
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Define a view class to handle the creation of AffiliateClick instances
class CreateAffiliateClick(APIView):
    def post(self, request):
        # Copy the incoming data to avoid modifying the original request data
        data = request.data.copy()
        # Retrieve the AffiliateUser instance using the provided email
        user  = AffiliateUser.objects.get(email=data['affiliate'])
        # Replace the email in the data with the corresponding AffiliateUser's ID
        data['affiliate'] = user.id
        # Get the IP address from the data
        ip = data.get("ip")
        
        try:
            # Try to retrieve an existing AffiliateUniqueClick instance based on the IP address
            instance = AffiliateUniqueClick.objects.get(ip=ip)
            # Initialize the serializer with the retrieved instance and updated data
            serializer = AffiliateClickSerializer(instance, data=data)
        except:
            # If no existing instance is found, create a new instance and initialize the serializer with data
            serializer = AffiliateClickSerializer(data=data)

        if serializer.is_valid():
            # If the serializer's data is valid, save the instance and return a success response
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # If the serializer's data is invalid, return an error response with the validation errors
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
    permission_classes = [IsAuthenticated]
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
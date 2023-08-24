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
from django.conf import settings
from django.http import HttpResponse
from threading import Thread
from datetime import date, datetime, timedelta
from rest_framework.permissions import IsAuthenticated
from payment.services import get_USD_rate
from user.services import upload_csv_to_s3
import pandas as pd
import os
from django.http import JsonResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
import datetime

class MyPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100  
  
class CreateAffiliateUser(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        # Get query parameters from the request
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        email = self.request.GET.get('email', None) or None
        product = self.request.GET.get('product', None) or None
        export = self.request.GET.get('export', None) or None
        
        # Fetch AffiliateUser(s) based on the provided email or a default email if not provided
        try:
            if email:
                affiliateuser = AffiliateUser.objects.filter(email=email)
            else:
                affiliateuser = AffiliateUser.objects.all()
        except AffiliateUser.DoesNotExist:
            return Response("No matching record found for the provided email.")
        
        # Fetch leads, clicks, and commissions related to the selected AffiliateUsers
        affiliateuser = affiliateuser.prefetch_related(
            'affiliate_leads',
            'affiliate_clicks',
            'affiliate_commission'
        )

        # Apply filters based on the provided product
        if product:
            affiliateuser = affiliateuser.filter(affiliate_commission__product=product)

        # If start_date is provided, use it for all date ranges
        if start_date:
            start_date_lead = start_date_click = start_date_commission = start_date
        else:
            # Calculate the earliest date among leads, clicks, and commissions
            first_lead = affiliateuser.exclude(affiliate_leads__created_at=None).earliest('affiliate_leads__created_at')
            first_click = affiliateuser.exclude(affiliate_clicks__created_at=None).earliest('affiliate_clicks__created_at')
            first_commission = affiliateuser.exclude(affiliate_commission__created_at=None).earliest('affiliate_commission__created_at')
            
            start_date_lead = first_lead.affiliate_leads.first().created_at.date() if first_lead else None
            start_date_click = first_click.affiliate_clicks.first().created_at.date() if first_click else None
            start_date_commission = first_commission.affiliate_commission.first().created_at.date() if first_commission else None

        
        # If end_date is provided, use it for all date ranges
        if end_date:
            end_date_lead = end_date_click = end_date_commission = end_date
        else:
            # Calculate the latest date among leads, clicks, and commissions
            last_lead = affiliateuser.exclude(affiliate_leads__created_at=None).latest('affiliate_leads__created_at')
            last_click = affiliateuser.exclude(affiliate_clicks__created_at=None).latest('affiliate_clicks__created_at')
            last_commission = affiliateuser.exclude(affiliate_commission__created_at=None).latest('affiliate_commission__created_at')
            
            end_date_lead = last_lead.affiliate_leads.last().created_at.date() + timedelta(days=1) if last_lead else None
            end_date_click = last_click.affiliate_clicks.last().created_at.date() + timedelta(days=1) if last_click else None
            end_date_commission = last_commission.affiliate_commission.last().created_at.date() + timedelta(days=1) if last_commission else None
        

        # Filter leads, clicks, and commissions based on the date ranges
        # filtered_leads = affiliateuser.filter(affiliate_leads__created_at__range=(start_date_lead, end_date_lead))
        # filtered_clicks = affiliateuser.filter(affiliate_clicks__created_at__range=(start_date_click, end_date_click))
        # filtered_commissions = affiliateuser.filter(affiliate_commission__created_at__range=(start_date_commission, end_date_commission))


        agents_list = []
        total_amount_pkr = 0
        usd_rate = get_USD_rate()
        # Iterate through each AffiliateUser and construct agent data
        for user in affiliateuser:
            agent_data = {
                'agent_name': user.first_name,
                'agent_leads': list(user.affiliate_leads.filter(created_at__range=(start_date_lead, end_date_lead)).values()),
                'agent_clicks': list(user.affiliate_clicks.filter(created_at__range=(start_date_click, end_date_click)).values()),
                'affiliate_commissions': list(user.affiliate_commission.filter(created_at__range=(start_date_commission, end_date_commission)).values()),
                'agent_sales': 0
            }

            agent_sales = 0
            for commission in user.affiliate_commission.all():
                # print(commission)
                amount_pkr = commission.amount_pkr
                amount_usd = commission.amount_usd
                converted_amount_pkr = amount_usd * usd_rate['PKR']
                total_amount_pkr += amount_pkr + converted_amount_pkr
                agent_sales += amount_pkr + converted_amount_pkr


            agent_data['agent_sales'] = agent_sales
          
                
            agents_list.append(agent_data)

        # Sort agents_list based on total_amount_pkr in descending order
        sorted_agents = sorted(agents_list, key=lambda x: x['agent_sales'], reverse=True)

        # Get the top 10 agents
        top_10_agents = sorted_agents[:10]
        # print(top_10_agents)
        top_agents = []
        for agent in top_10_agents:
            agent_name = agent['agent_name']
            agent_sale = agent.get('agent_sales', 0) 

            top_agents.append({'agent': agent_name,'agent_sales': agent_sale})

        # print(top_agents)

        
        # print(total_amount_pkr)

         # Calculate the sum of amount_pkr from all commissions for the current agent
    

        if export == 'true':
            #For CSV WORKING:
            Header = []
            for i in agents_list:
                agent_leads = i.get('agent_leads', [])  # Use an empty list as the default value if key is not present
                for data_dict in agent_leads:
                    if data_dict:
                        Header.extend(['agent_name'])
                        Header.extend(data_dict.keys())
                        break
            if Header:
                pass
            else:
                Header = ['agent_name','first_name', 'last_name','email','contact','address','country','created_at']

            # Create an empty DataFrame with the specified columns
            # df = pd.DataFrame(columns=Header)
            
            # Create a list to hold the DataFrames
            dfs = []

            for i in agents_list:
                agent_name = i.get('agent_name', "")
                agent_leads = i.get('agent_leads', [])  # Use an empty list as the default value if key is not present
                for data_dict in agent_leads:
                    if data_dict:
                        data_dict["agent_name"] = agent_name
                        # data_dict["product_name"] = product_name
                        dfs.append(pd.DataFrame([data_dict]))
                        # df = pd.concat([df, pd.DataFrame([data_dict])], ignore_index=True)
                        # df = df.append(data_dict, ignore_index=True)
            
            # Concatenate all DataFrames in the list
            df = pd.concat(dfs, ignore_index=True)
            
            file_name = f"AFFILIATE_DATA_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            df = df.to_csv(index=False)
            s3 = upload_csv_to_s3(df,file_name)
            data = {'file_link': file_path,'export':'true'}
            return Response(data)


        # Convert datetime objects to strings using a custom JSON encoder
        class CustomJSONEncoder(DjangoJSONEncoder):
            def default(self, obj):
                if isinstance(obj, datetime.datetime):
                    return obj.strftime('%Y-%m-%d %H:%M:%S')
                return super().default(obj)

        agents_list.append({'total_sales': total_amount_pkr})
        # Return the agent_data dictionary as a response
        return JsonResponse(agents_list, encoder=CustomJSONEncoder, safe=False)
    
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
        # Fetch all AffiliateUser instances and retrieve specific fields ("email", "username", "first_name")
        affiliate = AffiliateUser.objects.all().values("email")

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
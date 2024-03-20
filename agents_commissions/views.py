from django.shortcuts import render
import requests
# Create your views here.
from rest_framework.views import APIView
from .models import Daily_lead, Daily_Sales_Support
from rest_framework.response import Response
from .serializers import DailyLeadSerializer, DailySalesSupportSerializer
from rest_framework import status


class DailyLead(APIView):
    def post(self, request):
        data = request.data
        id = data.get('id')
        print("data", data)

        serializer = DailyLeadSerializer(data=data)
        if serializer.is_valid():
            # print(serializer)
            # print("is valid")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = request.data 
        id = data.get('id')

        try:
            instance = Daily_lead.objects.get(id=id)
            serializer = DailyLeadSerializer(instance, data=data)
        except Daily_lead.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():

            if data['manager_approval'] == 'True' and data['manager_approval_crm'] == 'True' and data['veriification_cfo'] == 'True' and data['completely_verified'] == '1' and data['paid'] == '0':
                serializer.validated_data['is_comission'] = True
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = request.data
        id = data.get('id')

        try:
            instance = Daily_lead.objects.get(id=id)
            instance.delete()
            return Response("deleted")
        except Daily_lead.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    
class DailySalesSupport(APIView):


    def post(self, request):
        # print("in post")
        data = request.data
        print(data)
        id = data.get('id')
        serializer = DailySalesSupportSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    def put(self, request):
        data = request.data 
        id = data.get('id')
        print("data", data)

        try:
            instance = Daily_Sales_Support.objects.get(id=id)
            serializer = DailySalesSupportSerializer(instance, data=data)
        except:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            if data['manager_approval'] == 'True' and data['manager_approval_crm'] == 'True' and data['veriification_cfo'] == 'True' and data['completely_verified'] == '1' and data['paid'] == '0':
                serializer.validated_data['is_comission'] = True
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request):
        data = request.data
        # print("data", data)
        id = data.get('id')

        try:
            instance = Daily_Sales_Support.objects.get(id=id)
            # print(instance)
            instance.delete()
            # print("deleted")
            return Response("deleted")
        except Daily_Sales_Support.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
  


class ResaveLeadsAPIView(APIView):
    def get(self, request):
        # Retrieve leads with lead_creator as 'administrator'
        leads = Daily_lead.objects.filter(lead_creator = 'ribal.shahid@alnafi.edu.pk')
        print(leads)
        # Iterate over the leads and re-save them
        for lead in leads:
            print(lead)
            lead.save()
        return Response({"message": "Leads re-saved successfully."})
    

class MatchingId(APIView):
    def get(self, request):
        # url = 'https://crm.alnafi.com/api/resource/Daily Sales Module?fields=["*"]&limit_start=0&limit_page_length=10000000'
        url = 'https://crm.alnafi.com/api/resource/Daily Sales For Support?fields=["*"]&limit_start=0&limit_page_length=10000000'
        api_key = "4e7074f890507cb"
        api_secret = "c954faf5ff73d31"

        headers = {
            'Authorization': f'token {api_key}:{api_secret}',
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        response_get = requests.get(url, headers=headers)
        if response_get.status_code == 200:
            response_data = response_get.json()
            data = response_data.get('data', [])
            # print(len(data))
            # all_daily_leads = Daily_lead.objects.all()
            all_daily_leads = Daily_Sales_Support.objects.all()

            for record in data:
                api_name = record.get('name')

                matching_ids = all_daily_leads.filter(id=api_name)
                if matching_ids.exists():
                    print(f"This is in my Model: {api_name}")
                else:
                    print(f"This is not there: {api_name}")

            return Response(response_data)
        else:
            return Response({'error': 'Failed to retrieve data from the API'}, status=response_get.status_code)
        


class UpdateDailyLead(APIView):
    def get(self, request):
        print("get")
        leads = Daily_Sales_Support.objects.all()
        
   
        for lead in leads:
            if lead.manager_approval == 'True' and lead.manager_approval_crm == 'True' and lead.veriification_cfo == 'True' and lead.completely_verified == '1' and lead.paid == '0':
                lead.is_comission = True
                lead.save()

        return Response("vdifbvofd")
    




from rest_framework.permissions import IsAuthenticated




class FetchAgentLeads(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        status = request.GET.get('status', None)
        agent = request.GET.get('agent', None)
        start_date = request.GET.get('start_date'),
        end_date = request.GET.get('end_date'),
        export = request.GET.get('export'),
        page = int(request.GET.get('page', 1))  # Default to page 1 if not provided
        limit = int(request.GET.get('limit', 10))  # Default limit to 10 if not provided


        #admin keys
        user_api_key = '4e7074f890507cb'
        user_secret_key = 'c954faf5ff73d31'


        agents = {
            'ahsan': {'user_api_key':'b5658b2d5a087d0','user_secret_key':'a9faaabc26bddc5'},
            'wamiq': {'user_api_key':'31c85c7e921b270','user_secret_key':'845aff8197932c3'},
        }

        if agent in agents:
            user_api_key = agents[agent]['user_api_key']
            user_secret_key = agents[agent]['user_secret_key']

        headers = {
            'Authorization': f'token {user_api_key}:{user_secret_key}',
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if status:
            url = f'https://crm.alnafi.com/api/resource/Lead?fields=["*"]&filters=[["Lead","status","=","{status}"]]&limit_page_length=10000000000'
        else:
            url = f'https://crm.alnafi.com/api/resource/Lead?fields=["email_id"]&&limit_page_length={limit}&limit_start={(page-1)*limit}'

        response = requests.get(url, headers=headers)
        lead_data = response.json()
        print(len(lead_data['data']))

        return Response(lead_data)
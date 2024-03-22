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
import datetime

class FetchAgentLeads(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        status = request.GET.get('status', None)
        agent = request.GET.get('agent', None)
        start_date_param = request.GET.get('start_date',None)
        end_date_param = request.GET.get('end_date',None)
        export = request.GET.get('export')
        page = int(request.GET.get('page', 1))  # Default to page 1 if not provided
        limit = int(request.GET.get('limit', 10))  # Default limit to 10 if not provided

        #admin keys
        user_api_key = '4e7074f890507cb'
        user_secret_key = 'c954faf5ff73d31'

        agents = {
            'Wamiq': {'user_api_key':'31c85c7e921b270','user_secret_key':'845aff8197932c3'},
            'Shoaib': {'user_api_key': '484f3e9978c00f3','user_secret_key':'f61de5c03b3935d'},
            'Suleman': {'user_api_key': '3f6d0f005e4fccc','user_secret_key':'bbcaef6140205d2'},
            'Ribal': {'user_api_key': '39d14c9d602fa09','user_secret_key':'216de0a015e7fd1'},
            'Sunil': {'user_api_key': '9d37a29d966277f','user_secret_key':'018c3f6127c43cc'},
            'Rehan': {'user_api_key': 'b6a9a44a08790f8','user_secret_key':'b6d91bfa5792ccc'},
            'Marij': {'user_api_key': 'b3bb7a167ec651a','user_secret_key':'449cd28cd263361'},
            'Waqas': {'user_api_key': 'b09d1796de6444a','user_secret_key':'b09d1796de6444a'},
            'Hamza': {'user_api_key': 'dd3d10e83dfbb6b','user_secret_key':'a1a50d549455fe3'},
            'Toqir': {'user_api_key': '5306bb96b02c8f1','user_secret_key':'362d44b933cef9e'},
            'Saad': {'user_api_key': 'e31afcb884def7e','user_secret_key':'cb799e6913b57f9'},
            'Saima': {'user_api_key': '3da0a250742fa00','user_secret_key':'5ec8bb8e1e94930'},

            'Zeeshan': {'user_api_key': 'a17f7cc184a55ec','user_secret_key':'3e26bf2dde0db20'},
            'Haider': {'user_api_key': '2a1d467717681df','user_secret_key':'39faa082ac5f258'},
            'Mehtab': {'user_api_key': '6b0bb41dba21795','user_secret_key':'f56c627e47bdff6'},
            'Ahsan': {'user_api_key':'b5658b2d5a087d0','user_secret_key':'a9faaabc26bddc5'},
            'Mutahir': {'user_api_key': 'ee3c9803e0a7aa0','user_secret_key':'ad8a5dc4bc4f13f'},
            'Salman': {'user_api_key': 'c09e9698c024bd5','user_secret_key':'02c5e4ff622bb22'},
            'Mujtaba': {'user_api_key': '940ef42feabf766','user_secret_key':'7a642a5b930eb44'},
        }


        if agent in agents:
            user_api_key = agents[agent]['user_api_key']
            user_secret_key = agents[agent]['user_secret_key']

        headers = {
            'Authorization': f'token {user_api_key}:{user_secret_key}',
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        if status != '':
            url = f'https://crm.alnafi.com/api/resource/Lead?fields=["email_id","form","source","status","owner","date"]&filters=[["Lead","status","=","{status}"]]&limit_start=0&limit_page_length=100000000000000'

        if status == '':
            url = f'https://crm.alnafi.com/api/resource/Lead?fields=["email_id","form","source","status","owner","date"]&limit_start=0&limit_page_length=100000000000000'

        response = requests.get(url, headers=headers)
        all_lead_data = response.json()
        with_dates = [entry for entry in all_lead_data['data'] if entry.get("date") is not None]
        without_dates = [entry for entry in all_lead_data['data'] if entry.get("date") is None]

        sorted_with_dates = sorted(with_dates, key=lambda lead: datetime.datetime.strptime(lead["date"], "%Y-%m-%d"))
        all_lead_data = sorted_with_dates + without_dates 

        if start_date_param == '':
            start_date = None
            i = 0
            while start_date is None and i < len(all_lead_data):
                start_date = all_lead_data[i].get('date', None)  # Handle potential absence of 'date' key
                i += 1
        
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()

        if start_date_param != '':
            start_date_param = datetime.datetime.strptime(start_date_param, '%Y-%m-%d').date()


        if end_date_param == '':
            end_date = None
            i = len(all_lead_data) - 1
            while end_date is None:
                end_date = all_lead_data[i].get('date', None)  # Handle potential absence of 'date' key
                i -= 1

            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()


        if end_date_param is not None and end_date_param != '':
            end_date_param = datetime.datetime.strptime(end_date_param, '%Y-%m-%d').date()


        filtered_leads = []

        if start_date_param == '' and end_date_param == '':     
            # print("1")   
            filtered_leads = filter_by_date(start_date,end_date,all_lead_data)
        elif start_date_param == '' and end_date_param != '':
            # print("2")
            filtered_leads = filter_by_date(start_date,end_date_param,all_lead_data)
        elif start_date_param != '' and end_date_param == '':
            # print("3")
            filtered_leads = filter_by_date(start_date_param,end_date,all_lead_data)
        else:
            # print("4")
            filtered_leads = filter_by_date(start_date_param,end_date_param,all_lead_data)

        if start_date_param == '' and end_date_param == '':        
            filtered_leads = filtered_leads + without_dates
        else:
            filtered_leads = filtered_leads

        if export:
            pass



        total_count = len(filtered_leads)
        pages = total_count // 10

        start_index = int((page - 1) * limit)
        end_index = int(start_index + limit)
        all_data = {}
        all_data['pages'] = pages+1
        all_data['total_count'] = total_count
        all_data['page'] = page
        all_data['leads'] = filtered_leads[start_index:end_index]
        return Response(all_data)
    


def filter_by_date(start_date, end_date,data):
    # print("start_date",start_date)
    # print("end_date",end_date)
    filtered_leads = []
    for lead in data:
        if lead['date'] is not None:
            lead_date = datetime.datetime.strptime(lead['date'], '%Y-%m-%d').date()
            if start_date <= lead_date <= end_date:
                filtered_leads.append(lead)

    return filtered_leads

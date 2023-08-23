from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from .models import Contacts, Inbox, Agent, Conversation
from django.http import HttpResponse
from threading import Thread
from rest_framework.response import Response
# Create your views here.
import requests
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
import math
from django.db.models import DateField, Count, F, Q
from django.db.models.functions import TruncDate
from django.utils.timezone import make_aware, get_current_timezone
import datetime
import math
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .services import week_chatwoot_data, week_month_convos, all_chatwoot_data, get_agents
import environ

env = environ.Env()
env.read_env()
api_access_token = env("API_ACCESS_TOKEN")


class ChatwootContacts(APIView):
    def save_instance(self, i):
        # if i.get("contact_inboxes") and len(i["contact_inboxes"]) > 0:
        #     # If the list is not empty, get the 'inbox_id'
        #     inbox_id = i["contact_inboxes"][0]["inbox"]["id"]
        #     inbox_instance = get_object_or_404(Inbox, id=inbox_id)
        # else:
        #     # If 'contact_inboxes' list is empty or does not exist, set 'inbox_instance' to None
        #     inbox_instance = None

        try:
            inbox_id = i["contact_inboxes"][0]["inbox"]["id"]
            # print(f"Fetching Inbox with ID: {inbox_id}")
            inbox_instance = get_object_or_404(Inbox, id=inbox_id)
        except Exception as e:
            # print(f"Error fetching Inbox with ID {inbox_id}: {e}")
            inbox_instance = None
        

        my_model_instance = Contacts(
            id=i['id'],
            first_name=i['name'],
            phone=i['phone_number'],
            email=i['email'],
            inbox=inbox_instance
        )
        my_model_instance.save()

    permission_classes = [IsAuthenticated]
    def get(self, request):
        count = 2741
        items_per_page = 15
        pages = math.ceil(count / items_per_page)
        for page_number in range(1, pages + 1):
            # print(page_number)
            # api_access_token = '7M41q5QiNfYDeHue6KzjWdzV'
            headers = {
                'api_access_token': api_access_token,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            params = {
                'page': page_number
            }

            url = 'https://chat.alnafi.com/api/v1/accounts/3/contacts'
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            threads = []
            for i in data['payload']:
                thread = Thread(target=self.save_instance, args=(i,))
                thread.start()
                threads.append(thread)

            # Wait for all threads to complete
            for thread in threads:
                thread.join()

        return Response(data)


class ConversationsReport(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Copy the incoming data to avoid modifying the original request data
        data = request.data.copy()
        # Get the query parameters from the request
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        days = self.request.GET.get('days', None) or None
        metric = self.request.GET.get('metric', None) or None


        # Calculate start_date and end_date based on selected days value
        if days is not None and int(days) in [7, 30, 90, 180, 365]:
            today = datetime.date.today()
            end_date = today
            start_date = end_date - datetime.timedelta(days=int(days))
    

        # Implement weekly, monthly, 3 months ,6 months, yearly filter 
        params = {
            'type': 'account',
        }

        if start_date:
            if isinstance(start_date, str):
                start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            since = make_aware(datetime.datetime.combine(start_date, datetime.datetime.min.time()), get_current_timezone())
        else:
            since = make_aware(datetime.datetime(2020, 1, 2), get_current_timezone())

        if end_date:
            if isinstance(end_date, str):
                end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            until = make_aware(datetime.datetime.combine(end_date, datetime.datetime.max.time()), get_current_timezone())
        else:
            until = make_aware(datetime.datetime(2023, 9, 2), get_current_timezone())


        # Calculate the time difference
        time_difference = until - since
        # Get the number of days from the time difference
        days_difference = time_difference.days
        # print("days difference",days_difference)
        # conversations = Conversation.objects.all().values()
        start_date = since.replace(tzinfo=None)
        end_date = until.replace(tzinfo=None)
        # end_date = end_date + timedelta(days=1, microseconds=-1)

        # Initialize an empty dictionary to store the response data
        response_dict = {}

        # Set the API access token and headers
        headers = {
        'api_access_token': api_access_token,
        "Content-Type": "application/json",
        "Accept": "application/json",
        }

        # Define the base URL for chatwoot reports
        url = 'https://chat.alnafi.com/api/v2/accounts/3/reports/'

         # Convert start_date and end_date to timestamps
        since = since.timestamp()
        until = until.timestamp()

        # Set parameters for the API request
        params['since'] = since
        params['until'] = until
        params['metric'] = metric
        # print(days_difference)
        if metric == "conversations_count":
            # if days_difference in [30, 90, 180, 365]:
            #     response_dict = week_month_convos(url,headers, params)
            if days_difference == 7:
                # Get conversations per date
                response_dict = week_chatwoot_data(url,headers, params)
            else:
                # Get conversations per date
                response_dict = week_month_convos(url,headers, params)
            
        elif metric == "incoming_messages_count":
            if days_difference == 7:
                response_dict = week_chatwoot_data(url,headers, params)            
            else:
                response_dict = week_month_convos(url,headers, params)

        elif metric == "outgoing_messages_count":
            if days_difference == 7:
                response_dict = week_chatwoot_data(url,headers, params)
            else:
                response_dict = week_month_convos(url,headers, params)        

        elif metric == "avg_first_response_time":
            if days_difference == 365:
                response_dict = week_month_convos(url,headers, params)
            elif days_difference == 180:
                response_dict = week_month_convos(url,headers, params)

            elif days_difference == 90:
                response_dict = week_month_convos(url,headers, params)
            elif days_difference == 30:
                response_dict = week_month_convos(url,headers, params)
            elif days_difference == 7:
                response_dict = week_chatwoot_data(url,headers, params)
            else:
                params['since'] = 1660521600.0
                params['until'] = 1692143999.999999
                response_dict = week_month_convos(url,headers, params)
                
        elif metric == "avg_resolution_time":
            
            if days_difference == 365:
                response_dict = week_month_convos(url,headers, params)
            elif days_difference == 180:
                response_dict = week_month_convos(url,headers, params)
            elif days_difference == 90:
                response_dict = week_month_convos(url,headers, params)
            elif days_difference == 30:
                response_dict = week_month_convos(url,headers, params)
            elif days_difference == 7:
                response_dict = week_chatwoot_data(url,headers, params)
            else:
                params['since'] = 1660521600.0
                params['until'] = 1692143999.999999
                response_dict = week_month_convos(url,headers, params)
        
        elif metric == "resolutions_count":
            if days_difference == 7:
                response_dict = week_chatwoot_data(url,headers, params)
            else:
                response_dict = week_month_convos(url,headers, params)

         
        # Make a summary API request to get overall data
        url = 'https://chat.alnafi.com/api/v2/accounts/3/reports/summary'
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        # Format average response time and resolution time
        avg_response_time_seconds = float(data['avg_first_response_time'])
        days = int(avg_response_time_seconds // 86400)
        hours = int((avg_response_time_seconds % 86400) // 3600)
        minutes = int((avg_response_time_seconds % 3600) // 60)

        if days > 0:
            data['avg_first_response_time'] = f"{str(days)} days {str(hours)} Hr {str(minutes)} min"
        else:
            data['avg_first_response_time'] = f"{str(hours)} Hr {str(minutes)} min"

        avg_resolution_time_seconds = float(data['avg_resolution_time'])
        days = int(avg_resolution_time_seconds // 86400)
        hours = int((avg_resolution_time_seconds % 86400) // 3600)
        minutes = int((avg_resolution_time_seconds % 3600) // 60)

        if days > 0:
            data['avg_resolution_time'] = f"{str(days)} days {str(hours)} Hr {str(minutes)} min"
        else:
            data['avg_resolution_time'] = f"{str(hours)} Hr {str(minutes)} min"

        response_dict["data"] = data
        # response_dict.append({"data":data})
        return Response(response_dict)
    

class AgentsReport(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = request.data.copy()
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        days = self.request.GET.get('days', None) or None
        id = self.request.GET.get('id', None) or None
        metric = self.request.GET.get('metric', None) or None

        if days is not None and int(days) in [7, 30, 90, 180, 365]:
            today = datetime.date.today()
            end_date = today
            start_date = end_date - datetime.timedelta(days=int(days))       
    
        params = {
            'type': 'agent',
            'id': id,
        }
        
        if start_date:
            if isinstance(start_date, str):
                start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            since = make_aware(datetime.datetime.combine(start_date, datetime.datetime.min.time()), get_current_timezone())
        else:
            since = make_aware(datetime.datetime(2020, 1, 2), get_current_timezone())

        if end_date:
            if isinstance(end_date, str):
                end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            until = make_aware(datetime.datetime.combine(end_date, datetime.datetime.max.time()), get_current_timezone())
        else:
            until = make_aware(datetime.datetime(2023, 9, 2), get_current_timezone())

        
        # Calculate the time difference
        time_difference = until - since
        # Get the number of days from the time difference
        days_difference = time_difference.days
        # conversations = Conversation.objects.all().values()
        start_date = since.replace(tzinfo=None)
        end_date = until.replace(tzinfo=None)
        # end_date = end_date + timedelta(days=1, microseconds=-1)
        response_dict = {}
        headers = {
        'api_access_token': api_access_token,
        "Content-Type": "application/json",
        "Accept": "application/json",
        }
        url = 'https://chat.alnafi.com/api/v2/accounts/3/reports/'
        since = since.timestamp()
        until = until.timestamp()
        params['since'] = since
        params['until'] = until
        params['metric'] = metric
        if metric == "conversations_count":
            if days_difference == 7:
                response_dict = week_chatwoot_data(url,headers, params)
            else:
                response_dict = week_month_convos(url,headers, params)
                    
        elif metric == "outgoing_messages_count":
            if days_difference == 7:
                response_dict = week_chatwoot_data(url,headers, params)
            else:
                response_dict = week_month_convos(url,headers, params)         
        elif metric == "avg_first_response_time":
            if days_difference == 365:
                response_dict = week_month_convos(url,headers, params)
            elif days_difference == 180:
                response_dict = week_month_convos(url,headers, params)
            elif days_difference == 90:
                response_dict = week_month_convos(url,headers, params)
            elif days_difference == 30:
                response_dict = week_month_convos(url,headers, params)
            elif days_difference == 7:
                response_dict = week_chatwoot_data(url,headers, params)
            else:
                params['since'] = 1660521600.0
                params['until'] = 1692143999.999999
                response_dict = week_month_convos(url,headers, params)
        elif metric == "avg_resolution_time": 
            if days_difference == 365:
                response_dict = week_month_convos(url,headers, params)
            elif days_difference == 180:
                response_dict = week_month_convos(url,headers, params)
            elif days_difference == 90:
                response_dict = week_month_convos(url,headers, params)
            elif days_difference == 30:
                response_dict = week_month_convos(url,headers, params)            
            elif days_difference == 7:
                response_dict = week_chatwoot_data(url,headers, params)
            else:
                params['since'] = 1660176000.0
                params['until'] = 1691798399.999999
                response_dict = week_month_convos(url,headers, params)

        elif metric == "resolutions_count":
            if days_difference == 7:
                response_dict = week_chatwoot_data(url,headers, params)
            else:
                response_dict = week_month_convos(url,headers, params)
                
        url = 'https://chat.alnafi.com/api/v2/accounts/3/reports/summary'
        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        avg_response_time_seconds = float(data['avg_first_response_time'])
        days = int(avg_response_time_seconds // 86400)
        hours = int((avg_response_time_seconds % 86400) // 3600)
        minutes = int((avg_response_time_seconds % 3600) // 60)

        if days > 0:
            data['avg_first_response_time'] = f"{str(days)} days {str(hours)} Hr {str(minutes)} min"
        else:
            data['avg_first_response_time'] = f"{str(hours)} Hr {str(minutes)} min"

        avg_resolution_time_seconds = float(data['avg_resolution_time'])
        days = int(avg_resolution_time_seconds // 86400)
        hours = int((avg_resolution_time_seconds % 86400) // 3600)
        minutes = int((avg_resolution_time_seconds % 3600) // 60)

        if days > 0:
            data['avg_resolution_time'] = f"{str(days)} days {str(hours)} Hr {str(minutes)} min"
        else:
            data['avg_resolution_time'] = f"{str(hours)} Hr {str(minutes)} min"

        agents = get_agents()
        filtered_data = [item for item in agents if item['id'] == int(id)]
        response_dict["data"] = data
        response_dict["data"]["agent_name"] = filtered_data[0]['available_name']
        return Response(response_dict)

class AgentsList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = get_agents()
        return Response(data)

class InboxesReport(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = request.data.copy()
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        days = self.request.GET.get('days', None) or None
        id = self.request.GET.get('id', None) or None
        metric = self.request.GET.get('metric', None) or None

        if days is not None and int(days) in [7, 30, 90, 180, 365]:
            today = datetime.date.today()
            end_date = today
            start_date = end_date - datetime.timedelta(days=int(days))   

        # Implement weekly, monthly, 3 months ,6 months, yearly filter 
        params = {
            'type': 'inbox',
            'id': id,
        }

        
        if start_date:
            if isinstance(start_date, str):
                start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            since = make_aware(datetime.datetime.combine(start_date, datetime.datetime.min.time()), get_current_timezone())
        else:
            since = make_aware(datetime.datetime(2020, 1, 2), get_current_timezone())

        if end_date:
            if isinstance(end_date, str):
                end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            until = make_aware(datetime.datetime.combine(end_date, datetime.datetime.max.time()), get_current_timezone())
        else:
            until = make_aware(datetime.datetime(2023, 9, 2), get_current_timezone())

        
        # Calculate the time difference
        time_difference = until - since
        # Get the number of days from the time difference
        days_difference = time_difference.days
        # conversations = Conversation.objects.all().values()
        start_date = since.replace(tzinfo=None)
        end_date = until.replace(tzinfo=None)
        # end_date = end_date + timedelta(days=1, microseconds=-1)
        response_dict = {}
        headers = {
        'api_access_token': api_access_token,
        "Content-Type": "application/json",
        "Accept": "application/json",
        }
        url = 'https://chat.alnafi.com/api/v2/accounts/3/reports/'
        since = since.timestamp()
        until = until.timestamp()
        params['since'] = since
        params['until'] = until
        params['metric'] = metric
     
        if metric == "conversations_count":
            if days_difference == 7:
                response_dict = week_chatwoot_data(url,headers, params)
            else:
                response_dict = week_month_convos(url,headers, params)
                    
        elif metric == "outgoing_messages_count":
            if days_difference == 7:
                response_dict = week_chatwoot_data(url,headers, params)
            else:
                response_dict = week_month_convos(url,headers, params)           
        elif metric == "avg_first_response_time":
            if days_difference == 365:
                response_dict = week_month_convos(url,headers, params)
            elif days_difference == 180:
                response_dict = week_month_convos(url,headers, params)
            elif days_difference == 90:
                response_dict = week_month_convos(url,headers, params)
            elif days_difference == 30:
                response_dict = week_month_convos(url,headers, params)
            elif days_difference == 7:
                response_dict = week_chatwoot_data(url,headers, params)
            else:
                params['since'] = 1660521600.0
                params['until'] = 1692143999.999999
                response_dict = week_month_convos(url,headers, params)
        elif metric == "avg_resolution_time": 
            if days_difference == 365:
                response_dict = week_month_convos(url,headers, params)
            elif days_difference == 180:
                response_dict = week_month_convos(url,headers, params)
            elif days_difference == 90:
                response_dict = week_month_convos(url,headers, params)
            elif days_difference == 30:
                response_dict = week_month_convos(url,headers, params)            
            elif days_difference == 7:
                response_dict = week_chatwoot_data(url,headers, params)
            else:
                params['since'] = 1660176000.0
                params['until'] = 1691798399.999999
                response_dict = week_month_convos(url,headers, params)

        elif metric == "resolutions_count":
            if days_difference == 7:
                response_dict = week_chatwoot_data(url,headers, params)
            else:
                response_dict = week_month_convos(url,headers, params)
                
        url = 'https://chat.alnafi.com/api/v2/accounts/3/reports/summary'
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        avg_response_time_seconds = float(data['avg_first_response_time'])
        days = int(avg_response_time_seconds // 86400)
        hours = int((avg_response_time_seconds % 86400) // 3600)
        minutes = int((avg_response_time_seconds % 3600) // 60)

        if days > 0:
            data['avg_first_response_time'] = f"{str(days)} days {str(hours)} Hr {str(minutes)} min"
        else:
            data['avg_first_response_time'] = f"{str(hours)} Hr {str(minutes)} min"

        avg_resolution_time_seconds = float(data['avg_resolution_time'])
        days = int(avg_resolution_time_seconds // 86400)
        hours = int((avg_resolution_time_seconds % 86400) // 3600)
        minutes = int((avg_resolution_time_seconds % 3600) // 60)

        if days > 0:
            data['avg_resolution_time'] = f"{str(days)} days {str(hours)} Hr {str(minutes)} min"
        else:
            data['avg_resolution_time'] = f"{str(hours)} Hr {str(minutes)} min"

        response_dict["data"] = data
        return Response(response_dict)



class ConversationsList(APIView):
    permission_classes = [IsAuthenticated]
    def save_instance(self, i):
        try:
            inbox_id = i["inbox_id"]
            inbox_instance = get_object_or_404(Inbox, id=inbox_id)
        except:
            inbox_instance = None

        try:
            contact_id = i["meta"]["sender"]["id"]
            contact_instance = get_object_or_404(Contacts, id=contact_id)
        except:    
            contact_instance = None

        try:
            agent_id = i["meta"]["assignee"]["id"]
            agent_instance = get_object_or_404(Agent, id=agent_id)
        except:
            agent_instance = None

        created_at = float(i['created_at'])
        dt_object = datetime.datetime.fromtimestamp(created_at)
        formatted_date = dt_object.strftime('%Y-%m-%d')

        try:
            my_model_instance = Conversation(
                contact=contact_instance,
                channel=i["meta"]['channel'],
                agent=agent_instance,
                id=i['id'],
                inbox=inbox_instance,
                created_at=formatted_date
            )
            my_model_instance.save()
        except Exception as e:
            print(e)

    permission_classes = [IsAuthenticated]
    def get(self, request):
        count = 4145
        items_per_page = 25
        pages = math.ceil(count / items_per_page)

        for page_number in range(1, pages + 1):
            headers = {
                'api_access_token': api_access_token,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            params = {
                'page': page_number
            }

            url = 'https://chat.alnafi.com/api/v1/accounts/3/conversations'
            response = requests.get(url, headers=headers, params=params)
            data = response.json()

            threads = []
            for i in data['data']['payload']:
                thread = Thread(target=self.save_instance, args=(i,))
                thread.start()
                threads.append(thread)

            # Wait for all threads to complete
            for thread in threads:
                thread.join()

        return Response(data)



class InboxesList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        headers = {
        'api_access_token': api_access_token,
        "Content-Type": "application/json",
        "Accept": "application/json",
        }
        url = 'https://chat.alnafi.com/api/v1/accounts/3/inboxes'
        response = requests.get(url, headers=headers)
        data = response.json()
        response_list = []

        for i in data['payload']:
            response_list.append({'id': i['id'], 'name': i['name']})  
           
        
        return Response(response_list)



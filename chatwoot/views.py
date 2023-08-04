from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from .models import Contacts, Inbox, Agent, Conversation
from django.http import HttpResponse
from threading import Thread
from rest_framework.response import Response
# Create your views here.
import requests
from datetime import datetime
from django.shortcuts import get_object_or_404
import math


class ChatwootContacts(APIView):
    # def get(self, request):
    #     Thread(target=self.get_thread, args=(request,)).start()
    #     return HttpResponse("working")

    # def get_thread(self, request):
    #     email_string = self.request.GET.get('emails', None) or None
    #     if email_string:
    #         emails = email_string.split(',')
    #         users = Contacts.objects.filter(email__in=emails)
    #     else:
    #         users = Contacts.objects.all()

    #     for user in users:
    #         # print(user)
    #         user.save()

    def get(self, request):
        count= 2741
        # count= 30
        items_per_page = 15
        pages = math.ceil(count / items_per_page)
        for page_number in range(1, pages + 1):
            api_access_token = '7M41q5QiNfYDeHue6KzjWdzV'
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
            # print(data)
            for i in data['payload']:
                if i.get("contact_inboxes") and len(i["contact_inboxes"]) > 0:
                    # If the list is not empty, get the 'inbox_id'
                    inbox_id = i["contact_inboxes"][0]["inbox"]["id"]
                    inbox_instance = get_object_or_404(Inbox, id=inbox_id)
                else:
                    # If 'contact_inboxes' list is empty or does not exist, set 'inbox_instance' to None
                    inbox_instance = None
                # print(inbox_instance)
                my_model_instance = Contacts(
                    id=i['id'],
                    first_name=i['name'],
                    phone=i['phone_number'],
                    email=i['email'],
                    # city = i['city'],
                    # country = i['country'],
                    inbox = inbox_instance
                )
                my_model_instance.save()
        return Response(data)


class ConversationsReport(APIView):
    def get(self, request):
        data = request.data.copy()
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        # Implement weekly monthly 3 months 6 months yearly filter 
        params = {
            'type': 'account',
        }

        if start_date:
            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
            since = start_date_obj.timestamp()
        else:
            since=1577963949
            #Thu Jan 02 2020 
        
        if end_date:
            end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
            until = end_date_obj.timestamp()
        else:
            until=1693653549
            #Sat Sep 02 2023

        print(since)
        print(until)

        # Convert the timestamps to datetime objects
        datetime1 = datetime.fromtimestamp(since)
        datetime2 = datetime.fromtimestamp(until)
        # Calculate the time difference
        time_difference = datetime2 - datetime1
        # Get the number of days from the time difference
        days_between = time_difference.days
        #start date end date ka difference agar week se kam he to sirf days ki analytics(convos par  day)
        #start date end date ka difference agar week se zada he aur month se kam he to sirf weeks ki analytics(convos per week)

        if days_between < 7:
            conversations = Conversation.objects.filter(created_at__range=(datetime1, datetime2))
            payments = payments.filter(Q(order_datetime__date__lte=end_date) & Q(order_datetime__date__gte=start_date))
        else:
            conversations = Conversation.objects.filter(created_at__range=(datetime1, datetime2))


        # print("conversations.count",conversations.count())

        params['since'] = since
        params['until'] = until

        api_access_token = '7M41q5QiNfYDeHue6KzjWdzV'
        headers = {
        'api_access_token': api_access_token,
        "Content-Type": "application/json",
        "Accept": "application/json",
        }
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

        return Response(data)
    

class ConversationsList(APIView):
    def get(self, request):
        count= 4145
        # count = 100
        items_per_page = 25
        pages = math.ceil(count / items_per_page)

        for page_number in range(1, pages + 1):
            # print(page_number)
            api_access_token = '7M41q5QiNfYDeHue6KzjWdzV'
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
            # print(len(data['data']['payload']))
            for i in data['data']['payload']:
                # print(i["inbox_id"])
                try:
                    # If the list is not empty, get the 'inbox_id'
                    inbox_id = i["inbox_id"]
                    # print(inbox_id)
                    inbox_instance = get_object_or_404(Inbox, id=inbox_id)
                except:
                    inbox_instance = None

                # print(inbox_instance)
                # print(i["meta"]["sender"]["id"])
                try:
                    # If the list is not empty, get the 'inbox_id'
                    contact_id = i["meta"]["sender"]["id"]
                    contact_instance = get_object_or_404(Contacts, id=contact_id)
                except:    
                    contact_instance = None
                # print(contact_instance)

                try:
                    # If the list is not empty, get the 'inbox_id'
                    agent_id = i["meta"]["assignee"]["id"]
                    agent_instance = get_object_or_404(Agent, id=agent_id)
                except:
                    # If 'contact_inboxes' list is empty or does not exist, set 'inbox_instance' to None
                    agent_instance = None
                # print(agent_instance)
                created_at = float(i['created_at'])
                dt_object = datetime.fromtimestamp(created_at)
                # Format the datetime object as a string in the "YYYY-MM-DD" format
                formatted_date = dt_object.strftime('%Y-%m-%d')

                try:
                    # print("saving")
                    my_model_instance = Conversation(
                        contact=contact_instance,
                        channel=i["meta"]['channel'],
                        agent=agent_instance,
                        id = i['id'],
                        inbox = inbox_instance,
                        created_at= formatted_date
                    )
                    my_model_instance.save()
                except Exception as e:
                    print(e)
        return Response(data)


class InboxesList(APIView):
    def get(self, request):
        api_access_token = '7M41q5QiNfYDeHue6KzjWdzV'
        headers = {
        'api_access_token': api_access_token,
        "Content-Type": "application/json",
        "Accept": "application/json",
        }
        url = 'https://chat.alnafi.com/api/v1/accounts/3/inboxes'
        response = requests.get(url, headers=headers)
        data = response.json()
        
        

        for i in data['payload']:
            my_model_instance = Inbox(
                id=i['id'],
                name=i['name'],
                channel_type=i['channel_type']
            )
            my_model_instance.save()
        return Response(data)


class AgentsList(APIView):
    def get(self, request):
        api_access_token = '7M41q5QiNfYDeHue6KzjWdzV'
        headers = {
        'api_access_token': api_access_token,
        "Content-Type": "application/json",
        "Accept": "application/json",
        }
        url = 'https://chat.alnafi.com/api/v1/accounts/3/agents'
        response = requests.get(url, headers=headers)
        data = response.json()
        
        for i in data:
            my_model_instance = Agent(
                email=i['email'],
                name=i['name'],
                available_name=i['available_name'],
                role=i['role']
            )
            my_model_instance.save()
        return Response(data)
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
        days = self.request.GET.get('days', None) or None


        if days is not None and int(days) == 7:
            # Get the current date
            end_date = datetime.date.today()

            # Subtract 7 days from the current date
            start_date = end_date - datetime.timedelta(days=7)

        # Implement weekly monthly 3 months 6 months yearly filter 
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

        # print("since", since)
        # print("until", until)
        
        # Calculate the time difference
        time_difference = until - since
        # Get the number of days from the time difference
        days_difference = time_difference.days
       
        conversations = Conversation.objects.all().values()
        response_dict = {}

        start_date = since.replace(tzinfo=None)
        end_date = until.replace(tzinfo=None)
        # end_date = end_date + timedelta(days=1, microseconds=-1)
        if days_difference >= 30:
            # Get conversations per date
            conversations_per_date = conversations.filter(
                created_at__date__range=[start_date, end_date]
            ).annotate(
                conversation_date=TruncDate('created_at'),
            ).values(
                'conversation_date',
            ).annotate(
                conversation_count=Count('id')
            )

            # Create a list of all dates between start_date and end_date
            date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

            # Create a dictionary to store conversation counts for each date
            conversation_counts = {date: 0 for date in date_range}

            # Update conversation counts with data from conversations_per_date
            for item in conversations_per_date:
                conversation_date = item['conversation_date']
                conversation_count = item['conversation_count']
                conversation_counts[conversation_date] = conversation_count


            # Create a list of dictionaries containing date and conversation count
            result_list = [{'conversation_date': date.strftime('%Y-%m-%d'), 'conversation_count': conversation_counts[date]} for date in date_range]

            # Add the result_list to the response_dict
            response_dict["conversations_per_date"] = result_list
            # print(result_list)

            # response_dict["conversations_per_date"] = list(conversations_per_date)

            # Calculate the number of weeks in the data
            # print(len(conversations_per_date))
            weeks = len(conversations_per_date) // 7
            # print(weeks)
            if len(conversations_per_date) % 7 > 0:
                weeks += 1
            # Initialize an empty list to store the grouped conversations
            grouped_conversations = []
            # Loop through the data and create groups for each week
            for i in range(weeks):
                start_idx = i * 7
                end_idx = start_idx + 7
                week_conversations = conversations_per_date[start_idx:end_idx]
                # print(week_conversations)
                total_count = sum(conv['conversation_count'] for conv in week_conversations)
                grouped_conversations.append({f"{conversations_per_date[start_idx]['conversation_date']}": total_count})

            response_dict["conversations_per_week"] = grouped_conversations

            # Calculate the number of weeks in the data
            months = len(conversations_per_date) // 30
            if len(conversations_per_date) % 30 > 0:
                months += 1

            # Initialize an empty list to store the grouped conversations
            grouped_conversations = []
            # Loop through the data and create groups for each week
            for i in range(months):
                start_idx = i * 30
                end_idx = start_idx + 30
                month_conversations = conversations_per_date[start_idx:end_idx]
                total_count = sum(conv['conversation_count'] for conv in month_conversations)
                grouped_conversations.append({f"{conversations_per_date[start_idx]['conversation_date']}": total_count})

            response_dict["conversations_per_month"] = grouped_conversations
            # print(grouped_conversations)
        
        elif days_difference >=7:
            # Get conversations per date
            conversations_per_date = conversations.filter(
                created_at__date__range=[start_date, end_date]
            ).annotate(
                conversation_date=TruncDate('created_at'),
            ).values(
                'conversation_date',
            ).annotate(
                conversation_count=Count('id')
            )

            response_dict["conversations_per_date"] = list(conversations_per_date)

            # Calculate the number of weeks in the data
            weeks = len(conversations_per_date) // 7
            if len(conversations_per_date) % 7 > 0:
                weeks += 1

            # Initialize an empty list to store the grouped conversations
            grouped_conversations = []
            # Loop through the data and create groups for each week
            for i in range(weeks):
                start_idx = i * 7
                end_idx = start_idx + 7
                week_conversations = conversations_per_date[start_idx:end_idx]
                total_count = sum(conv['conversation_count'] for conv in week_conversations)
                grouped_conversations.append({f"{conversations_per_date[start_idx]['conversation_date']}": total_count})

            response_dict["conversations_per_week"] = grouped_conversations
            # print(grouped_conversations)
        else:
            # Get conversations per date
            conversations_per_date = conversations.filter(
                created_at__date__range=[start_date, end_date]
            ).annotate(
                conversation_date=TruncDate('created_at'),
            ).values(
                'conversation_date',
            ).annotate(
                conversation_count=Count('id')
            )

            response_dict["conversations_per_date"] = list(conversations_per_date)

        since = since.timestamp()
        until = until.timestamp()
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

        response_dict["data"] = data
        # response_dict.append({"data":data})
        return Response(response_dict)
    

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
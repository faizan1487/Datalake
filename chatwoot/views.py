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

    def get(self, request):
        count = 2741
        items_per_page = 15
        pages = math.ceil(count / items_per_page)
        for page_number in range(1, pages + 1):
            # print(page_number)
            api_access_token = '7M41q5QiNfYDeHue6KzjWdzV'
            headers = {
                'api_access_token': '7M41q5QiNfYDeHue6KzjWdzV',
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



    # def get(self, request):
    #     count= 2741
    #     # count= 30
    #     items_per_page = 15
    #     pages = math.ceil(count / items_per_page)
    #     for page_number in range(1, pages + 1):
    #         api_access_token = '7M41q5QiNfYDeHue6KzjWdzV'
    #         headers = {
    #         'api_access_token': api_access_token,
    #         "Content-Type": "application/json",
    #         "Accept": "application/json",
    #         }

    #         params = {
    #             'page': page_number
    #         }

    #         url = 'https://chat.alnafi.com/api/v1/accounts/3/contacts'
    #         response = requests.get(url, headers=headers, params=params)
    #         data = response.json()
    #         # print(data)
    #         for i in data['payload']:
    #             if i.get("contact_inboxes") and len(i["contact_inboxes"]) > 0:
    #                 # If the list is not empty, get the 'inbox_id'
    #                 inbox_id = i["contact_inboxes"][0]["inbox"]["id"]
    #                 inbox_instance = get_object_or_404(Inbox, id=inbox_id)
    #             else:
    #                 # If 'contact_inboxes' list is empty or does not exist, set 'inbox_instance' to None
    #                 inbox_instance = None
    #             # print(inbox_instance)
    #             my_model_instance = Contacts(
    #                 id=i['id'],
    #                 first_name=i['name'],
    #                 phone=i['phone_number'],
    #                 email=i['email'],
    #                 # city = i['city'],
    #                 # country = i['country'],
    #                 inbox = inbox_instance
    #             )
    #             my_model_instance.save()
    #     return Response(data)



permission_classes = [IsAuthenticated]
class ConversationsReport(APIView):
    def get(self, request):
        data = request.data.copy()
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        days = self.request.GET.get('days', None) or None
        metric = self.request.GET.get('metric', None) or None

        if days is not None and int(days) == 7:
            # Get the current date
            end_date = datetime.date.today()

            # Subtract 7 days from the current date
            start_date = end_date - datetime.timedelta(days=7)
        elif days is not None and int(days) == 30:
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=30)
        elif days is not None and int(days) == 90:
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=90)
        elif days is not None and int(days) == 180:
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=180)
        elif days is not None and int(days) == 365:
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=365)
        else:
            end_date = datetime.date.today()
            # Subtract 7 days from the current date
            start_date = end_date - datetime.timedelta(days=365)

            
        # print(start_date)
        # print(end_date)

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
        conversations = Conversation.objects.all().values()
        start_date = since.replace(tzinfo=None)
        end_date = until.replace(tzinfo=None)
        # end_date = end_date + timedelta(days=1, microseconds=-1)
        response_dict = {}
        api_access_token = '7M41q5QiNfYDeHue6KzjWdzV'
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
        # print(days_difference)
        if metric == "conversations_count":
            if days_difference == 365:
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data) 
                response_dict["data_per_date"] = data
                # response_dict["data_per_date"] = list(data_per_date)

                # Calculate the number of weeks in the data
                # print(len(data_per_date))
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_conversations = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_conversations = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_conversations)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_conversations.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_conversations

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_conversations = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_conversations = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in month_conversations)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    grouped_conversations.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_month"] = grouped_conversations
                # print(grouped_conversations)

            elif days_difference == 30:
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data) 
                response_dict["data_per_date"] = data
                # response_dict["data_per_date"] = list(data_per_date)

                # Calculate the number of weeks in the data
                # print(len(data_per_date))
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_conversations = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_conversations = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_conversations)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_conversations.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_conversations

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_conversations = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_conversations = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in month_conversations)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    grouped_conversations.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_month"] = grouped_conversations
                # print(grouped_conversations)


            elif days_difference == 180:
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data) 
                response_dict["data_per_date"] = data
                # response_dict["data_per_date"] = list(data_per_date)

                # Calculate the number of weeks in the data
                # print(len(data_per_date))
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_conversations = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_conversations = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_conversations)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_conversations.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_conversations

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_conversations = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_conversations = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in month_conversations)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    grouped_conversations.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_month"] = grouped_conversations
                # print(grouped_conversations)

            elif days_difference == 90:
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data) 
                response_dict["data_per_date"] = data
                # response_dict["data_per_date"] = list(data_per_date)

                # Calculate the number of weeks in the data
                # print(len(data_per_date))
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_conversations = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_conversations = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_conversations)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_conversations.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_conversations

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_conversations = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_conversations = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in month_conversations)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    grouped_conversations.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_month"] = grouped_conversations
                # print(grouped_conversations)
            
            elif days_difference == 7:
                # Get conversations per date

                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data) 
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                if len(data) % 7 > 0:
                    weeks += 1

                # Initialize an empty list to store the grouped conversations
                grouped_conversations = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_conversations = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in week_conversations)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_conversations.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_conversations
                # print(grouped_conversations)
            else:
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data) 
                response_dict["data_per_date"] = data
        elif metric == "incoming_messages_count":
            if days_difference == 365:
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_messages

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_messages = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in month_messages)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_month"] = grouped_messages

            elif days_difference == 30:
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_messages

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_messages = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in month_messages)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_month"] = grouped_messages
            
            elif days_difference == 7:
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_messages
            
            else:
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data) 
                response_dict["data_per_date"] = data            
        elif metric == "outgoing_messages_count":
            
            if days_difference == 365:
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_messages

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_messages = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in month_messages)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_month"] = grouped_messages
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()
                    # print(week_conversations)

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_messages

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_messages = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in month_messages)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_month"] = grouped_messages

            elif days_difference == 30:
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()
                    # print(week_conversations)

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_messages

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_messages = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in month_messages)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_month"] = grouped_messages

            elif days_difference == 7:
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })
                
                response_dict["data_per_week"] = grouped_messages
            
            else:
                print("outgoing messsages else")
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data) 
                response_dict["data_per_date"] = data            
        elif metric == "avg_first_response_time":
            if days_difference == 365:
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_messages

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_messages = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in month_messages)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_month"] = grouped_messages


            if days_difference == 30:
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_messages

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_messages = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in month_messages)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_month"] = grouped_messages

            elif days_difference == 7:
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })
    
                response_dict["data_per_week"] = grouped_messages
            else:
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data) 
                response_dict["data_per_date"] = data


        elif metric == "avg_resolution_time":
            
            if days_difference == 30:
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])

                    avg_resolution_time_seconds = float(i['value'])
                    days = int(avg_resolution_time_seconds // 86400)
                    hours = int((avg_resolution_time_seconds % 86400) // 3600)
                    minutes = int((avg_resolution_time_seconds % 3600) // 60)

                    if days > 0:
                        i['value'] = f"{str(days)} days {str(hours)} Hr {str(minutes)} min"
                    else:
                        i['value'] = f"{str(hours)} Hr {str(minutes)} min"

                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['count'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_messages

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_messages = data[start_idx:end_idx]
                    total_count = sum(conv['count'] for conv in month_messages)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_month"] = grouped_messages
            elif days_difference == 7:
                response = requests.get(url, headers=headers, params=params)
                data = response.json()
                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])

                    avg_resolution_time_seconds = float(i['value'])
                    days = int(avg_resolution_time_seconds // 86400)
                    hours = int((avg_resolution_time_seconds % 86400) // 3600)
                    minutes = int((avg_resolution_time_seconds % 3600) // 60)

                    if days > 0:
                        i['value'] = f"{str(days)} days {str(hours)} Hr {str(minutes)} min"
                    else:
                        i['value'] = f"{str(hours)} Hr {str(minutes)} min"

                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date

                #  data_per_date
                data = list(data)
                response_dict["data_per_date"] = data
                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_messages)
                    # print(week_conversations)
                    total_count = sum(conv['count'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })
    
                response_dict["data_per_week"] = grouped_messages
            else:
                response = requests.get(url, headers=headers, params=params)
                data = response.json()
                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])

                    avg_resolution_time_seconds = float(i['value'])
                    days = int(avg_resolution_time_seconds // 86400)
                    hours = int((avg_resolution_time_seconds % 86400) // 3600)
                    minutes = int((avg_resolution_time_seconds % 3600) // 60)

                    if days > 0:
                        i['value'] = f"{str(days)} days {str(hours)} Hr {str(minutes)} min"
                    else:
                        i['value'] = f"{str(hours)} Hr {str(minutes)} min"

                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date

                # print(data)
                #  data_per_date
                data = list(data)
                response_dict["data_per_date"] = data
                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_messages)
                    # print(week_conversations)
                    total_count = sum(conv['count'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })
    
                response_dict["data_per_week"] = grouped_messages
        elif metric == "resolutions_count":
            if days_difference == 30:
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_messages

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_messages = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in month_messages)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_month"] = grouped_messages
            elif days_difference == 7:
                response = requests.get(url, headers=headers, params=params)
                data = response.json()
                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])

                    avg_resolution_time_seconds = float(i['value'])
                    days = int(avg_resolution_time_seconds // 86400)
                    hours = int((avg_resolution_time_seconds % 86400) // 3600)
                    minutes = int((avg_resolution_time_seconds % 3600) // 60)

                    if days > 0:
                        i['value'] = f"{str(days)} days {str(hours)} Hr {str(minutes)} min"
                    else:
                        i['value'] = f"{str(hours)} Hr {str(minutes)} min"

                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date

                # print(data)
                #  data_per_date
                data = list(data)
                response_dict["data_per_date"] = data
                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_messages)
                    # print(week_conversations)
                    total_count = sum(conv['count'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })
    
                response_dict["data_per_week"] = grouped_messages
        

        # api_access_token = '7M41q5QiNfYDeHue6KzjWdzV'
        # headers = {
        # 'api_access_token': api_access_token,
        # "Content-Type": "application/json",
        # "Accept": "application/json",
        # }
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
    

permission_classes = [IsAuthenticated]
class AgentsReport(APIView):
    def get(self, request):
        data = request.data.copy()
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        days = self.request.GET.get('days', None) or None
        id = self.request.GET.get('id', None) or None
        metric = self.request.GET.get('metric', None) or None

        # print(start_date)
        # print(end_date)
        # print(days)
        if days is not None and int(days) == 7:
            # Get the current date
            end_date = datetime.date.today()
        
            # Subtract 7 days from the current date
            start_date = end_date - datetime.timedelta(days=7)
        elif days is not None and int(days) == 30:
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=30)
        elif days is not None and int(days) == 90:
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=90)
        elif days is not None and int(days) == 180:
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=180)
        elif days is not None and int(days) == 365:
            end_date = datetime.date.today()
            start_date = end_date - datetime.timedelta(days=365)

        # print(start_date)
        # print(end_date)            
       

        # Implement weekly, monthly, 3 months ,6 months, yearly filter 
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
        conversations = Conversation.objects.all().values()
        start_date = since.replace(tzinfo=None)
        end_date = until.replace(tzinfo=None)
        # end_date = end_date + timedelta(days=1, microseconds=-1)
        response_dict = {}
        api_access_token = '7M41q5QiNfYDeHue6KzjWdzV'
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
        # print(days_difference)
        # print(start_date)
        # print(end_date)
        if metric == "conversations_count":
            if days_difference == 365:
                # print("365")
                response = requests.get(url, headers=headers, params=params)
                data = response.json()
                # print(data)
                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data) 
                response_dict["data_per_date"] = data
                # response_dict["data_per_date"] = list(data_per_date)

                # Calculate the number of weeks in the data
                # print(len(data_per_date))
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_conversations = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_conversations = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_conversations)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_conversations.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_conversations

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_conversations = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_conversations = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in month_conversations)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    grouped_conversations.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_month"] = grouped_conversations
                # print(grouped_conversations)

            elif days_difference == 180:
                print("180")
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data) 
                response_dict["data_per_date"] = data
                # response_dict["data_per_date"] = list(data_per_date)

                # Calculate the number of weeks in the data
                # print(len(data_per_date))
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_conversations = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_conversations = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_conversations)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_conversations.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_conversations
               
                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_conversations = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_conversations = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in month_conversations)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    grouped_conversations.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_month"] = grouped_conversations
                # print(grouped_conversations)


            elif days_difference == 90:
                print("90")
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data) 
                response_dict["data_per_date"] = data
                # response_dict["data_per_date"] = list(data_per_date)

                # Calculate the number of weeks in the data
                # print(len(data_per_date))
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_conversations = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_conversations = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_conversations)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_conversations.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_conversations

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_conversations = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_conversations = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in month_conversations)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    grouped_conversations.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_month"] = grouped_conversations
                # print(grouped_conversations)

            elif days_difference == 30:
                print("30")
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data) 
                response_dict["data_per_date"] = data
                # response_dict["data_per_date"] = list(data_per_date)

                # Calculate the number of weeks in the data
                # print(len(data_per_date))
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_conversations = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_conversations = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_conversations)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_conversations.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_conversations

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_conversations = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_conversations = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in month_conversations)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    grouped_conversations.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_month"] = grouped_conversations
                # print(grouped_conversations)
            
            elif days_difference == 7:
                # print("days_difference 7")
                # Get conversations per date

                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data) 
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                if len(data) % 7 > 0:
                    weeks += 1

                # Initialize an empty list to store the grouped conversations
                grouped_conversations = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_conversations = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in week_conversations)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_conversations.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_conversations
                # print(grouped_conversations)
            else:
                print("else")
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data) 
                response_dict["data_per_date"] = data
                    
        elif metric == "outgoing_messages_count":
            if days_difference == 365:
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_messages

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_messages = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in month_messages)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_month"] = grouped_messages
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()
                    # print(week_conversations)

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_messages

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_messages = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in month_messages)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_month"] = grouped_messages
            
            elif days_difference == 180:
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()
                    # print(week_conversations)

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_messages

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_messages = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in month_messages)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_month"] = grouped_messages


            elif days_difference == 90:
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()
                    # print(week_conversations)

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_messages

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_messages = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in month_messages)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_month"] = grouped_messages

            elif days_difference == 30:
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()
                    # print(week_conversations)

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_messages

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_messages = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in month_messages)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_month"] = grouped_messages

            elif days_difference == 7:
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })
                
                response_dict["data_per_week"] = grouped_messages
            
            else:
                # print("outgoing messsages else")
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data) 
                response_dict["data_per_date"] = data            
        elif metric == "avg_first_response_time":
            if days_difference == 365:
                # Get conversations per date
                # print(params)
                response = requests.get(url, headers=headers, params=params)
                data = response.json()
                
                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])

                    avg_resolution_time_seconds = float(i['value'])
                    days = int(avg_resolution_time_seconds // 86400)
                    hours = int((avg_resolution_time_seconds % 86400) // 3600)
                    minutes = int((avg_resolution_time_seconds % 3600) // 60)

                    if days > 0:
                        i['value'] = f"{str(days)} days {str(hours)} Hr {str(minutes)} min"
                    else:
                        i['value'] = f"{str(hours)} Hr {str(minutes)} min"

                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date

                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_messages)
                    total_count = sum(conv['count'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 

                    if i < len(week_messages):
                        value = week_messages[i]['value']
                    
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": value,
                        "count": total_count
                    })

                response_dict["data_per_week"] = grouped_messages

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_messages = data[start_idx:end_idx]
                    total_count = sum(conv['count'] for conv in month_messages)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    
                    if i < len(month_messages):
                        value = month_messages[i]['value']
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": value,
                        "count": total_count
                    })

                response_dict["data_per_month"] = grouped_messages

            elif days_difference == 180:
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])

                    avg_resolution_time_seconds = float(i['value'])
                    days = int(avg_resolution_time_seconds // 86400)
                    hours = int((avg_resolution_time_seconds % 86400) // 3600)
                    minutes = int((avg_resolution_time_seconds % 3600) // 60)

                    if days > 0:
                        i['value'] = f"{str(days)} days {str(hours)} Hr {str(minutes)} min"
                    else:
                        i['value'] = f"{str(hours)} Hr {str(minutes)} min"

                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['count'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 

                    if i < len(week_messages):
                        value = week_messages[i]['value']
                    
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": value,
                        "count": total_count
                    })

                response_dict["data_per_week"] = grouped_messages

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_messages = data[start_idx:end_idx]
                    total_count = sum(conv['count'] for conv in week_messages)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 

                    if i < len(month_messages):
                        value = month_messages[i]['value']
                    
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": value,
                        "count": total_count
                    })

                response_dict["data_per_month"] = grouped_messages

            elif days_difference == 90:
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()
                # print(data)
                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    avg_resolution_time_seconds = float(i['value'])
                    days = int(avg_resolution_time_seconds // 86400)
                    hours = int((avg_resolution_time_seconds % 86400) // 3600)
                    minutes = int((avg_resolution_time_seconds % 3600) // 60)

                    if days > 0:
                        i['value'] = f"{str(days)} days {str(hours)} Hr {str(minutes)} min"
                    else:
                        i['value'] = f"{str(hours)} Hr {str(minutes)} min"

                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    total_count = sum(conv['count'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 

                    if i < len(week_messages):
                        value = week_messages[i]['value']
                    
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": value,
                        "count": total_count
                    })

                response_dict["data_per_week"] = grouped_messages

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_messages = data[start_idx:end_idx]
                    total_count = sum(conv['count'] for conv in month_messages)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 

                    if i < len(month_messages):
                        value = month_messages[i]['value']
                    
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": value,
                        "count": total_count
                    })

                response_dict["data_per_month"] = grouped_messages

            elif days_difference == 30:
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])

                    avg_resolution_time_seconds = float(i['value'])
                    days = int(avg_resolution_time_seconds // 86400)
                    hours = int((avg_resolution_time_seconds % 86400) // 3600)
                    minutes = int((avg_resolution_time_seconds % 3600) // 60)

                    if days > 0:
                        i['value'] = f"{str(days)} days {str(hours)} Hr {str(minutes)} min"
                    else:
                        i['value'] = f"{str(hours)} Hr {str(minutes)} min"

                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['count'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 

                    if i < len(week_messages):
                        value = week_messages[i]['value']
                    
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": value,
                        "count": total_count
                    })

                response_dict["data_per_week"] = grouped_messages

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_messages = data[start_idx:end_idx]
                    total_count = sum(conv['count'] for conv in month_messages)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 

                    if i < len(month_messages):
                        value = month_messages[i]['value']
                    
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": value,
                        "count": total_count
                    })

                response_dict["data_per_month"] = grouped_messages


            elif days_difference == 7:
                print(params)
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])

                    avg_resolution_time_seconds = float(i['value'])
                    days = int(avg_resolution_time_seconds // 86400)
                    hours = int((avg_resolution_time_seconds % 86400) // 3600)
                    minutes = int((avg_resolution_time_seconds % 3600) // 60)

                    if days > 0:
                        i['value'] = f"{str(days)} days {str(hours)} Hr {str(minutes)} min"
                    else:
                        i['value'] = f"{str(hours)} Hr {str(minutes)} min"

                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['count'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 

                    if i < len(week_messages):
                        value = week_messages[i]['value']
                    
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": value,
                        "count": total_count
                    })
    
                response_dict["data_per_week"] = grouped_messages
            else:
                params['since'] = 1660176000.0
                params['until'] = 1691798399.999999
                response = requests.get(url, headers=headers, params=params)
                data = response.json()
                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])

                    avg_resolution_time_seconds = float(i['value'])
                    days = int(avg_resolution_time_seconds // 86400)
                    hours = int((avg_resolution_time_seconds % 86400) // 3600)
                    minutes = int((avg_resolution_time_seconds % 3600) // 60)

                    if days > 0:
                        i['value'] = f"{str(days)} days {str(hours)} Hr {str(minutes)} min"
                    else:
                        i['value'] = f"{str(hours)} Hr {str(minutes)} min"

                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data) 
                response_dict["data_per_date"] = data
        elif metric == "avg_resolution_time": 
            if days_difference == 365:
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])

                    avg_resolution_time_seconds = float(i['value'])
                    days = int(avg_resolution_time_seconds // 86400)
                    hours = int((avg_resolution_time_seconds % 86400) // 3600)
                    minutes = int((avg_resolution_time_seconds % 3600) // 60)

                    if days > 0:
                        i['value'] = f"{str(days)} days {str(hours)} Hr {str(minutes)} min"
                    else:
                        i['value'] = f"{str(hours)} Hr {str(minutes)} min"

                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['count'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 

                    if i < len(week_messages):
                        value = week_messages[i]['value']
                    
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": value,
                        "count": total_count
                    })

                response_dict["data_per_week"] = grouped_messages

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_messages = data[start_idx:end_idx]
                    total_count = sum(conv['count'] for conv in month_messages)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 

                    if i < len(month_messages):
                        value = month_messages[i]['value']
                    
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": value,
                        "count": total_count
                    })

                response_dict["data_per_month"] = grouped_messages

            elif days_difference == 180:
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])

                    avg_resolution_time_seconds = float(i['value'])
                    days = int(avg_resolution_time_seconds // 86400)
                    hours = int((avg_resolution_time_seconds % 86400) // 3600)
                    minutes = int((avg_resolution_time_seconds % 3600) // 60)

                    if days > 0:
                        i['value'] = f"{str(days)} days {str(hours)} Hr {str(minutes)} min"
                    else:
                        i['value'] = f"{str(hours)} Hr {str(minutes)} min"

                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['count'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 

                    if i < len(week_messages):
                        value = week_messages[i]['value']
                    
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": value,
                        "count": total_count
                    })

                response_dict["data_per_week"] = grouped_messages

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_messages = data[start_idx:end_idx]
                    total_count = sum(conv['count'] for conv in month_messages)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 

                    if i < len(month_messages):
                        value = month_messages[i]['value']
                    
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": value,
                        "count": total_count
                    })

                response_dict["data_per_month"] = grouped_messages


            elif days_difference == 90:
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])

                    avg_resolution_time_seconds = float(i['value'])
                    days = int(avg_resolution_time_seconds // 86400)
                    hours = int((avg_resolution_time_seconds % 86400) // 3600)
                    minutes = int((avg_resolution_time_seconds % 3600) // 60)

                    if days > 0:
                        i['value'] = f"{str(days)} days {str(hours)} Hr {str(minutes)} min"
                    else:
                        i['value'] = f"{str(hours)} Hr {str(minutes)} min"

                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['count'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 

                    if i < len(week_messages):
                        value = week_messages[i]['value']
                    
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": value,
                        "count": total_count
                    })

                response_dict["data_per_week"] = grouped_messages

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_messages = data[start_idx:end_idx]
                    total_count = sum(conv['count'] for conv in month_messages)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 

                    if i < len(month_messages):
                        value = month_messages[i]['value']
                    
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": value,
                        "count": total_count
                    })

                response_dict["data_per_month"] = grouped_messages

            elif days_difference == 30:
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])

                    avg_resolution_time_seconds = float(i['value'])
                    days = int(avg_resolution_time_seconds // 86400)
                    hours = int((avg_resolution_time_seconds % 86400) // 3600)
                    minutes = int((avg_resolution_time_seconds % 3600) // 60)

                    if days > 0:
                        i['value'] = f"{str(days)} days {str(hours)} Hr {str(minutes)} min"
                    else:
                        i['value'] = f"{str(hours)} Hr {str(minutes)} min"

                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['count'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 

                    if i < len(week_messages):
                        value = week_messages[i]['value']
                    
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": value,
                        "count": total_count
                    })

                response_dict["data_per_week"] = grouped_messages

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_messages = data[start_idx:end_idx]
                    total_count = sum(conv['count'] for conv in month_messages)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 

                    if i < len(month_messages):
                        value = month_messages[i]['value']
                    
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": value,
                        "count": total_count
                    })

                response_dict["data_per_month"] = grouped_messages
            
            
            
            elif days_difference == 7:
                response = requests.get(url, headers=headers, params=params)
                data = response.json()
                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])

                    avg_resolution_time_seconds = float(i['value'])
                    days = int(avg_resolution_time_seconds // 86400)
                    hours = int((avg_resolution_time_seconds % 86400) // 3600)
                    minutes = int((avg_resolution_time_seconds % 3600) // 60)

                    if days > 0:
                        i['value'] = f"{str(days)} days {str(hours)} Hr {str(minutes)} min"
                    else:
                        i['value'] = f"{str(hours)} Hr {str(minutes)} min"

                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date

                # print(data)
                #  data_per_date
                data = list(data)
                response_dict["data_per_date"] = data
                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_messages)
                    # print(week_conversations)
                    total_count = sum(conv['count'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 

                    if i < len(week_messages):
                        value = week_messages[i]['value']
                    
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": value,
                        "count": total_count
                    })
    
                response_dict["data_per_week"] = grouped_messages
            else:
                params['since'] = 1660176000.0
                params['until'] = 1691798399.999999
                response = requests.get(url, headers=headers, params=params)
                data = response.json()
                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    avg_resolution_time_seconds = float(i['value'])
                    days = int(avg_resolution_time_seconds // 86400)
                    hours = int((avg_resolution_time_seconds % 86400) // 3600)
                    minutes = int((avg_resolution_time_seconds % 3600) // 60)

                    if days > 0:
                        i['value'] = f"{str(days)} days {str(hours)} Hr {str(minutes)} min"
                    else:
                        i['value'] = f"{str(hours)} Hr {str(minutes)} min"

                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date

                # print(data)
                #  data_per_date
                data = list(data)
                response_dict["data_per_date"] = data
                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_messages)
                    # print(week_conversations)
                    total_count = sum(conv['count'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 

                    if i < len(week_messages):
                        value = week_messages[i]['value']
                    
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": value,
                        "count": total_count
                    })
    
                response_dict["data_per_week"] = grouped_messages
        elif metric == "resolutions_count":
            if days_difference == 365:
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_messages

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_messages = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in month_messages)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_month"] = grouped_messages

            if days_difference == 180:
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_messages

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_messages = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in month_messages)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_month"] = grouped_messages
            
            if days_difference == 90:
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_messages

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_messages = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in month_messages)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_month"] = grouped_messages
            
            
            elif days_difference == 30:
                # Get conversations per date
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data)
                response_dict["data_per_date"] = data

                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_week"] = grouped_messages

                # Calculate the number of weeks in the data
                months = len(data) // 30
                if len(data) % 30 > 0:
                    months += 1

                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(months):
                    start_idx = i * 30
                    end_idx = start_idx + 30
                    month_messages = data[start_idx:end_idx]
                    total_count = sum(conv['value'] for conv in month_messages)
                    if end_idx < len(data):
                        month_end_date = data[end_idx]['timestamp']
                    else:
                        month_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                        "value": total_count
                    })

                response_dict["data_per_month"] = grouped_messages
            elif days_difference == 7:
                response = requests.get(url, headers=headers, params=params)
                data = response.json()
                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date

                # print(data)
                #  data_per_date
                data = list(data)
                response_dict["data_per_date"] = data
                # Calculate the number of weeks in the data
                weeks = len(data) // 7
                # print(weeks)
                if len(data) % 7 > 0:
                    weeks += 1
                # Initialize an empty list to store the grouped conversations
                grouped_messages = []
                # Loop through the data and create groups for each week
                for i in range(weeks):
                    start_idx = i * 7
                    end_idx = start_idx + 7
                    week_messages = data[start_idx:end_idx]
                    # print(week_messages)
                    # print(week_conversations)
                    total_count = sum(conv['value'] for conv in week_messages)
                    if end_idx < len(data):
                        week_end_date = data[end_idx]['timestamp']
                    else:
                        week_end_date = "" 
                    grouped_messages.append({
                        "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                        "value": total_count
                    })
    
                response_dict["data_per_week"] = grouped_messages
            else:
                response = requests.get(url, headers=headers, params=params)
                data = response.json()

                for i in  data:
                    date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                    i['timestamp'] = formatted_date
                # data_per_date
                data = list(data) 
                response_dict["data_per_date"] = data
        

        # api_access_token = '7M41q5QiNfYDeHue6KzjWdzV'
        # headers = {
        # 'api_access_token': api_access_token,
        # "Content-Type": "application/json",
        # "Accept": "application/json",
        # }
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


# permission_classes = [IsAuthenticated]
class ConversationsList(APIView):

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

    def get(self, request):
        count = 4145
        items_per_page = 25
        pages = math.ceil(count / items_per_page)

        for page_number in range(1, pages + 1):
            print(page_number)
            api_access_token = '7M41q5QiNfYDeHue6KzjWdzV'
            headers = {
                'api_access_token': '7M41q5QiNfYDeHue6KzjWdzV',
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
        
        # for i in data:
        #     my_model_instance = Agent(
        #         email=i['email'],
        #         name=i['name'],
        #         available_name=i['available_name'],
        #         role=i['role']
        #     )
        #     my_model_instance.save()
        return Response(data)
import requests
import datetime
import math
import environ
from rest_framework.response import Response

env = environ.Env()
env.read_env()
api_access_token = env("API_ACCESS_TOKEN")

def week_month_convos(url,headers,params):
    # Call a function to fetch week-wise chatwoot data
    response_dict = week_chatwoot_data(url,headers,params)
    # Make a GET request to the provided URL with headers and parameters
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    # Calculate the number of months in the data
    months = len(data) // 30
    if len(data) % 30 > 0:
        months += 1

    # Initialize an empty list to store the grouped conversations
    grouped_conversations = []
    # Define metrics that require special processing
    metrics = ['avg_resolution_time','avg_first_response_time']
    # Check if the selected metric requires special processing
    if params['metric'] in metrics:
        for i in  data:
            # print(i)
            date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
            avg_resolution_time_seconds = float(i['value'])
            days = int(avg_resolution_time_seconds // 86400)
            hours = int((avg_resolution_time_seconds % 86400) // 3600)
            minutes = int((avg_resolution_time_seconds % 3600) // 60)

            if days > 0:
                i['value'] = f"{str(days)} days {str(hours)} Hr {str(minutes)} min"
            else:
                i['value'] = f"{str(hours)} Hr {str(minutes)} min"

            # print(i['value'])
            formatted_date = date_obj.strftime('%Y-%m-%d')
            i['timestamp'] = formatted_date
        
        for i in range(months):
            start_idx = i * 30
            end_idx = start_idx + 30
            month_messages = data[start_idx:end_idx]
            total_count = sum(conv['count'] for conv in month_messages)
            # print(start_idx)
            # print(end_idx)
            # print(month_messages)
            # Determine the month end date
            if end_idx < len(data):
                month_end_date = data[end_idx]['timestamp']
            else:
                month_end_date = "" 

            # Define a function to convert 'value' strings into minutes
            def value_to_minutes(value_str):
                if 'days' in value_str:
                    days, rest = value_str.split(' days ')
                    hours, minutes = rest.split(' Hr ')
                    return int(days) * 24 * 60 + int(hours) * 60 + int(minutes[:-4])
                elif 'Hr' in value_str:
                    hours, minutes = value_str.split(' Hr ')
                    return int(hours) * 60 + int(minutes[:-4])
                elif 'min' in value_str:
                    return int(value_str[:-7])
                else:
                    return 0
                
            max_value_dict = max(month_messages, key=lambda item: value_to_minutes(item['value']))
            value = max_value_dict['value']
            
            grouped_conversations.append({
                "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                "value": value,
                "count": total_count
            })
    else:
        # Format the timestamps for other metrics
        for i in  data:
            date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
            formatted_date = date_obj.strftime('%Y-%m-%d')
            i['timestamp'] = formatted_date

        # Loop through the data and create groups for each month
        for i in range(months):
            start_idx = i * 30
            end_idx = start_idx + 30
            month_conversations = data[start_idx:end_idx]
            total_count = sum(conv['value'] for conv in month_conversations)

            # Determine the month end date
            if end_idx < len(data):
                month_end_date = data[end_idx]['timestamp']
            else:
                month_end_date = "" 
            
            grouped_conversations.append({
                "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                "value": total_count
            })

    # Determine the month end date
    response_dict["data_per_month"] = grouped_conversations

    # Return the updated response dictionary
    return response_dict


def week_chatwoot_data(url,headers,params):
    # Initialize an empty dictionary to store the response data
    response_dict = {}
    # print(params)

    # Make a GET request to the provided URL with headers and parameters
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
     # Check if the selected metric requires special formatting
    metrics = ['avg_resolution_time','avg_first_response_time']
    if params['metric'] in metrics:
        # Format the data for metrics that need time-based representation
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
    else:
        # Format the timestamps for other metrics
        for i in  data:
            date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
            formatted_date = date_obj.strftime('%Y-%m-%d')
            i['timestamp'] = formatted_date

    # Add the formatted data to the response dictionary
    data = list(data) 
    response_dict["data_per_date"] = data

    # Calculate the number of weeks in the data
    weeks = len(data) // 7
    if len(data) % 7 > 0:
        weeks += 1

    # Initialize an empty list to store the grouped conversations
    grouped_conversations = []
    # Loop through the data and create groups for each week
    metrics = ['avg_resolution_time','avg_first_response_time']
    if params['metric'] in metrics:
        for i in range(weeks):
            start_idx = i * 7
            end_idx = start_idx + 7
            week_messages = data[start_idx:end_idx]
            # print(start_idx)
            # print(end_idx)
            # print(week_messages)
            # print(week_conversations)
            total_count = sum(conv['count'] for conv in week_messages)
            if end_idx < len(data):
                week_end_date = data[end_idx]['timestamp']
            else:
                week_end_date = ""

            # Define a function to convert 'value' strings into minutes
            def value_to_minutes(value_str):
                if 'days' in value_str:
                    days, rest = value_str.split(' days ')
                    hours, minutes = rest.split(' Hr ')
                    return int(days) * 24 * 60 + int(hours) * 60 + int(minutes[:-4])
                elif 'Hr' in value_str:
                    hours, minutes = value_str.split(' Hr ')
                    return int(hours) * 60 + int(minutes[:-4])
                elif 'min' in value_str:
                    return int(value_str[:-7])
                else:
                    return 0
                
            max_value_dict = max(week_messages, key=lambda item: value_to_minutes(item['value']))
            value = max_value_dict['value']
            
            grouped_conversations.append({
                "timestamp": f"{data[start_idx]['timestamp']} {week_end_date}",
                "value": value,
                "count": total_count
            })
    else:
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


    # Add the grouped conversations to the response dictionary
    response_dict["data_per_week"] = grouped_conversations
    return response_dict


def all_chatwoot_data(url,headers,params):
    # Initialize an empty dictionary to store the response data
    response_dict = {}
    # Make a GET request to the provided URL with headers and parameters
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    # Check if the selected metric requires special formatting
    metrics = ['avg_resolution_time','avg_first_response_time']
    if params['metric'] in metrics:
        # Format the data for metrics that need time-based representation
        for i in  data:
              # Convert timestamp to a datetime object
            date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
            avg_resolution_time_seconds = float(i['value'])
            # Convert average resolution time from seconds to days, hours, and minutes
            days = int(avg_resolution_time_seconds // 86400)
            hours = int((avg_resolution_time_seconds % 86400) // 3600)
            minutes = int((avg_resolution_time_seconds % 3600) // 60)

            # Format the value based on days and hours
            if days > 0:
                i['value'] = f"{str(days)} days {str(hours)} Hr {str(minutes)} min"
            else:
                i['value'] = f"{str(hours)} Hr {str(minutes)} min"

             # Format the timestamp to '%Y-%m-%d' format
            formatted_date = date_obj.strftime('%Y-%m-%d')
            i['timestamp'] = formatted_date
    else:
        # Format the timestamps for other metrics
        for i in  data:
            date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
            formatted_date = date_obj.strftime('%Y-%m-%d')
            i['timestamp'] = formatted_date

     # Add the formatted data to the response dictionary
    data = list(data) 
    response_dict["data_per_date"] = data
    return response_dict



def get_agents():
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
    return data
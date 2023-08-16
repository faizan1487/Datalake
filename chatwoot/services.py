import requests
import datetime
import math


def week_month_convos(url,headers,params):
    # response_dict = {}
    response_dict = week_chatwoot_data(url,headers,params)
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    # Calculate the number of weeks in the data
    months = len(data) // 30
    if len(data) % 30 > 0:
        months += 1

    # Initialize an empty list to store the grouped conversations
    grouped_conversations = []
    metrics = ['avg_resolution_time','avg_first_response_time']
    if params['metric'] in metrics:
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
            
            grouped_conversations.append({
                "timestamp": f"{data[start_idx]['timestamp']} {month_end_date}",
                "value": value,
                "count": total_count
            })
    else:
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
    return response_dict
    # print(grouped_conversations)


def week_chatwoot_data(url,headers,params):
    # Get conversations per date
    response_dict = {}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    metrics = ['avg_resolution_time','avg_first_response_time']
    if params['metric'] in metrics:
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
    metrics = ['avg_resolution_time','avg_first_response_time']
    if params['metric'] in metrics:
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



    response_dict["data_per_week"] = grouped_conversations
    return response_dict


def all_chatwoot_data(url,headers,params):
     # Get conversations per date
    response_dict = {}
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    metrics = ['avg_resolution_time','avg_first_response_time']
    if params['metric'] in metrics:
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
        for i in  data:
            date_obj = datetime.datetime.fromtimestamp(i['timestamp'])
            formatted_date = date_obj.strftime('%Y-%m-%d')
            i['timestamp'] = formatted_date
    # data_per_date
    data = list(data) 
    response_dict["data_per_date"] = data
    return response_dict
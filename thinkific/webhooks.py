from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from .serializers import ThinkificUserSerializer,ThinkificUserEnrollmentSerializer
from rest_framework import status
import json 
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.decorators import renderer_classes
from .models import Thinkific_User, Thinkific_Users_Enrollments
import csv
from user.models import AlNafi_User

@csrf_exempt
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def user_created_webhook(request):
    if(request.method != "POST"):
        return HttpResponse(status=400)
    
    data = request.body
    data_string = data.decode('utf-8')
    json_data = json.loads(data_string)
    # print(json_data)
    email = json_data['payload']['email']

    user = AlNafi_User.objects.filter(email=email).values('phone')
    if user:
        # print(user)
        # print(user[0]['phone'])
        # print(user.phone)
        json_data['payload']['phone'] = user[0]['phone']

    print(json_data)
    serializer = ThinkificUserSerializer(data=json_data['payload'])
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def formatdate(datestr):
    date_string=datestr
    substring = date_string[:19]
    new_substring = substring.replace('T', " ")
    return new_substring


@csrf_exempt
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def enrollment_created_webhook(request):
    if(request.method != "POST"):
        return HttpResponse(status=400)
    
    data = request.body
    data_string = data.decode('utf-8')
    json_data = json.loads(data_string)
    payload_data = json_data['payload']
    created_at = payload_data['created_at']
    if created_at == None:
        pass
    else:
        formatted_date = formatdate(created_at)
        payload_data['created_at'] = formatted_date
    
    expiry_date = payload_data['expiry_date']
    if expiry_date == None:
        pass
    else:
        formatted_date = formatdate(expiry_date)
        payload_data['expiry_date'] = formatted_date
        
    completed_at = payload_data['completed_at']
    if completed_at == None:
        pass
    else:
        formatted_date = formatdate(completed_at)
        payload_data['completed_at'] = formatted_date
        
    started_at = payload_data['started_at']
    if started_at == None:
        pass
    else:
        formatted_date = formatdate(started_at)
        payload_data['started_at'] = formatted_date
        
    activated_at = payload_data['activated_at']
    if activated_at == None:
        pass
    else:
        formatted_date = formatdate(activated_at)
        payload_data['activated_at'] = formatted_date
        
    
    updated_at = payload_data['updated_at']
    if updated_at == None:
        pass
    else:
        formatted_date = formatdate(updated_at)
        payload_data['updated_at'] = formatted_date
    
    payload_data['user_id'] = json_data['payload']['user']['id']
    payload_data['first_name'] = json_data['payload']['user']['first_name']
    payload_data['last_name'] = json_data['payload']['user']['last_name']
    payload_data['email'] = json_data['payload']['user']['email']
    payload_data['course_id'] = json_data['payload']['course']['id']
    payload_data['course_name'] = json_data['payload']['course']['name']
    del payload_data['user']
    del payload_data['course']
    serializer = ThinkificUserEnrollmentSerializer(data=payload_data)
    
    try:
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
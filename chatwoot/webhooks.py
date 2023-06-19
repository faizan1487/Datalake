from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from .serializers import ChatwootUserSerializer
from rest_framework import status
import json 
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.decorators import renderer_classes
from .models import ChatwoorUser
import csv


# @csrf_exempt
# @api_view(['POST'])
# @renderer_classes([JSONRenderer])
# def user_created_webhook(request):
#     print(request.method)
#     if(request.method != "POST"):
#         print("bad request")
#         return HttpResponse(status=400)
    
#     data = request.body
#     print("data",data)
#     data_string = data.decode('utf-8')
#     print("data string", data_string)
#     json_data = json.loads(data_string)
#     print("json_data",json_data)
#     payload_data = {}

#     payload_data['first_name'] = json_data['name']
#     payload_data['phone'] = json_data['phone_number']
#     payload_data['email'] = json_data['email']
#     # print(json_data['additional_attributes']['city'])
#     payload_data['city'] = json_data['additional_attributes']['city']
#     payload_data['country'] = json_data['additional_attributes']['country']

#     serializer = ChatwootUserSerializer(data=payload_data)
    
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     else:
#         print(serializer.errors)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def user_created_webhook(request):
    print(request.method)
    if request.method != "POST":
        print("bad request")
        return HttpResponse(status=400)
    
    data = request.body
    # print("data", data)
    data_string = data.decode('utf-8')
    # print("data string", data_string)
    json_data = json.loads(data_string)
    # print("json_data", json_data)
    # payload_data = {}
    # payload_data['first_name'] = json_data['name']
    # payload_data['phone'] = json_data['phone_number']
    # payload_data['email'] = json_data['email']
    # payload_data['city'] = json_data['additional_attributes']['city']
    # payload_data['country'] = json_data['additional_attributes']['country']

    payload_data = {
        'first_name': json_data['name'] if 'name' in json_data else None,
        'phone': json_data['phone_number'] if 'phone_number' in json_data else None,
        'email': json_data['email'] if 'email' in json_data else None,
        'city': json_data['additional_attributes']['city'] if 'additional_attributes' in json_data and 'city' in json_data['additional_attributes'] else None,
        'country': json_data['additional_attributes']['country'] if 'additional_attributes' in json_data and 'country' in json_data['additional_attributes'] else None
        }

    try:
        user = ChatwoorUser.objects.get(email=payload_data['email'])
        serializer = ChatwootUserSerializer(instance=user, data=payload_data)
    except ChatwoorUser.DoesNotExist:
        serializer = ChatwootUserSerializer(data=payload_data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
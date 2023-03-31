from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from .serializers import ThinkificUserSerializer
from rest_framework import status
import json 
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework.decorators import renderer_classes

@csrf_exempt
@api_view(['POST'])
@renderer_classes([JSONRenderer])
def user_created_webhook(request):
    if(request.method != "POST"):
        return HttpResponse(status=400)
    
    data = request.body
    data_string = data.decode('utf-8')
    json_data = json.loads(data_string)
    serializer = ThinkificUserSerializer(data=json_data['payload'])
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# @csrf_exempt
# def user_created_webhook(request):
#     # if(request.method != "POST"):
#     #     return HttpResponse(status=400)
#     data = request.body
#     # data_string = data.decode('utf-8')
#     # json_data = json.loads(data_string)
#     # serializer_data = json_data['payload']
#     # print(serializer_data)
#     serializer = ThinkificUserSerializer(data=data)
#     # print(serializer)
    
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




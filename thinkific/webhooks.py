from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from .serializers import ThinkificUserSerializer
from rest_framework import status
import json 


@csrf_exempt
def user_created_webhook(request):
    if(request.method != "POST"):
        return HttpResponse(status=400)
    data = request.body
    data_string = data.decode('utf-8')
    json_data = json.loads(data_string)
    serializer_data = json_data['payload']
    serializer = ThinkificUserSerializer(data=serializer_data)
    # print(serializer)
    
    if serializer.is_valid():
        # print("VAlid data" )
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # print("serializer not valid")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
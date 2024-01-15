from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from .models import Daily_lead
from rest_framework.response import Response
from .serializers import DailyLeadSerializer
from rest_framework import status

class DailyLead(APIView):
    def post(self, request):
        # print("in post")
        data = request.data
        # print(data)
        id = data.get('id')

        try:
            instance = Daily_lead.objects.filter(
                id=id
            )

            serializer = DailyLeadSerializer(instance.first(), data=data)
        except:
            serializer = DailyLeadSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self,request):
        data = request.data
        id = data.get('id')

        instance = Daily_lead.objects.filter(id=id)
        instance.delete()

        return Response("deleted")
from django.shortcuts import render
import requests
# Create your views here.
from rest_framework.views import APIView
from .models import Daily_lead, Daily_Sales_Support
from rest_framework.response import Response
from .serializers import DailyLeadSerializer, DailySalesSupportSerializer
from rest_framework import status

class DailyLead(APIView):
    def post(self, request):
        data = request.data
        id = data.get('id')
        # print("data", data)

        serializer = DailyLeadSerializer(data=data)
        if serializer.is_valid():
            # print(serializer)
            # print("is valid")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        data = request.data 
        id = data.get('id')
        # print("data", data)

        try:
            instance = Daily_lead.objects.get(id=id)
            serializer = DailyLeadSerializer(instance, data=data)
        except Daily_lead.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            # print("update is valid")
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        data = request.data
        id = data.get('id')

        try:
            instance = Daily_lead.objects.get(id=id)
            instance.delete()
            return Response("deleted")
        except Daily_lead.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    
class DailySalesSupport(APIView):
    def post(self, request):
        # print("in post")
        data = request.data
        print(data)
        id = data.get('id')
        serializer = DailySalesSupportSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request):
        data = request.data 
        id = data.get('id')
        # print("data", data)

        try:
            instance = Daily_Sales_Support.objects.get(id=id)
            serializer = DailySalesSupportSerializer(instance, data=data)
        except DailySalesSupportSerializer.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request):
        data = request.data
        # print("data", data)
        id = data.get('id')

        try:
            instance = Daily_Sales_Support.objects.get(id=id)
            # print(instance)
            instance.delete()
            # print("deleted")
            return Response("deleted")
        except Daily_Sales_Support.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
  


class ResaveLeadsAPIView(APIView):
    def get(self, request):
        # Retrieve leads with lead_creator as 'administrator'
        leads = Daily_Sales_Support.objects.all()

        # Iterate over the leads and re-save them
        for lead in leads:
            lead.save()
        return Response({"message": "Leads re-saved successfully."})
class MatchingId(APIView):
    def get(self, request):
        url = 'https://crm.alnafi.com/api/resource/Daily Sales Module?fields=["*"]&limit_start=0&limit_page_length=10000000'
        api_key = "4e7074f890507cb"
        api_secret = "c954faf5ff73d31"

        headers = {
            'Authorization': f'token {api_key}:{api_secret}',
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        response_get = requests.get(url, headers=headers)
        if response_get.status_code == 200:
            response_data = response_get.json()
            data = response_data.get('data', [])
            # print(len(data))
            all_daily_leads = Daily_lead.objects.all()

            for record in data:
                api_name = record.get('name')

                matching_ids = all_daily_leads.filter(id=api_name)
                if matching_ids.exists():
                    print(f"This is in my Model: {api_name}")
                else:
                    print(f"This is not there: {api_name}")

            return Response(response_data)
        else:
            return Response({'error': 'Failed to retrieve data from the API'}, status=response_get.status_code)
        
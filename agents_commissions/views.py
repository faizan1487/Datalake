from django.shortcuts import render

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
        # print(data)
        id = data.get('id')

        try:
            instance = Daily_Sales_Support.objects.filter(
                id=id
            )

            serializer = DailySalesSupportSerializer(instance.first(), data=data)
        except:
            serializer = DailySalesSupportSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request):
        data = request.data
        # print("data", data)
        id = data.get('id')

        try:
            instance = Daily_Sales_Support.objects.get(id=id)
            instance.delete()
            # print("Deleted")
            return Response("Deleted", status=status.HTTP_204_NO_CONTENT)
        except Daily_Sales_Support.DoesNotExist:
            return Response("Not Found", status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # print(f"Error: {e}")
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
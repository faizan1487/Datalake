import email
import re
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
import requests
import environ 

env = environ.Env()
env.read_env()

# Create your views here.
class LiveCoupons(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # q = self.request.GET.get('q', None) or None
        url="https://content-service.alnafi.edu.pk/api/coupons-data/?populate=*"
        
        params = {
            'populate': "*"
        }

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            # Assuming the response is actually JSON (check content-type header if unsure)
            json_data = response.json()

            return Response(json_data)
        else:
            return Response("Error")
        


class CouponUsers(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        coupon = request.GET.get('coupon')
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)
        export = request.GET.get('export',None)
        page= request.GET.get('page')
        url = env('PAYMENT_SERVICE_COUPON_URL_PROD')
        params = {
            'coupon': coupon,
            'start_date': start_date,
            'end_date': end_date,
            'page': page,
            'export':export
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raise an exception for non-200 status codes
            data = response.json()
            return Response(data)
        except requests.exceptions.RequestException as e:
            if response.status_code == 500:
                return Response({'message': 'Internal server error occurred. Please try again later.'}, status=500)
            else:
                # Handle other types of request exceptions
                return Response({'message': f'An error occurred: {str(e)}'}, status=response.status_code)
import email
import re
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
import requests

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
            'Authorization': 'Bearer 4ebc2c82f4e716d05b64a3eb274b64bf5a60a66397e7b5a4ac7f2c99a6bacefb9cc7b2e2997e9532dac38adfa651990be1bdd89cf51a2d5dd131132ac6e6023daeeca9b690b8df0ed32f18fd9b3f23a89eb173d4d0181c02975b498f847f8d1c66a53cf120a6308f05c431dc115322cc9784e9b6f005c099f8367bfa35987e4b',
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
        coupon = request.GET.get('coupon', None)
        # url=f"http://127.0.0.1:8001/payments/coupon-users"
        url="https://stage-payment-service.alnafi.edu.pk/payments/coupon-users/"

  
        params = {
            'coupon': coupon
        }
        response = requests.get(url,params=params)

        data = response.json()

        return Response(data)
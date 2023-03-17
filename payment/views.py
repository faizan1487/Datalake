from django.shortcuts import render
from .models import Payment
from .serializer import PaymentSerializer, Easypaisa_PaymentsSerializer, Ubl_Ipg_PaymentsSerializer
from .services import easypaisa_payment, stripe_payment, ubl_payment
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class GetUserDetails(APIView):

    def post(self,request):
        email = request.data['email']
        
        easypaisa_obj = easypaisa_payment(email)
        easypaisa_serializer = Easypaisa_PaymentsSerializer(easypaisa_obj,many=True)
        
        stripe_obj = stripe_payment(email)
        stripe_serializer = PaymentSerializer(stripe_obj,many=True)
        
        ubl_obj = ubl_payment(email)
        ubl_serializer = Ubl_Ipg_PaymentsSerializer(ubl_obj,many=True)
        
        data = {
            'easypaisa': easypaisa_serializer.data,
            'stripe': stripe_serializer.data,
            'ubl': ubl_serializer.data
        }
        
        return Response(data)
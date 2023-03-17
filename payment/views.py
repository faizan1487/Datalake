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
        source = request.data['source']
        
        if source == 'easypaisa':
            obj = easypaisa_payment(email)
            serializer = Easypaisa_PaymentsSerializer(obj,many=True)
        elif source == 'stripe':
            obj = stripe_payment(email)
            serializer = PaymentSerializer(obj,many=True)
        else:
            print('ubl')
            obj = ubl_payment(email)
            serializer = Ubl_Ipg_PaymentsSerializer(obj,many=True)
            
            
        # obj = Payment.objects.filter(email=email,source=source)
        print(obj)
        # serializer = Easypaisa_PaymentsSerializer(obj,many=True)
        return Response(serializer.data)
    
    
    
    
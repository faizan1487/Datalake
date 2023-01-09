from django.shortcuts import render
from .models import Payment
from .serializer import PaymentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
class GetUserDetails(APIView):

    def post(self,request):
        email = request.data['email']
        source = request.data['source']

        obj = Payment.objects.filter(email=email,payment_source=source)
        print(obj)
        serializer = PaymentSerializer(obj,many=True)
        return Response(serializer.data)


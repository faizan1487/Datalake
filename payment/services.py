from django.shortcuts import render
from .models import Payment, Easypaisa_Payment, UBL_IPG_Payment
from .serializer import PaymentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response



def easypaisa_payment(email):
    obj = Easypaisa_Payment.objects.filter(customer_email=email)
    return obj


def stripe_payment(email):
    obj = Payment.objects.filter(email=email)
    return obj


def ubl_payment(email):
    obj = UBL_IPG_Payment.objects.filter(customer_email=email)
    return obj
from django.shortcuts import render
from .models import Payment, Easypaisa_Payment, UBL_IPG_Payment
from .serializer import PaymentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from datetime import date, datetime, time


def easypaisa_payment(email):
    obj = Easypaisa_Payment.objects.filter(customer_email=email)
    return obj
def stripe_payment(email):
    obj = Payment.objects.filter(email=email)
    return obj
def ubl_payment(email):
    obj = UBL_IPG_Payment.objects.filter(customer_email=email)
    return obj


def easypaisa_pay(q,start_date, end_date):
    if start_date:
        pass
    else:
        first_payment = Easypaisa_Payment.objects.first()
        start_date = first_payment.order_datetime
        
    if end_date:
        pass
    else:
        last_payment = Easypaisa_Payment.objects.last()
        start_date = last_payment.order_datetime
        
    end_datetime = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d'), time.max)
    queryset = Easypaisa_Payment.objects.filter(
        Q(customer_email__icontains=q) | Q(product_name__icontains=q)
        |Q(order_id__iexact=q), 
        Q(order_datetime__gte = start_date) & Q(order_datetime__lte = end_datetime)
        )
    return queryset

def stripe_pay(q,start_date,end_date):
    if start_date:
        pass
    else:
        first_payment = Payment.objects.first()
        start_date = first_payment.order_datetime
        
    if end_date:
        pass
    else:
        last_payment = Payment.objects.last()
        end_date = last_payment.order_datetime
        
        end_datetime = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d'), time.max)
        queryset = Payment.objects.filter(
            Q(email__icontains=q) | Q(product__icontains=q)
            |Q(payment_id__iexact=q),
            Q(created__gte=start_date) & Q(created__lte=end_datetime)
            )
    return queryset


def ubl_pay(q,start_date,end_date):
    if start_date:
        pass
    else:
        first_payment = UBL_IPG_Payment.objects.first()
        start_date = first_payment.order_datetime
        
    if end_date:
        end_datetime = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d'), time.max)
        queryset = UBL_IPG_Payment.objects.filter(
            Q(customer_email__icontains=q) | Q(product_name__icontains=q)
            |Q(order_id__iexact=q),
            Q(order_datetime__gte=start_date) & Q(order_datetime__lte=end_datetime)
            )
    else:
        last_payment = UBL_IPG_Payment.objects.last()
        end_date = last_payment.order_datetime
 
        end_datetime = datetime.combine(datetime.strptime(end_date, '%Y-%m-%d'), time.max)
        queryset = UBL_IPG_Payment.objects.filter(
            Q(customer_email__icontains=q) | Q(product_name__icontains=q)
            |Q(order_id__iexact=q),
            Q(order_datetime__gte=start_date) & Q(order_datetime__lte=end_datetime)
            )
    return queryset
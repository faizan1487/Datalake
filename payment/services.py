from django.shortcuts import render
from .models import Stripe_Payment, Easypaisa_Payment, UBL_IPG_Payment
from .serializer import StripePaymentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from datetime import date, datetime, time, timedelta

def stripe_pay(q, start_date, end_date, source):
    if start_date:
        pass
    else:
        first_payment = Stripe_Payment.objects.last()
        date_time_obj = first_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")                                                                                      
        start_date = new_date_obj + timedelta(days=20)      
    if end_date:
        pass
    else:
        pass
        last_payment = Stripe_Payment.objects.first()
        date_time_obj = last_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")      
        end_date = new_date_obj - timedelta(days=20)  
    if source:
        pass
    else:
        source = ""      
    if q:
        queryset = Stripe_Payment.objects.filter(
            Q(customer_email__iexact=q) | Q(name__icontains=q)
            |Q(payment_id__iexact=q))
        query_time = queryset.filter(Q(order_datetime__date__gte = start_date) & Q(order_datetime__date__lte = end_date))
    else:
        queryset = Stripe_Payment.objects.all()
        query_time = queryset.filter(Q(order_datetime__date__gte = start_date) & Q(order_datetime__date__lte = end_date))     
    return query_time

def easypaisa_pay(q, start_date, end_date, source):
    if start_date:
        pass
    else:
        first_payment = Easypaisa_Payment.objects.last()
        date_time_obj = first_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")                                                                                    
        start_date = new_date_obj + timedelta(days=20)       
    if end_date:
        pass
    else:
        last_payment = Easypaisa_Payment.objects.first()
        date_time_obj = last_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")
        end_date = new_date_obj - timedelta(days=20)
    if source:
        pass
    else:
        source = ""
    
    if q:
        queryset = Easypaisa_Payment.objects.filter(
            Q(customer_email__iexact=q) | Q(product_name__icontains=q)
            |Q(order_id__iexact=q))
        query_time = queryset.filter(Q(order_datetime__date__lte = end_date) & Q(order_datetime__date__gte = start_date))
    else:
        queryset = Easypaisa_Payment.objects.all()
        query_time = queryset.filter(Q(order_datetime__date__lte = end_date) & Q(order_datetime__date__gte = start_date))
        
    return query_time

def ubl_pay(q, start_date, end_date, source):
    if start_date==None:
        first_payment = UBL_IPG_Payment.objects.last()
        start_date = first_payment.order_datetime + timedelta(days=20) 
    else:
        pass  
        
    if end_date==None:
        last_payment = UBL_IPG_Payment.objects.first()
        end_date = last_payment.order_datetime - timedelta(days=20)
    else:
        pass
    
    print(start_date)
    print(end_date)
    
    if source:
        pass
    else:
        source = ""  
    
    
    if q:
        queryset = UBL_IPG_Payment.objects.filter(
            Q(customer_email__iexact=q) | Q(product_name__icontains=q)
            |Q(order_id__iexact=q))
        time_query = queryset.filter(Q(order_datetime__date__lte=end_date) & Q(order_datetime__date__gte=start_date))
    else:
        queryset = UBL_IPG_Payment.objects.all()
        time_query = queryset.filter(Q(order_datetime__date__lte=end_date) & Q(order_datetime__date__gte=start_date))
    return time_query
from django.shortcuts import render
from .models import Stripe_Payment, Easypaisa_Payment, UBL_IPG_Payment,AlNafi_Payment
from .serializer import StripePaymentSerializer, Ubl_Ipg_PaymentsSerializer, Easypaisa_PaymentsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from datetime import date, datetime, time, timedelta
import pandas as pd
from django.conf import settings
import os
import shutil

def json_to_csv(serialized_data,name):
    file_name = f"{name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    # Build the full path to the media directory
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    pd.DataFrame(serialized_data.data).to_csv(file_path, index=False)
    return file_path

def stripe_no_payments(start_date,end_date):
    if start_date:
        pass
    else:
        first_payment = Stripe_Payment.objects.last()
        date_time_obj = first_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")                                                                                      
        start_date = str(new_date_obj.date())    
    if end_date:
        pass
    else:
        pass
        last_payment = Stripe_Payment.objects.first()
        date_time_obj = last_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")      
        end_date = str(new_date_obj.date())
         
    
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()       
    delta = end_date_obj - start_date_obj
    dates = []
    for i in range(delta.days + 1):
        date = start_date_obj + timedelta(days=i)
        dates.append(date)
        
    payments = Stripe_Payment.objects.filter(order_datetime__date__in=dates)
    payment_dict = {}
    for payment in payments:
        if payment.order_datetime.date() in payment_dict:
            payment_dict[payment.order_datetime.date()].append(payment)
        else:
            payment_dict[payment.order_datetime.date()] = [payment]
            
    response_data = []
    for date in dates:
        if date in payment_dict:
            payments_for_date = payment_dict[date]
            serialized_payments = StripePaymentSerializer(payments_for_date, many=True).data
        else:
            serialized_payments = []

        response_data.append({
            'date': date,
            'payments': len(serialized_payments)
        })
    return response_data

def ubl_no_payments(start_date,end_date):
    if start_date:
        pass
    else:
        first_payment = UBL_IPG_Payment.objects.last()
        date_time_obj = first_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")                                                                                      
        start_date = str(new_date_obj.date())    
    if end_date:
        pass
    else:
        pass
        last_payment = UBL_IPG_Payment.objects.first()
        date_time_obj = last_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")      
        end_date = str(new_date_obj.date())
         
    
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()       
    delta = end_date_obj - start_date_obj
    dates = []
    for i in range(delta.days + 1):
        date = start_date_obj + timedelta(days=i)
        dates.append(date)
        
    payments = UBL_IPG_Payment.objects.filter(order_datetime__date__in=dates)
    payment_dict = {}
    for payment in payments:
        if payment.order_datetime.date() in payment_dict:
            payment_dict[payment.order_datetime.date()].append(payment)
        else:
            payment_dict[payment.order_datetime.date()] = [payment]
            
    response_data = []
    for date in dates:
        if date in payment_dict:
            payments_for_date = payment_dict[date]
            serialized_payments = Ubl_Ipg_PaymentsSerializer(payments_for_date, many=True).data
        else:
            serialized_payments = []

        response_data.append({
            'date': date,
            'payments': len(serialized_payments)
        })
    return response_data
    
def easypaisa_no_payments(start_date,end_date):
    if start_date:
        pass
    else:
        first_payment = Easypaisa_Payment.objects.last()
        date_time_obj = first_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")                                                                                      
        start_date = str(new_date_obj.date())    
    if end_date:
        pass
    else:
        pass
        last_payment = Easypaisa_Payment.objects.first()
        date_time_obj = last_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")      
        end_date = str(new_date_obj.date())
         
    
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()       
    delta = end_date_obj - start_date_obj
    dates = []
    for i in range(delta.days + 1):
        date = start_date_obj + timedelta(days=i)
        dates.append(date)
        
    payments = Easypaisa_Payment.objects.filter(order_datetime__date__in=dates)
    payment_dict = {}
    for payment in payments:
        if payment.order_datetime.date() in payment_dict:
            payment_dict[payment.order_datetime.date()].append(payment)
        else:
            payment_dict[payment.order_datetime.date()] = [payment]
            
    response_data = []
    for date in dates:
        if date in payment_dict:
            payments_for_date = payment_dict[date]
            serialized_payments = Easypaisa_PaymentsSerializer(payments_for_date, many=True).data
        else:
            serialized_payments = []

        response_data.append({
            'date': date,
            'payments': len(serialized_payments)
        })
    return response_data


def no_of_payments(start_date,end_date,queryset):
    if start_date:
        pass
    else:
        first_payment = AlNafi_Payment.objects.last()
        date_time_obj = first_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")                                                                                      
        start_date = str(new_date_obj.date())    
    if end_date:
        pass
    else:
        pass
        last_payment = AlNafi_Payment.objects.first()
        date_time_obj = last_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")      
        end_date = str(new_date_obj.date())
    
    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()       
    delta = end_date_obj - start_date_obj
    dates = []
    for i in range(delta.days + 1):
        date = start_date_obj + timedelta(days=i)
        dates.append(date)
    
    if queryset:
        payments = queryset.filter(order_datetime__date__in=dates)    
    else:
        payments = AlNafi_Payment.objects.filter(order_datetime__date__in=dates)
    payment_dict = {}
    for payment in payments:
        if payment.order_datetime.date() in payment_dict:
            payment_dict[payment.order_datetime.date()].append(payment)
        else:
            payment_dict[payment.order_datetime.date()] = [payment]
            
    response_data = []
    for date in dates:
        if date in payment_dict:
            payments_for_date = payment_dict[date]
            serialized_payments = Easypaisa_PaymentsSerializer(payments_for_date, many=True).data
        else:
            serialized_payments = []

        response_data.append({
            'date': date,
            'payments': len(serialized_payments)
        })
    return response_data
    
def stripe_pay(q, start_date, end_date):
    if start_date:
        pass
    else:
        first_payment = Stripe_Payment.objects.last()
        date_time_obj = first_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")                                                                                      
        start_date = new_date_obj      
    if end_date:
        pass
    else:
        pass
        last_payment = Stripe_Payment.objects.first()
        date_time_obj = last_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")      
        end_date = new_date_obj
          
    if q:
        queryset = Stripe_Payment.objects.filter(
            Q(customer_email__iexact=q) | Q(name__icontains=q)
            |Q(payment_id__iexact=q))
        query_time = queryset.filter(Q(order_datetime__date__gte = start_date) & Q(order_datetime__date__lte = end_date))
    else:
        queryset = Stripe_Payment.objects.all()
        query_time = queryset.filter(Q(order_datetime__date__gte = start_date) & Q(order_datetime__date__lte = end_date))     
    return query_time

def easypaisa_pay(q, start_date, end_date):
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
    
    if q:
        queryset = Easypaisa_Payment.objects.filter(
            Q(customer_email__iexact=q) | Q(product_name__icontains=q)
            |Q(order_id__iexact=q))
        query_time = queryset.filter(Q(order_datetime__date__lte = end_date) & Q(order_datetime__date__gte = start_date))
    else:
        queryset = Easypaisa_Payment.objects.all()
        query_time = queryset.filter(Q(order_datetime__date__lte = end_date) & Q(order_datetime__date__gte = start_date))
    
    return query_time

def ubl_pay(q, start_date, end_date):
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
    
    if q:
        queryset = UBL_IPG_Payment.objects.filter(
            Q(customer_email__iexact=q) | Q(product_name__icontains=q)
            |Q(order_id__iexact=q))
        time_query = queryset.filter(Q(order_datetime__date__lte=end_date) & Q(order_datetime__date__gte=start_date))
    else:
        queryset = UBL_IPG_Payment.objects.all()
        time_query = queryset.filter(Q(order_datetime__date__lte=end_date) & Q(order_datetime__date__gte=start_date))
    return time_query
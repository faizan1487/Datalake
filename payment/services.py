from django.shortcuts import render
from .models import Stripe_Payment, Easypaisa_Payment, UBL_IPG_Payment,AlNafi_Payment, Main_Payment
from .serializer import StripePaymentSerializer, Ubl_Ipg_PaymentsSerializer, Easypaisa_PaymentsSerializer,MainPaymentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.db.models import Q
from datetime import date, datetime, time, timedelta
import pandas as pd
from django.conf import settings
import os
import shutil
from products.models import Alnafi_Product, Main_Product
from django.db.models import F, Max, Q
from django.core.exceptions import ObjectDoesNotExist


def json_to_csv(serialized_data,name):
    file_name = f"{name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    # Build the full path to the media directory
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    pd.DataFrame(serialized_data.data).to_csv(file_path, index=False)
    return file_path


def main_no_of_payments(start_date,end_date,source):
    payments = Main_Payment.objects.all()
    if source:
        payments = payments.filter(source=source)
        
    if not start_date:
        if payments:
            first_payment = payments.exclude(order_datetime=None).last()
            date_time_obj = first_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
            new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")                                                                                    
            start_date = new_date_obj + timedelta(days=20)       
    if not end_date:
        if payments:
            last_payment = payments.exclude(order_datetime=None).first()
            date_time_obj = last_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
            new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")
            end_date = new_date_obj - timedelta(days=20)
               
    delta = end_date - start_date
    dates = []
    for i in range(delta.days + 1):
        date = start_date + timedelta(days=i)
        dates.append(date)
        
    payments = payments.filter(order_datetime__date__in=dates)
    payment_dict = {}
    for payment in payments:
        if payment.order_datetime.date() in payment_dict:
            payment_dict[payment.order_datetime.date()].append(payment)
        else:
            payment_dict[payment.order_datetime.date()] = [payment]

    response_data = []
    for date in dates:
        if date.date() in payment_dict:
            payments_for_date = payment_dict[date.date()]
            serialized_payments = MainPaymentSerializer(payments_for_date, many=True).data
        else:
            serialized_payments = []

        response_data.append({
            'date': date.date(),
            'payments': len(serialized_payments)
        })
    
    return response_data


def stripe_no_payments(start_date,end_date):
    if not start_date:
        first_payment = Stripe_Payment.objects.exclude(order_datetime=None).last()
        date_time_obj = first_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")                                                                                      
        start_date = str(new_date_obj.date()) 
           
    if not end_date:
        last_payment = Stripe_Payment.objects.exclude(order_datetime=None).first()
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
    if not start_date:
        first_payment = UBL_IPG_Payment.objects.exclude(order_datetime=None).last()
        date_time_obj = first_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")                                                                                      
        start_date = str(new_date_obj.date())    
    if not end_date:
        last_payment = UBL_IPG_Payment.objects.exclude(order_datetime=None).first()
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
    if not start_date:
        first_payment = Easypaisa_Payment.objects.exclude(order_datetime=None).last()
        date_time_obj = first_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")                                                                                      
        start_date = str(new_date_obj.date())    
    if not end_date:
        last_payment = Easypaisa_Payment.objects.exclude(order_datetime=None).first()
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


def no_of_payments(start_date,end_date,payments):
    if not start_date:
        first_payment = payments.exclude(order_datetime=None).last()
        date_time_obj = first_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")                                                                                      
        start_date = str(new_date_obj.date())    
    if not end_date:
        last_payment = payments.exclude(order_datetime=None).first()
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
    
    if payments:
        payments = payments.filter(order_datetime__date__in=dates)    
    else:
        payments = Main_Payment.objects.filter(order_datetime__date__in=dates)
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
            serialized_payments = MainPaymentSerializer(payments_for_date, many=True).data
        else:
            serialized_payments = []

        response_data.append({
            'date': date,
            'payments': len(serialized_payments)
        })
    return response_data
    
def stripe_pay(q, start_date, end_date,plan,product):
    if not start_date:
        first_payment = Stripe_Payment.objects.exclude(order_datetime=None).last()
        date_time_obj = first_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")                                                                                      
        start_date = new_date_obj      
    if not end_date:
        last_payment = Stripe_Payment.objects.exclude(order_datetime=None).first()
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
        
    if product:
        query_time = query_time.filter(product_name__icontains=product)
    
    
    payment_plan = []
    payment_cycle = []
    for obj in query_time:
        product = Alnafi_Product.objects.filter(name=obj.product_name)
        # print(product)
        if plan == 'yearly':
            for i in product:
                if i.plan:
                    if i.plan == 'Yearly':
                        payment_plan.append(obj)
                        payment_cycle.append('Yearly')
        elif plan == 'halfyearly':
            for i in product:
                if i.plan:
                    if i.plan == 'Half Yearly':
                        payment_plan.append(obj)
                        payment_cycle.append('Half yearly')
        elif plan == 'quarterly':           
            for i in product:
                if i.plan:
                    if i.plan == 'Quarterly':
                        payment_plan.append(obj)
                        payment_cycle.append('Quarterly')
        elif plan == 'monthly':           
            for i in product:
                if i.plan:
                    if i.plan == 'Monthly':
                        payment_plan.append(obj)
                        payment_cycle.append('Monthly')
        else:
            for i in product:
                if i.plan:
                    if i.plan == 'Yearly':
                        payment_plan.append(obj)
                        payment_cycle.append('Yearly')
                    if i.plan == 'Half Yearly':
                        payment_plan.append(obj)
                        payment_cycle.append('Half yearly')
                    if i.plan == 'Quarterly':
                        payment_plan.append(obj)
                        payment_cycle.append('Quarterly')
                    if i.plan == 'Monthly':
                        payment_plan.append(obj)
                        payment_cycle.append('Monthly')
                        
    query_time = payment_plan   
    response_data = {"data":query_time,
                        "payment_cycle":payment_cycle}            
    return response_data



def search_payment(export, query, start_date, end_date, plan, request, url, product, source, origin):
    payments = Main_Payment.objects.all()
    print("payments count", payments.count())
    if origin:
        if origin == 'local':
            payments = payments.filter(source__in=['Easypaisa', 'UBL_IPG'])
        else:
            payments = payments.filter(source='stripe')

    if source:
        payments = payments.filter(source=source.capitalize())
    print("payments count", payments.count())
    if not start_date:
        first_payment = payments.exclude(order_datetime=None).last()
        start_date = first_payment.order_datetime + timedelta(days=20) if first_payment else None

    if not end_date:
        last_payment = payments.exclude(order_datetime=None).first()
        end_date = last_payment.order_datetime - timedelta(days=20) if last_payment else None

    if query:
        payments = payments.filter(
            Q(user__email__iexact=query) | Q(product__product_name__iexact=query))
        payments = payments.filter(Q(order_datetime__date__lte=end_date) & Q(order_datetime__date__gte=start_date))

    if product:
        product_obj = Main_Product.objects.get(product_name=product)
        # print(product_obj.product_payments)
        payments = product_obj.product_payments.filter(Q(order_datetime__date__lte=end_date) & Q(order_datetime__date__gte=start_date))

    if plan:
        if plan == 'yearly':
            payments = payments.filter(product__product_plan='Yearly')
        elif plan == 'halfyearly':
            payments = payments.filter(product__product_plan='Half Yearly')
        elif plan == 'quarterly':
            payments = payments.filter(product__product_plan='Quarterly')
        elif plan == 'monthly':
            payments = payments.filter(product__product_plan='Monthly')

    payment_cycle = payments.values_list('product__product_plan', flat=True).distinct()
    response_data = {"payments": payments, "payment_cycle": payment_cycle}

    return response_data


def easypaisa_pay(q,start_date,end_date,plan,product):
    if not start_date:
        first_payment = Easypaisa_Payment.objects.exclude(order_datetime=None).last()
        date_time_obj = first_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")                                                                                    
        start_date = new_date_obj + timedelta(days=20)       
    if not end_date:
        last_payment = Easypaisa_Payment.objects.exclude(order_datetime=None).first()
        date_time_obj = last_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")
        end_date = new_date_obj - timedelta(days=20)
    
    if q:
        queryset = Easypaisa_Payment.objects.filter(
            Q(customer_email__iexact=q) | Q(order_id__iexact=q))
        query_time = queryset.filter(Q(order_datetime__date__lte = end_date) & Q(order_datetime__date__gte = start_date))
    else:
        queryset = Easypaisa_Payment.objects.all()
        query_time = queryset.filter(Q(order_datetime__date__lte = end_date) & Q(order_datetime__date__gte = start_date))
    
    if product:
        query_time = query_time.filter(product_name__icontains=product)
    
    payment_plan = []
    payment_cycle = []
    for obj in query_time:
        product = Alnafi_Product.objects.filter(name=obj.product_name)
        if plan == 'yearly':
            for i in product:
                if i.plan:
                    if i.plan == 'Yearly':
                        payment_plan.append(obj)
                        payment_cycle.append('Yearly')
        elif plan == 'halfyearly':
            for i in product:
                if i.plan:
                    if i.plan == 'Half Yearly':
                        payment_plan.append(obj)
                        payment_cycle.append('Half yearly')
        elif plan == 'quarterly':           
            for i in product:
                if i.plan:
                    if i.plan == 'Quarterly':
                        payment_plan.append(obj)
                        payment_cycle.append('Quarterly')
        elif plan == 'monthly':           
            for i in product:
                if i.plan:
                    if i.plan == 'Monthly':
                        payment_plan.append(obj)
                        payment_cycle.append('Monthly')
        else:
            for i in product:
                if i.plan:
                    if i.plan == 'Yearly':
                        payment_plan.append(obj)
                        payment_cycle.append('Yearly')
                    if i.plan == 'Half Yearly':
                        payment_plan.append(obj)
                        payment_cycle.append('Half yearly')
                    if i.plan == 'Quarterly':
                        payment_plan.append(obj)
                        payment_cycle.append('Quarterly')
                    if i.plan == 'Monthly':
                        payment_plan.append(obj)
                        payment_cycle.append('Monthly')
    
                        
    query_time = payment_plan   
        
    response_data = {"data":query_time,
                        "payment_cycle":payment_cycle}        
    return response_data

def ubl_pay(q, start_date, end_date,plan,product):
    if not start_date:
        first_payment = UBL_IPG_Payment.objects.exclude(order_datetime=None).last()
        start_date = first_payment.order_datetime + timedelta(days=20) 
        
    if not end_date:
        last_payment = UBL_IPG_Payment.objects.exclude(order_datetime=None).first()
        end_date = last_payment.order_datetime - timedelta(days=20)
    
    if q:
        queryset = UBL_IPG_Payment.objects.filter(
            Q(customer_email__iexact=q)|Q(order_id__iexact=q))
        query_time = queryset.filter(Q(order_datetime__date__lte=end_date) & Q(order_datetime__date__gte=start_date))
    else:
        queryset = UBL_IPG_Payment.objects.all()
        query_time = queryset.filter(Q(order_datetime__date__lte=end_date) & Q(order_datetime__date__gte=start_date))
       
    if product:
        query_time = query_time.filter(product_name__icontains=product)
    
    payment_plan = []
    payment_cycle = []
    for obj in query_time:
        product = Alnafi_Product.objects.filter(name=obj.product_name)
        if plan == 'yearly':
            for i in product:
                if i.plan:
                    if i.plan == 'Yearly':
                        payment_plan.append(obj)
                        payment_cycle.append('Yearly')
        elif plan == 'halfyearly':
            for i in product:
                if i.plan:
                    if i.plan == 'Half Yearly':
                        payment_plan.append(obj)   
                        payment_cycle.append('Half yearly')                
        elif plan == 'quarterly':           
            for i in product:
                if i.plan:
                    if i.plan == 'Quarterly':
                        payment_plan.append(obj) 
                        payment_cycle.append('Quarterly')                                 
        elif plan == 'monthly':           
            for i in product:
                if i.plan:
                    if i.plan == 'Monthly':
                        payment_plan.append(obj)
                        payment_cycle.append('Monthly')  
        else:
            for i in product:
                if i.plan:
                    if i.plan == 'Yearly':
                        payment_plan.append(obj)
                        payment_cycle.append('Yearly')
                    if i.plan == 'Half Yearly':
                        payment_plan.append(obj)
                        payment_cycle.append('Half yearly')
                    if i.plan == 'Quarterly':
                        payment_plan.append(obj)
                        payment_cycle.append('Quarterly')
                    if i.plan == 'Monthly':
                        payment_plan.append(obj)
                        payment_cycle.append('Monthly')
                        
    query_time = payment_plan  
    response_data = {"data":query_time,
                        "payment_cycle":payment_cycle}
        
    return response_data






# def payment_validation(time_threshold_str, q, source):
#     payments = Main_Payment.objects.all().select_related('product')

#     if source:
#         payments = payments.filter(source=source)

#     if q:
#         payments = payments.filter(customer_email__iexact=q)

#     response = {"payments": None, "valid_payments": []}
#     if payments:
#         validated_payments = []
#         valid_payments = []

#         product_ids = set(payments.values_list('product_id', flat=True))
#         products = Main_Product.objects.filter(id__in=product_ids).values('id', 'amount_pkr', 'product_plan')

#         alnafi_payments = payments.filter(source='Al-Nafi').order_by('-order_datetime').prefetch_related('user', 'product')

#         latest_payments = {}
#         for payment in alnafi_payments:
#             key = (payment.user_id, payment.product_id)
#             if key not in latest_payments:
#                 latest_payments[key] = payment

#         for payment in payments:
#             valid_payment = False

#             try:
#                 product = next(filter(lambda p: p['id'] == payment.product_id, products), None)

#                 if product and product['amount_pkr'] == payment.amount:
#                     valid_payment = True

#                 latest_payment = latest_payments.get((payment.user_id, payment.product_id))

#                 if latest_payment:
#                     tolerance = timedelta(days=1)
#                     if (payment.order_datetime.date() - tolerance <= latest_payment.order_datetime.date() <= payment.order_datetime.date() + tolerance):
#                         valid_payment = True

#                 if product:
#                     if product['product_plan'] == 'Yearly':
#                         tolerance = timedelta(days=15)
#                         if latest_payment:
#                             expiry_date = latest_payment.expiration_datetime.date()
#                             expected_expiry = latest_payment.order_datetime.date() + timedelta(days=380) - tolerance

#                             if expected_expiry <= expiry_date <= (latest_payment.order_datetime.date() + timedelta(days=380) + tolerance):
#                                 valid_payment = True

#                     if product['product_plan'] == 'Half Yearly':
#                         if latest_payment:
#                             tolerance = timedelta(days=10)
#                             expiry_date = latest_payment.expiration_datetime.date()
#                             expected_expiry = latest_payment.order_datetime.date() + timedelta(days=180) - tolerance

#                             if expected_expiry <= expiry_date <= (latest_payment.order_datetime.date() + timedelta(days=180) + tolerance):
#                                 valid_payment = True

#                     if product['product_plan'] == 'Quarterly':
#                         if latest_payment:
#                             tolerance = timedelta(days=7)
#                             expiry_date = latest_payment.expiration_datetime.date()
#                             expected_expiry = latest_payment.order_datetime.date() + timedelta(days=90) - tolerance

#                             if expected_expiry <= expiry_date <= (latest_payment.order_datetime.date() + timedelta(days=90) + tolerance):
#                                 valid_payment = True

#                     if product['product_plan'] == 'Monthly':
#                         if latest_payment:
#                             tolerance = timedelta(days=5)
#                             expiry_date = latest_payment.expiration_datetime.date()
#                             expected_expiry = latest_payment.order_datetime.date() + timedelta(days=30) - tolerance

#                             if expected_expiry <= expiry_date <= (latest_payment.order_datetime.date() + timedelta(days=30) + tolerance):
#                                 valid_payment = True

#             except ObjectDoesNotExist:
#                 pass

#             validated_payments.append(payment)
#             valid_payments.append(valid_payment)

#         serializer = MainPaymentSerializer(validated_payments, many=True)
#         for i in range(len(serializer.data)):
#             serializer.data[i]['is_valid_payment'] = valid_payments[i]

#         response["payments"] = serializer.data

#     else:
#         response["payments"] = MainPaymentSerializer(payments, many=True).data

#     return response


def ubl_payment_validation(time_threshold_str,q):
    ubl_pay = UBL_IPG_Payment.objects.filter(order_datetime__date__gte=time_threshold_str)
    if q:
        ubl_pay = ubl_pay.filter(customer_email__iexact=q)
    
    ubl_payments = []
    valid_payments = []
    if ubl_pay:
        for obj in ubl_pay:
            valid_payment = True
            ubl_payments.append(obj)
            alnafi_product = Alnafi_Product.objects.filter(name=obj.product_name)
            
            
            if alnafi_product:
                if alnafi_product[0].amount_pkr == obj.amount:
                    valid_payment = True
            
            #Get the latest alnafi payment
            alnafi_payment = list(AlNafi_Payment.objects.filter(customer_email=obj.customer_email))
            if alnafi_payment:
                if obj.product_name == alnafi_payment[0].product_name:
                    valid_payment = True
                else:
                    valid_payment = False
                    # print("obj id", obj.id)
                    # print("false product name")
                    # print("obj.product_name",obj.product_name)
                    # print("alnafi_payment[0].product_name",alnafi_payment[0].product_name)
                
                tolerance = timedelta(days=1)
                if obj['order_datetime'].date()>=alnafi_payment[0].order_datetime.date() - tolerance and obj.order_datetime.date()<=alnafi_payment[0].order_datetime.date() + tolerance:
                    valid_payment = True
                else:
                    valid_payment = False
                    # print("obj id", obj.id)
                    # print("false order datetime")
                    # print("obj.order_datetime",obj.order_datetime)
                    # print("alnafi_payment[0].order_datetime",alnafi_payment[0].order_datetime)
                if alnafi_product:
                    # print("alnafi producr exists")
                    # print("alnafi_product[0].plan",alnafi_product[0].plan)
                    if alnafi_product[0].plan == 'Yearly':
                        # print("plan is yearly")
                        tolerance = timedelta(days=15)
                        expiry_date = alnafi_payment[0]['expiration_datetime']
                        expected_expiry = alnafi_payment[0].order_datetime+timedelta(days=380)-tolerance
                        # print("expiry_date",expiry_date)
                        # print("expected_expiry - tolerance",expected_expiry)
                        # print("expected_expiry + tolerance", alnafi_payment[0].order_datetime+timedelta(days=380) + tolerance)
                        if expiry_date >= expected_expiry and expiry_date <= alnafi_payment[0].order_datetime+timedelta(days=380) + tolerance:
                            # print("corrent expirt date")
                            valid_payment = True
                        else:
                            # print("obj id", obj.id)
                            # print("false expiry date")
                            # print("expiry_date",expiry_date)
                            # print("expected_expiry - tolerance",expected_expiry)
                            # print("expected_expiry + tolerance", alnafi_payment[0].order_datetime+timedelta(days=380) + tolerance)
                            valid_payment = False
                    if alnafi_product[0].plan == 'Half Yearly':
                        # print(alnafi_product[0].plan)
                        tolerance = timedelta(days=10)
                        expiry_date = alnafi_payment[0]['expiration_datetime']
                        expected_expiry = alnafi_payment[0].order_datetime+timedelta(days=180)-tolerance
                        if expiry_date >= expected_expiry and expiry_date <= alnafi_payment[0].order_datetime+timedelta(days=180) + tolerance:
                            # print("corrent expirt date")
                            valid_payment = True
                        else:
                            # print("false expiry")
                            valid_payment = False
                    
                    if alnafi_product[0].plan == 'Quarterly':
                        # print(alnafi_product[0].plan)
                        tolerance = timedelta(days=7)
                        expiry_date = alnafi_payment[0]['expiration_datetime']
                        expected_expiry = alnafi_payment[0].order_datetime+timedelta(days=90)-tolerance
                        if expiry_date >= expected_expiry and expiry_date <= alnafi_payment[0].order_datetime+timedelta(days=90) + tolerance:
                            # print("corrent expirt date")
                            valid_payment = True
                        else:
                            # print("false expiry")
                            valid_payment = False
                            
                    if alnafi_product[0].plan == 'Monthly':
                        # print(alnafi_product[0].plan)
                        tolerance = timedelta(days=5)
                        expiry_date = alnafi_payment[0]['expiration_datetime']
                        expected_expiry = alnafi_payment[0].order_datetime+timedelta(days=30)-tolerance
                        if expiry_date >= expected_expiry and expiry_date <= alnafi_payment[0].order_datetime+timedelta(days=30) + tolerance:
                            # print("corrent expirt date")
                            valid_payment = True
                        else:
                            # print("false expiry")
                            valid_payment = False
            
                valid_payments.append(valid_payment)
            
            # print(ubl_payments)
            serializer = Ubl_Ipg_PaymentsSerializer(ubl_payments, many=True)
            # print(serializer.data)
            # print(ubl_payments)
            # print(valid_payments)
            for i in range(len(serializer.data)):
                serializer.data[i]['is_valid_payment'] = valid_payments[i]
                
            response = {"payments":serializer,
                "valid_payments": valid_payments}
    else:
        serializer = Ubl_Ipg_PaymentsSerializer(ubl_pay,many=True)     
        response = {"payments":serializer}  
        
    return response


def easypaisa_payment_validation(time_threshold_str,q):
    easypaisa_pay = Easypaisa_Payment.objects.filter(order_datetime__date__gte=time_threshold_str)
    if q:
        easypaisa_pay = easypaisa_pay.filter(customer_email__iexact=q)  
        
    easypaisa_payments = []
    valid_payments = []
    
    if easypaisa_pay:
        for obj in easypaisa_pay:
            valid_payment = True
            easypaisa_payments.append(obj)
            alnafi_product = Alnafi_Product.objects.filter(name=obj.product_name)
            # print("obj.product_name", obj.product_name)
            # print("alnafiproduct", alnafi_product)
            # print("obj.amount", type(obj.amount))
            if alnafi_product:
                # print("alnafi_product[0].amount_pkr ",type(alnafi_product[0].amount_pkr))
                if alnafi_product[0].amount_pkr == obj.amount:
                    valid_payment = True
            
            #Get the latest alnafi payment
            alnafi_payment = list(AlNafi_Payment.objects.filter(customer_email=obj.customer_email))
            if alnafi_payment:
                if obj.product_name == alnafi_payment[0].product_name:
                    valid_payment = True
                else:
                    valid_payment = False
                    # print("obj id", obj.id)
                    # print("false product name")
                    # print("obj.product_name",obj.product_name)
                    # print("alnafi_payment[0].product_name",alnafi_payment[0].product_name)
                
                tolerance = timedelta(days=1)
                if obj.order_datetime.date()>=alnafi_payment[0].order_datetime.date() - tolerance and obj.order_datetime.date()<=alnafi_payment[0].order_datetime.date() + tolerance:
                    valid_payment = True
                else:
                    valid_payment = False
                    # print("obj id", obj.id)
                    # print("false order datetime")
                    # print("obj.order_datetime",obj.order_datetime)
                    # print("alnafi_payment[0].order_datetime",alnafi_payment[0].order_datetime)
                if alnafi_product:
                    # print("alnafi producr exists")
                    # print("alnafi_product[0].plan",alnafi_product[0].plan)
                    if alnafi_product[0].plan == 'Yearly':
                        tolerance = timedelta(days=15)
                        expiry_date = alnafi_payment[0]['expiration_datetime']
                        expected_expiry = alnafi_payment[0].order_datetime+timedelta(days=380)-tolerance
                        if expiry_date >= expected_expiry and expiry_date <= alnafi_payment[0].order_datetime+timedelta(days=380) + tolerance:
                            # print("corrent expirt date")
                            valid_payment = True
                        else:
                            # print("obj id", obj.id)
                            # print("false expiry date")
                            # print("expiry_date",expiry_date)
                            # print("expected_expiry - tolerance",expected_expiry)
                            # print("expected_expiry + tolerance", alnafi_payment[0].order_datetime+timedelta(days=380) + tolerance)
                            valid_payment = False
                    if alnafi_product[0].plan == 'Half Yearly':
                        # print(alnafi_product[0].plan)
                        tolerance = timedelta(days=10)
                        expiry_date = alnafi_payment[0]['expiration_datetime']
                        expected_expiry = alnafi_payment[0].order_datetime+timedelta(days=180)-tolerance
                        if expiry_date >= expected_expiry and expiry_date <= alnafi_payment[0].order_datetime+timedelta(days=180) + tolerance:
                            # print("corrent expirt date")
                            valid_payment = True
                        else:
                            # print("obj id", obj.id)
                            # print("false expiry")
                            # print("expiry_date",expiry_date)
                            # print("alnafi_payment[0]['expiration_datetime']+timedelta(days=380)",alnafi_payment[0]['expiration_datetime']+timedelta(days=180))
                            # print("expected_expiry-tolerance", expected_expiry)
                            # print("alnafi_payment[0]['expiration_datetime']",type(alnafi_payment[0]['expiration_datetime']))
                            valid_payment = False
                    
                    if alnafi_product[0].plan == 'Quarterly':
                        # print(alnafi_product[0].plan)
                        tolerance = timedelta(days=7)
                        expiry_date = alnafi_payment[0]['expiration_datetime']
                        expected_expiry = alnafi_payment[0].order_datetime+timedelta(days=90)-tolerance
                        if expiry_date >= expected_expiry and expiry_date <= alnafi_payment[0].order_datetime+timedelta(days=90) + tolerance:
                            # print("corrent expirt date")
                            valid_payment = True
                        else:
                            # print("false expiry")
                            # print("obj id", obj.id)
                            # print("alnafi_payment[0]['expiration_datetime']",alnafi_payment[0].expiration_datetime)
                            # print("alnafi_payment[0].expiration_datetime+timedelta(days=90)",alnafi_payment[0].expiration_datetime+timedelta(days=90))
                            # print("expected_expiry",expected_expiry)
                            # print("alnafi_payment[0].expiration_datetime",type(alnafi_payment[0].expiration_datetime))
                            valid_payment = False
                            
                    if alnafi_product[0].plan == 'Monthly':
                        # print(alnafi_product[0].plan)
                        tolerance = timedelta(days=5)
                        expiry_date = alnafi_payment[0].expiration_datetime
                        expected_expiry = alnafi_payment[0].order_datetime+timedelta(days=30)-tolerance
                        if expiry_date >= expected_expiry and expiry_date <= alnafi_payment[0].order_datetime+timedelta(days=30) + tolerance:
                            # print("corrent expirt date")
                            valid_payment = True
                        else:
                            # print("false expiry")
                            # print("obj id", obj.id)
                            # print("expiry_date",alnafi_payment[0].expiration_datetime)
                            # print("alnafi_payment[0].expiration_datetime+timedelta(days=30)",alnafi_payment[0].expiration_datetime+timedelta(days=30))
                            # print("expected_expiry-tolerance",expected_expiry)
                            # print("alnafi_payment[0].expiration_datetime",type(alnafi_payment[0].expiration_datetime))
                            valid_payment = False
                
                    
            # print("valid_payment", valid_payment)
            valid_payments.append(valid_payment)
            serializer = Easypaisa_PaymentsSerializer(easypaisa_payments, many=True)
            # print("queryset", serializer.data)
            # print(easypaisa_payments)
            # print("valid payments", valid_payments)
            for i in range(len(serializer.data)):
                # print(i)
                # print(serializer.data)
                # print(serializer.data[i])
                serializer.data[i]['is_valid_payment'] = valid_payments[i]
            response = {"payments":serializer,
                "valid_payments": valid_payments}     
    else:
        serializer = Easypaisa_PaymentsSerializer(easypaisa_pay,many=True)
        response = {"payments":serializer}
    return response


def stripe_payment_validation(time_threshold_str,q):
    stripe_pay = Stripe_Payment.objects.filter(order_datetime__date__gte=time_threshold_str)
    if q:
        stripe_pay = stripe_pay.filter(customer_email__iexact=q)
    
    # print("stripepay",stripe_pay)
    stripe_payments = []
    valid_payments = [] 
    if stripe_pay:
        for obj in stripe_pay:
            valid_payment = True
            stripe_payments.append(obj)
            alnafi_product = Alnafi_Product.objects.filter(name=obj.product_name)
            # print("obj.product_name", obj.product_name)
            # print("alnafiproduct", alnafi_product)
            # print("obj.amount", type(obj.amount))
            if alnafi_product:
                # print("alnafi_product[0].amount_usd ",type(alnafi_product[0].amount_usd))
                if alnafi_product[0].amount_usd == obj.amount:
                    valid_payment = True
            
            #Get the latest alnafi payment
            alnafi_payment = list(AlNafi_Payment.objects.filter(customer_email=obj.customer_email))
            # print("alnafi_payment",alnafi_payment)
            if alnafi_payment:
                if obj.product_name == alnafi_payment[0].product_name:
                    valid_payment = True
                else:
                    valid_payment = False
                    # print("obj id", obj.id)
                    # print("false product name")
                    # print("obj.product_name",obj.product_name)
                    # print("alnafi_payment[0].product_name",alnafi_payment[0].product_name)
                
                tolerance = timedelta(days=1)
                if obj.order_datetime.date()>=alnafi_payment[0].order_datetime.date() - tolerance and obj.order_datetime.date()<=alnafi_payment[0].order_datetime.date() + tolerance:
                    valid_payment = True
                else:
                    valid_payment = False
                    # print("obj id", obj.id)
                    # print("false order datetime")
                    # print("obj.order_datetime",obj.order_datetime)
                    # print("alnafi_payment[0].order_datetime",alnafi_payment[0].order_datetime)
                if alnafi_product:
                    # print("alnafi producr exists")
                    # print("alnafi_product[0].plan",alnafi_product[0].plan)
                    if alnafi_product[0].plan == 'Yearly':
                        tolerance = timedelta(days=15)
                        expiry_date = alnafi_payment[0].expiration_datetime
                        expected_expiry = alnafi_payment[0].order_datetime+timedelta(days=380)-tolerance
                        if expiry_date >= expected_expiry and expiry_date <= alnafi_payment[0].order_datetime+timedelta(days=380) + tolerance:
                            # print("corrent expirt date")
                            valid_payment = True
                        else:
                            # print("obj id", obj.id)
                            # print("false expiry date")
                            # print("expiry_date",expiry_date)
                            # print("expected_expiry - tolerance",expected_expiry)
                            # print("expected_expiry + tolerance", alnafi_payment[0].order_datetime+timedelta(days=380) + tolerance)
                            valid_payment = False
                    if alnafi_product[0].plan == 'Half Yearly':
                        # print(alnafi_product[0].plan)
                        tolerance = timedelta(days=10)
                        expiry_date = alnafi_payment[0].expiration_datetime
                        expected_expiry = alnafi_payment[0].order_datetime+timedelta(days=180)-tolerance
                        if expiry_date >= expected_expiry and expiry_date <= alnafi_payment[0].order_datetime+timedelta(days=180) + tolerance:
                            # print("corrent expirt date")
                            valid_payment = True
                        else:
                            # print("obj id", obj.id)
                            # print("false expiry")
                            # print("expiry_date",expiry_date)
                            # print("alnafi_payment[0].expiration_datetime+timedelta(days=380)",alnafi_payment[0].expiration_datetime+timedelta(days=180))
                            # print("expected_expiry-tolerance", expected_expiry)
                            # print("alnafi_payment[0].expiration_datetime",type(alnafi_payment[0].expiration_datetime))
                            valid_payment = False
                    
                    if alnafi_product[0].plan == 'Quarterly':
                        # print(alnafi_product[0].plan)
                        tolerance = timedelta(days=7)
                        expiry_date = alnafi_payment[0].expiration_datetime
                        expected_expiry = alnafi_payment[0].order_datetime+timedelta(days=90)-tolerance
                        if expiry_date >= expected_expiry and expiry_date <= alnafi_payment[0].order_datetime+timedelta(days=90) + tolerance:
                            # print("corrent expirt date")
                            valid_payment = True
                        else:
                            # print("false expiry")
                            # print("obj id", obj.id)
                            # print("alnafi_payment[0].expiration_datetime",alnafi_payment[0].expiration_datetime)
                            # print("alnafi_payment[0].expiration_datetime+timedelta(days=90)",alnafi_payment[0].expiration_datetime+timedelta(days=90))
                            # print("expected_expiry",expected_expiry)
                            # print("alnafi_payment[0].expiration_datetime",type(alnafi_payment[0].expiration_datetime))
                            valid_payment = False
                            
                    if alnafi_product[0].plan == 'Monthly':
                        # print(alnafi_product[0].plan)
                        tolerance = timedelta(days=5)
                        expiry_date = alnafi_payment[0].expiration_datetime
                        expected_expiry = alnafi_payment[0].order_datetime+timedelta(days=30)-tolerance
                        if expiry_date >= expected_expiry and expiry_date <= alnafi_payment[0].order_datetime+timedelta(days=30) + tolerance:
                            # print("corrent expirt date")
                            valid_payment = True
                        else:
                            # print("false expiry")
                            # print("obj id", obj.id)
                            # print("expiry_date",alnafi_payment[0].expiration_datetime)
                            # print("alnafi_payment[0].expiration_datetime+timedelta(days=30)",alnafi_payment[0].expiration_datetime+timedelta(days=30))
                            # print("expected_expiry-tolerance",expected_expiry)
                            # print("alnafi_payment[0].expiration_datetime",type(alnafi_payment[0].expiration_datetime))
                            valid_payment = False
                
                    
            # print("valid_payment", valid_payment)
            valid_payments.append(valid_payment)
            serializer = StripePaymentSerializer(stripe_payments, many=True)
            # print("queryset", serializer.data)
            # print(easypaisa_payments)
            # print("valid payments", valid_payments)
            for i in range(len(serializer.data)):
                # print(i)
                # print(serializer.data)
                # print(serializer.data[i])
                serializer.data[i]['is_valid_payment'] = valid_payments[i]
            response = {"payments":serializer,
                "valid_payments": valid_payments}
    else:
        serializer = StripePaymentSerializer(stripe_pay, many=True)
        response = {"payments":serializer}
    
    return response
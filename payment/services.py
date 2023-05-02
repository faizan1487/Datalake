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
from products.models import Alnafi_Product
def json_to_csv(serialized_data,name):
    file_name = f"{name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    # Build the full path to the media directory
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    pd.DataFrame(serialized_data.data).to_csv(file_path, index=False)
    return file_path

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


def no_of_payments(start_date,end_date,queryset):
    if not start_date:
        first_payment = AlNafi_Payment.objects.exclude(order_datetime=None).last()
        date_time_obj = first_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
        new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")                                                                                      
        start_date = str(new_date_obj.date())    
    if not end_date:
        last_payment = AlNafi_Payment.objects.exclude(order_datetime=None).first()
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
    
    if plan:
        payment_plan = []
        for obj in query_time:
            product = Alnafi_Product.objects.filter(name=obj.product_name)
            # print(product)
            if plan == 'yearly':
                for i in product:
                    if i.plan:
                        if i.plan == 'Yearly':
                            payment_plan.append(obj)
            if plan == 'halfyearly':
                for i in product:
                    if i.plan:
                        if i.plan == 'Half Yearly':
                            payment_plan.append(obj)
                            
            if plan == 'quarterly':           
                for i in product:
                    if i.plan:
                        if i.plan == 'Quarterly':
                            payment_plan.append(obj)
                            
            if plan == 'monthly':           
                for i in product:
                    if i.plan:
                        if i.plan == 'Monthly':
                            payment_plan.append(obj)
                            
        query_time = payment_plan              
    return query_time

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
    
    if plan:
        payment_plan = []
        for obj in query_time:
            product = Alnafi_Product.objects.filter(name=obj.product_name)
            # print(product)
            if plan == 'yearly':
                for i in product:
                    if i.plan:
                        if i.plan == 'Yearly':
                            payment_plan.append(obj)
            if plan == 'halfyearly':
                for i in product:
                    if i.plan:
                        if i.plan == 'Half Yearly':
                            payment_plan.append(obj)
                            
            if plan == 'quarterly':           
                for i in product:
                    if i.plan:
                        if i.plan == 'Quarterly':
                            payment_plan.append(obj)
                            
            if plan == 'monthly':           
                for i in product:
                    if i.plan:
                        if i.plan == 'Monthly':
                            payment_plan.append(obj)
                            
        query_time = payment_plan    
                
    return query_time

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
    
    if plan:
        payment_plan = []
        for obj in query_time:
            product = Alnafi_Product.objects.filter(name=obj.product_name)
            # print(product)
            if plan == 'yearly':
                for i in product:
                    if i.plan:
                        if i.plan == 'Yearly':
                            payment_plan.append(obj)
            if plan == 'halfyearly':
                for i in product:
                    if i.plan:
                        if i.plan == 'Half Yearly':
                            payment_plan.append(obj)                   
            if plan == 'quarterly':           
                for i in product:
                    if i.plan:
                        if i.plan == 'Quarterly':
                            payment_plan.append(obj)  
                                             
            if plan == 'monthly':           
                for i in product:
                    if i.plan:
                        if i.plan == 'Monthly':
                            payment_plan.append(obj)
                            
        query_time = payment_plan  
        
          
    return query_time


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
            
            # print("alnafi_product[0].amount_pkr ",type(alnafi_product[0].amount_pkr ))
            # print("obj.amount", type(obj.amount))
            if alnafi_product:
                if alnafi_product[0].amount_pkr == obj.amount:
                    valid_payment = True
            
            #Get the latest alnafi payment
            alnafi_payment = list(AlNafi_Payment.objects.filter(customer_email=obj.customer_email))
            # print("alnafi_payment[0].expiration_datetime",alnafi_payment[0].expiration_datetime)
            # print("alnafi_payment[0].expiration_datetime+timedelta(days=380)",alnafi_payment[0].expiration_datetime+timedelta(days=380))
            # print("alnafi_payment[0].expiration_datetime",type(alnafi_payment[0].expiration_datetime))
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
                        # print("plan is yearly")
                        tolerance = timedelta(days=15)
                        expiry_date = alnafi_payment[0].expiration_datetime
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
                        expiry_date = alnafi_payment[0].expiration_datetime
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
                        expiry_date = alnafi_payment[0].expiration_datetime
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
                        expiry_date = alnafi_payment[0].expiration_datetime
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
        response_data = {"payments":serializer.data}
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
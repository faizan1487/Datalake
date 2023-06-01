from rest_framework import status
from user.models import User
from .models import Stripe_Payment, Easypaisa_Payment, UBL_IPG_Payment, AlNafi_Payment,Main_Payment,UBL_Manual_Payment
from products.models import Main_Product
from .serializer import (StripePaymentSerializer, Easypaisa_PaymentsSerializer, Ubl_Ipg_PaymentsSerializer, 
                         AlNafiPaymentSerializer,PaymentCombinedSerializer,LocalPaymentCombinedSerializer,MainPaymentSerializer,UBL_Manual_PaymentSerializer)
from .services import (easypaisa_pay, ubl_pay, stripe_pay, json_to_csv,stripe_no_payments,ubl_no_payments,easypaisa_no_payments,
                       renewal_no_of_payments,ubl_payment_validation,easypaisa_payment_validation,stripe_payment_validation,search_payment,
                       main_no_of_payments)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta, date
from django.db.models import Q
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import Group
import os
import pandas as pd
from rest_framework.permissions import BasePermission
from user.services import GroupPermission
from products.models import  IslamicAcademy_Product, Alnafi_Product
from itertools import chain
from django.core.cache import cache
from user.services import upload_csv_to_s3
import numpy as np
import json
from django.db.models import F, Max, Q
from django.db.models.functions import Upper
from django.core.exceptions import ObjectDoesNotExist



class MyPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100           

# delete this api before production
class AlnafiPayment(APIView):
    # def get(self,request):
    #     alnafi_payment = AlNafi_Payment.objects.values('id', 'order_id', 'payment_id')
    #     serializer = GetAlnafipaymentSerializer(alnafi_payment, many=True)
    #     return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        serializer = AlNafiPaymentSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UBLManualPayment(APIView):
    # def get(self,request):
    #     alnafi_payment = AlNafi_Payment.objects.values('id', 'order_id', 'payment_id')
    #     serializer = GetAlnafipaymentSerializer(alnafi_payment, many=True)
    #     return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        print(data)
        serializer = UBL_Manual_PaymentSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'status':"Success!"})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MainPaymentAPIView(APIView):
    def post(self, request):
        file = request.FILES['file']
        df = pd.read_csv(file)
        # print(int(df.to_dict('records')[0]['product']))
        
        # Replace non-finite values with NaN
        df['product'] = pd.to_numeric(df['product'], errors='coerce')
        
        # Convert NaN values to None (null) instead of a default value
        df['product'] = np.where(pd.isnull(df['product']), None, df['product'])
        
        # print(df['product'])
        serializer = MainPaymentSerializer(data=df.to_dict('records'), many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status= 400)

class PaymentDelete(APIView):
    def get(self, request):
        objs = UBL_Manual_Payment.objects.all()
        objs.delete()
        return Response('deleted')

#optimized 
class RenewalPayments(APIView):
    # permission_classes = [IsAuthenticated]
    # permission_classes = [GroupPermission]
    # required_groups = ['Sales', 'Admin']
    def get(self, request):
        expiration = self.request.GET.get('expiration_date', None) or None
        q = self.request.GET.get('q', None) or None
        source = self.request.GET.get('source', None) or None
        exact = self.request.GET.get('exact', None) or None
        export = self.request.GET.get('export', None) or None
        plan = self.request.GET.get('plan', None) or None
        url = request.build_absolute_uri()
        active = self.request.GET.get('is_active', None) or None
        product = self.request.GET.get('product', None) or None

        # payments = cache.get(url)
        # if payments is None:
        payments = Main_Payment.objects.filter(source='Al-Nafi').exclude(product__product_name="test").select_related('product').values()
        payments = payments.exclude(amount__in=[1,0.01,1.0,2.0,3.0,4.0,5.0,5.0,6.0,7.0,8.0,9.0,10.0])
            # cache.set(url, payments)

        if q:
            payments = payments.filter(Q(user__email__iexact=q) | Q(amount__iexact=q))            
            
        if source:
            payments = payments.filter(source=source)

        if product:
            payments = payments.filter(product__product_name__icontains=product)

        if expiration:
            expiration_date = date.today() + timedelta(days=int(expiration))
            if exact == 'true':
                payments = payments.filter(expiration_datetime__date=expiration_date)
            else:
                payments = payments.filter(
                    Q(expiration_datetime__date__gte=date.today()) & Q(expiration_datetime__date__lte=expiration_date)
                )

        if active == 'true':
            payments = payments.filter(expiration_datetime__date__gt=date.today())
        elif active == 'false':
            payments = payments.filter(expiration_datetime__date__lt=date.today())

        plan_mapping = {
            'yearly': 'Yearly',
            'halfyearly': 'Half Yearly',
            'quarterly': 'Quarterly',
            'monthly': 'Monthly',
        }
        #The annotate() function is used to add an extra field payment_cycle to each payment object in the queryset. 
        # This field represents the uppercase version of the product_plan field of the associated product.
        payments = payments.annotate(payment_cycle=Upper('product__product_plan'))
        #If the plan is provided and it is not 'all', the queryset is further filtered using
        # the filter() function. It applies a condition using the Q object, which checks if 
        # the product_plan is an exact case-insensitive match to the given plan 
        # or if it matches any plan name from the plan_mapping dictionary.
        if plan:
            if plan.lower() != 'all':
                payments = payments.filter(
                    Q(product__product_plan__iexact=plan) | Q(product__product_plan__iexact=plan_mapping.get(plan, ''))
                )
        else:
            payments = payments.filter(product__product_plan__isnull=False)

        for i, data in enumerate(payments):
            # date_string = data['expiration_datetime']
            date_string = payments[i]['expiration_datetime']
            if date_string:
                payments[i]['is_active'] = date_string.date() >= date.today()
            else:
                payments[i]['is_active'] = False

        def json_serializable(obj):
                if isinstance(obj, datetime):
                    return obj.isoformat()  # Convert datetime to ISO 8601 format
                raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")
            
        users = list(payments.values('user__email','user__phone'))
        products = list(payments.values('product__product_name'))
        payment_list = list(payments.values())                          
        for i in range(len(payment_list)):
            try:
                payment_list[i]['user_id'] = users[i]['user__email']
                payment_list[i]['phone'] = users[i]['user__phone']
                payment_list[i]['product_id'] = products[i]['product__product_name']
                payment_list[i]['is_active'] = payments[i]['is_active']
            except Exception as e:
                pass
        
        if export == 'true':
            file_name = f"Payments_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            df = pd.DataFrame(payment_list).to_csv(index=False)
            s3 = upload_csv_to_s3(df, file_name)
            data = {'file_link': file_path, 'export': 'true'}
            return Response(data)
        else:
            payment_json = json.dumps(payment_list, default=json_serializable)  # Serialize the list to JSON with custom encoder
            payment_objects = json.loads(payment_json)
            
            paginator = MyPagination()
            paginated_queryset = paginator.paginate_queryset(payment_objects, request)
            return paginator.get_paginated_response(paginated_queryset)     
    
#optimized       
class SearchPayments(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [GroupPermission]
    required_groups = ['Sales', 'Admin']
    def get(self, request):
        query = self.request.GET.get('q', None) or None
        source = self.request.GET.get('source', None) or None
        origin = self.request.GET.get('origin', None) or None
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        export = self.request.GET.get('export', None) or None
        plan = self.request.GET.get('plan', None) or None   
        product = self.request.GET.get('product', None) or None  
        url = request.build_absolute_uri()
        # payments = cache.get(url+'payments')
        # if payments is None:
        payments = search_payment(export,query,start_date,end_date,plan,request,url,product,source,origin)
            # cache.set(url+'payments', payments)   
        
        
        if payments['success'] == 'true':
            def json_serializable(obj):
                    if isinstance(obj, datetime):
                        return obj.isoformat()  # Convert datetime to ISO 8601 format
                    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

            users = list(payments['payments'].values('user__email'))
            products = list(payments['payments'].values('product__product_name'))
            payment_list = list(payments["payments"].values())

            for i in range(len(payments['payments'])):
                try:
                    payment_list[i]['user_id'] = users[i]['user__email']
                    payment_list[i]['product_id'] = products[i]['product__product_name']
                except Exception as e:
                    pass  


            
            if export=='true':
                df = pd.DataFrame(payment_list)
                # Merge dataframes
                file_name = f"Payments_DATA_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                df = df.to_csv(index=False)
                s3 = upload_csv_to_s3(df,file_name)
                data = {'file_link': file_path,'export':'true'}
                return Response(data)
            else:            
                payment_json = json.dumps(payment_list, default=json_serializable)  # Serialize the list to JSON with custom encoder
                payment_objects = json.loads(payment_json)
                
                paginator = MyPagination()
                paginated_queryset = paginator.paginate_queryset(payment_objects, request)
                return paginator.get_paginated_response(paginated_queryset)
        else:
            response_data = {"Error": "Incorrect product name or payments for this product does not exist"}
            return Response(response_data)
                
#optimized
class PaymentValidation(APIView):
    # permission_classes = [IsAuthenticated]
    # permission_classes = [GroupPermission]
    # required_groups = ['Sales', 'Admin']
    def get(self, request):
        q = self.request.GET.get('q', None) or None
        source = self.request.GET.get('source', None) or None
        export = self.request.GET.get('export', None) or None
        # create a datetime object for 24 hours ago
        url = request.build_absolute_uri()  
        
        # payments = cache.get(url)'Al-Nafi'
        # if payments is None:
        payments = Main_Payment.objects.filter(source='Al-Nafi').exclude(product__product_name="test").values()
        payments = payments.exclude(amount__in=[0,0.1,1,2,0.01,1.0,2.0,3.0,4.0,5.0,5.0,6.0,7.0,8.0,9.0,10.0,10])
        # cache.set(url, payments)      
        if source:
            payments = payments.filter(source=source)

        if q:
            payments = payments.filter(Q(user__email__iexact=q) | Q(amount__iexact=q))   

        
        valid_payments = []

        product_ids = set(payments.values_list('product_id', flat=True))
        products = Main_Product.objects.filter(id__in=product_ids).values('id', 'amount_pkr','amount_usd', 'product_plan')

        source_payments = Main_Payment.objects.filter(source__in=['Easypaisa','UBL_IPG','Stripe']).order_by('-order_datetime').prefetch_related('user', 'product').values()
        latest_payments = {}
        ##Removes duplicates from source_payments and only adds the latest payment into the latest payment dict
        for payment in source_payments:
            key = (payment['user_id'], payment['product_id'])
            if key not in latest_payments:
                latest_payments[key] = payment
                
        for payment in payments:
            valid_payment = {
                'valid': True,
                'reasons': []
            }

            try:
                product = next(filter(lambda p: p['id'] == payment['product_id'], products), None)
                if product:
                    if payment['currency'] == 'PKR':
                        product_amount_without_zeros = str(product['amount_pkr']).rstrip('0').rstrip('.')
                        if product_amount_without_zeros == payment['amount']:
                            pass
                        else:
                            valid_payment['valid'] = False
                            valid_payment['reasons'].append('Product and Payment Amount mismatch')
                    elif payment['currency'] == 'USD':
                        product_amount_without_zeros = str(product['amount_usd']).rstrip('0').rstrip('.')
                        if product_amount_without_zeros == payment['amount']:
                            pass
                        else:
                            valid_payment['valid'] = False
                            valid_payment['reasons'].append('Product and Payment Amount mismatch')

                    else:
                        valid_payment['valid'] = False
                        valid_payment['reasons'].append('Invalid currency')

                else:
                    valid_payment['valid'] = False
                    valid_payment['reasons'].append('Product not found')



                latest_payment = latest_payments.get((payment['user_id'], payment['product_id']))
                
                # This condition will be False when the order date of the latest payment (latest_payment['order_datetime'])
                # is outside the range defined by subtracting the tolerance from the current payment's order date (payment['order_datetime'].date() - tolerance) 
                # and adding the tolerance to it (payment['order_datetime'].date() + tolerance).
                
                # In other words, if the order date of the latest payment is earlier than payment['order_datetime'].date() - tolerance 
                # or later than payment['order_datetime'].date() + tolerance, the condition will evaluate to False, indicating a mismatch 
                # in the order dates.

                # This condition is used to determine if the order dates of the current payment and the latest payment are close enough within 
                # the specified tolerance. If they are within that range, the condition evaluates to True, indicating that the check is successful. 
                # Otherwise, it evaluates to False, indicating a mismatch in the order dates.
                
                if latest_payment:
                    tolerance = timedelta(days=1)
                    if (payment['order_datetime'].date() - tolerance <= latest_payment['order_datetime'].date() <= payment['order_datetime'].date() + tolerance):
                        pass
                    else:
                        valid_payment['valid'] = False
                        valid_payment['reasons'].append('Order date mismatch')
                        
                if product:
                    if product['product_plan'] == 'Yearly':
                        tolerance = timedelta(days=15)
                        if latest_payment:
                            expiry_date = payment['expiration_datetime'].date()
                            expected_expiry = payment['order_datetime'].date() + timedelta(days=380) - tolerance

                            if expected_expiry <= expiry_date <= (latest_payment['order_datetime'].date() + timedelta(days=380) + tolerance):
                                pass
                            else:
                                valid_payment['valid'] = False
                                valid_payment['reasons'].append('Yearly expiration date mismatch')

                    if product['product_plan'] == 'Half Yearly':
                        if latest_payment:
                            tolerance = timedelta(days=10)
                            expiry_date = payment['expiration_datetime'].date()
                            expected_expiry = payment['order_datetime'].date() + timedelta(days=180) - tolerance

                            if expected_expiry <= expiry_date <= (latest_payment['order_datetime'].date() + timedelta(days=180) + tolerance):
                                pass
                            else:
                                valid_payment['valid'] = False
                                valid_payment['reasons'].append('Half Yearly expiration date mismatch')

                    if product['product_plan'] == 'Quarterly':
                        if latest_payment:
                            tolerance = timedelta(days=7)
                            expiry_date = payment['expiration_datetime'].date()
                            expected_expiry = payment['order_datetime'].date() + timedelta(days=90) - tolerance

                            if expected_expiry <= expiry_date <= (latest_payment['order_datetime'].date() + timedelta(days=90) + tolerance):
                                pass
                            else:
                                valid_payment['valid'] = False
                                valid_payment['reasons'].append('Quarterly expiration date mismatch')

                    if product['product_plan'] == 'Monthly':
                        if latest_payment:
                            tolerance = timedelta(days=5)
                            expiry_date = payment['expiration_datetime'].date()
                            expected_expiry = payment['order_datetime'].date() + timedelta(days=30) - tolerance

                            if expected_expiry <= expiry_date <= (latest_payment['order_datetime'].date() + timedelta(days=30) + tolerance):
                                pass
                            else:
                                valid_payment['valid'] = False
                                valid_payment['reasons'].append('Monthly expiration date mismatch')

            except ObjectDoesNotExist:
                pass

            valid_payments.append(valid_payment)            
        
        def json_serializable(obj):
                if isinstance(obj, datetime):
                    return obj.isoformat()  # Convert datetime to ISO 8601 format
                raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

        users = list(payments.values('user__email'))
        products = list(payments.values('product__product_name'))
        payment_list = list(payments.values())                          
        for i in range(len(payment_list)):
            try:
                payment_list[i]['user_id'] = users[i]['user__email']
                payment_list[i]['product_id'] = products[i]['product__product_name']
                payment_list[i]['is_valid_payment'] = valid_payments[i]
            except Exception as e:
                pass
      
            
        payment_json = json.dumps(payment_list, default=json_serializable)  # Serialize the list to JSON with custom encoder
        payment_objects = json.loads(payment_json)
        
        paginator = MyPagination()
        paginated_queryset = paginator.paginate_queryset(payment_objects, request)
        return paginator.get_paginated_response(paginated_queryset) 
       
#Optimized
#shows no of payments on each date
class NoOfPayments(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [GroupPermission]
    required_groups = ['Sales', 'Admin']
    def get(self, request):
        source = self.request.GET.get('source', None) or None
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        
        payments = main_no_of_payments(start_date,end_date,source)
        response_data = {"payments": payments}
        return Response(response_data)
    
        
        
#Optimized  
#shows alnafi/mainsite no of payments on each date
class RenewalNoOfPayments(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [GroupPermission]
    required_groups = ['Sales', 'Admin']
    def get(self, request):
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        payments = Main_Payment.objects.exclude(product__product_name="test").exclude(amount=1).filter(source='Al-Nafi')
        response_data = renewal_no_of_payments(start_date,end_date,payments)
        return Response(response_data)
        
        
            


#Creating API For ubl_ipg Payments:
class GetUBLPayments(APIView):
    def get(self,request):
        ubl_pay = UBL_IPG_Payment.objects.all()
        serializer = Ubl_Ipg_PaymentsSerializer(ubl_pay, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        serializer = Ubl_Ipg_PaymentsSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Creating API For Easypaisa Payments
class GetEasypaisaPayments(APIView):
    def get(self,request):
        obj = Easypaisa_Payment.objects.all()
        serializer = Easypaisa_PaymentsSerializer(obj, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        serializer = Easypaisa_PaymentsSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#main site payment data required                

        
       
        
#Creating API For Stripe Payments: 
# class GetAlnafiPayments(APIView):
#     def get(self,request):
#         alnafi_payment = AlNafi_Payment.objects.all()
#         serializer = AlNafiPaymentSerializer(alnafi_payment,many=True)
#         return Response(serializer.data)
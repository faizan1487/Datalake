from rest_framework import status
from user.models import User
from .models import Stripe_Payment, Easypaisa_Payment, UBL_IPG_Payment, AlNafi_Payment,Main_Payment
from products.models import Main_Product
from .serializer import (StripePaymentSerializer, Easypaisa_PaymentsSerializer, Ubl_Ipg_PaymentsSerializer, 
                         AlNafiPaymentSerializer,PaymentCombinedSerializer,LocalPaymentCombinedSerializer,MainPaymentSerializer)
from .services import (easypaisa_pay, ubl_pay, stripe_pay, json_to_csv,stripe_no_payments,ubl_no_payments,easypaisa_no_payments,
                       no_of_payments,ubl_payment_validation,easypaisa_payment_validation,stripe_payment_validation,search_payment,
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


class MainPaymentAPIView(APIView):
    def post(self, request):
        file = request.FILES['file']
        df = pd.read_csv(file)
        # print(int(df.to_dict('records')[0]['product']))
        
        # Replace non-finite values with NaN
        df['product'] = pd.to_numeric(df['product'], errors='coerce')
        
        # Convert NaN values to None (null) instead of a default value
        df['product'] = np.where(pd.isnull(df['product']), None, df['product'])
        
        print(df['product'])
        serializer = MainPaymentSerializer(data=df.to_dict('records'), many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status= 400)



class PaymentDelete(APIView):
    def get(self, request):
        objs = Main_Payment.objects.all()
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

        payments = cache.get(url)
        if payments is None:
            payments = Main_Payment.objects.select_related('product').all().values()
            cache.set(url, payments)

        if q:
            payments = payments.filter(user__email__iexact=q)

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

        payments = payments.annotate(payment_cycle=Upper('product__product_plan'))

        if plan:
            if plan.lower() != 'all':
                payments = payments.filter(
                    Q(product__product_plan__iexact=plan) | Q(product__product_plan__iexact=plan_mapping.get(plan, ''))
                )
        else:
            payments = payments.filter(product__product_plan__isnull=False)

        # serializer = MainPaymentSerializer(payments, many=True)

        for i, data in enumerate(payments):
            date_string = data['expiration_datetime']
            if date_string:
                # try:
                #     date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S").date()
                # except ValueError:
                #     date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f").date()
                payments[i]['is_active'] = date_string.date() >= date.today()
            else:
                payments[i]['is_active'] = False

        
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
        payments = cache.get(url+'payments')
        if payments is None:
            payments = search_payment(export,query,start_date,end_date,plan,request,url,product,source,origin)
            cache.set(url+'payments', payments)   
        
        
        def json_serializable(obj):
                if isinstance(obj, datetime):
                    return obj.isoformat()  # Convert datetime to ISO 8601 format
                raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

        users = list(payments['payments'].values('user__email'))
        products = list(payments['payments'].values('product__product_name'))
        payment_list = list(payments["payments"].values())                          
        for i in range(len(payment_list)):
            try:
                payment_list[i]['payment_cycle'] = payments['payment_cycle'][i]
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
            

#optimized
class PaymentValidation(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [GroupPermission]
    required_groups = ['Sales', 'Admin']
    def get(self, request):
        q = self.request.GET.get('q', None) or None
        source = self.request.GET.get('source', None) or None
        export = self.request.GET.get('export', None) or None
        # create a datetime object for 24 hours ago
        time_threshold = timezone.now() - timezone.timedelta(days=90)
        time_threshold_str = time_threshold.strftime('%Y-%m-%d')
        url = request.build_absolute_uri()  
        
        payments = cache.get(url)
        if payments is None:
            # payments = payment_validation(time_threshold_str,q,source)
            # payments = Main_Payment.objects.all().select_related('product')
            payments = Main_Payment.objects.all().values()
            cache.set(url, payments) 
        
        
        

        if source:
            payments = payments.filter(source=source)

        if q:
            payments = payments.filter(user__email__iexact=q)

        response = {"payments": None, "valid_payments": []}
        
        validated_payments = []
        valid_payments = []

        product_ids = set(payments.values_list('product_id', flat=True))
        products = Main_Product.objects.filter(id__in=product_ids).values('id', 'amount_pkr', 'product_plan')

        alnafi_payments = payments.filter(source='Al-Nafi').order_by('-order_datetime').prefetch_related('user', 'product')

        latest_payments = {}
        for payment in alnafi_payments:
            key = (payment['user_id'], payment['product_id'])
            if key not in latest_payments:
                latest_payments[key] = payment

        for payment in payments:
            valid_payment = False

            try:
                product = next(filter(lambda p: p['id'] == payment['product_id'], products), None)

                if product and product['amount_pkr'] == payment['amount']:
                    valid_payment = True

                latest_payment = latest_payments.get((payment['user_id'], payment['product_id']))

                if latest_payment:
                    tolerance = timedelta(days=1)
                    if (payment['order_datetime'].date() - tolerance <= latest_payment['order_datetime'].date() <= payment['order_datetime'].date() + tolerance):
                        valid_payment = True

                if product:
                    if product['product_plan'] == 'Yearly':
                        tolerance = timedelta(days=15)
                        if latest_payment:
                            expiry_date = latest_payment['expiration_datetime'].date()
                            expected_expiry = latest_payment['order_datetime'].date() + timedelta(days=380) - tolerance

                            if expected_expiry <= expiry_date <= (latest_payment['order_datetime'].date() + timedelta(days=380) + tolerance):
                                valid_payment = True

                    if product['product_plan'] == 'Half Yearly':
                        if latest_payment:
                            tolerance = timedelta(days=10)
                            expiry_date = latest_payment['expiration_datetime'].date()
                            expected_expiry = latest_payment['order_datetime'].date() + timedelta(days=180) - tolerance

                            if expected_expiry <= expiry_date <= (latest_payment['order_datetime'].date() + timedelta(days=180) + tolerance):
                                valid_payment = True

                    if product['product_plan'] == 'Quarterly':
                        if latest_payment:
                            tolerance = timedelta(days=7)
                            expiry_date = latest_payment['expiration_datetime'].date()
                            expected_expiry = latest_payment['order_datetime'].date() + timedelta(days=90) - tolerance

                            if expected_expiry <= expiry_date <= (latest_payment['order_datetime'].date() + timedelta(days=90) + tolerance):
                                valid_payment = True

                    if product['product_plan'] == 'Monthly':
                        if latest_payment:
                            tolerance = timedelta(days=5)
                            expiry_date = latest_payment['expiration_datetime'].date()
                            expected_expiry = latest_payment['order_datetime'].date() + timedelta(days=30) - tolerance

                            if expected_expiry <= expiry_date <= (latest_payment['order_datetime'].date() + timedelta(days=30) + tolerance):
                                valid_payment = True

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
    
        """_summary_

        Returns:
            _type_: _description_
        """    
#Optimized      
class RenewalNoOfPayments(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [GroupPermission]
    required_groups = ['Sales', 'Admin']
    def get(self, request):
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        payments = Main_Payment.objects.filter(source='Al-Nafi')
        response_data = no_of_payments(start_date,end_date,payments)
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
from rest_framework import status
from user.models import User
from .models import Stripe_Payment, Easypaisa_Payment, UBL_IPG_Payment, AlNafi_Payment,Main_Payment
from .serializer import (StripePaymentSerializer, Easypaisa_PaymentsSerializer, Ubl_Ipg_PaymentsSerializer, 
                         AlNafiPaymentSerializer,PaymentCombinedSerializer,LocalPaymentCombinedSerializer,MainPaymentSerializer)
from .services import (easypaisa_pay, ubl_pay, stripe_pay, json_to_csv,stripe_no_payments,ubl_no_payments,easypaisa_no_payments,
                       no_of_payments,ubl_payment_validation,easypaisa_payment_validation,stripe_payment_validation,search_payment,
                       payment_validation,main_no_of_payments)
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






#main site data required
class SearchAlNafiPayments(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [GroupPermission]
    required_groups = ['Sales', 'Admin']
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
        if q:
            queryset = cache.get(url)
            if queryset is None:
                queryset = AlNafi_Payment.objects.filter(
                    Q(customer_email__iexact=q) | Q(order_id__iexact=q))
                cache.set(url, queryset)
        else:
            queryset = cache.get(url)
            if queryset is None:
                queryset = AlNafi_Payment.objects.all()
                cache.set(url, queryset)
          
        if product:
            queryset = queryset.filter(product_name__icontains=product)  
              
        if source:
            queryset = queryset.filter(source__iexact=source)
            
        if expiration:
            if exact=='true':
                expiration_date = date.today() + timedelta(days=int(expiration))
                queryset = queryset.filter(expiration_datetime__date=expiration_date)
            else:
                expiration_date = date.today() + timedelta(days=int(expiration))
                queryset = queryset.filter(Q(expiration_datetime__date__gte=date.today()) & Q(expiration_datetime__date__lte=expiration_date)) 
        
        
                   
        if active == 'true':
            queryset = [obj for obj in queryset if obj.expiration_datetime.date() > date.today()]
        elif active == 'false':
            queryset = [obj for obj in queryset if obj.expiration_datetime.date() < date.today()]
        
        payment_plan = []
        payment_cycle = []
        for obj in queryset:
            product = Alnafi_Product.objects.filter(name=obj.product_name)
            if product:
                if product[0].plan:
                    if plan == 'yearly':
                        if product[0].plan == 'Yearly':
                            payment_plan.append(obj)
                            payment_cycle.append('Yearly')
                    elif plan == 'halfyearly':
                        if product[0].plan == 'Half Yearly':
                            payment_plan.append(obj)
                            payment_cycle.append('Half yearly')
                    elif plan == 'quarterly':           
                        if product[0].plan == 'Quarterly':
                            payment_plan.append(obj)
                            payment_cycle.append('Quarterly')
                    elif plan == 'monthly':           
                        if product[0].plan == 'Monthly':
                            payment_plan.append(obj)
                            payment_cycle.append('Monthly')
                    else:
                        if product[0].plan == 'Yearly':
                            payment_plan.append(obj)
                            payment_cycle.append('Yearly')
                        if product[0].plan == 'Half Yearly':
                            payment_plan.append(obj)
                            payment_cycle.append('Half yearly')
                        if product[0].plan == 'Quarterly':
                            payment_plan.append(obj)
                            payment_cycle.append('Quarterly')
                        if product[0].plan == 'Monthly':
                            payment_plan.append(obj)
                            payment_cycle.append('Monthly')   
                                
        queryset = payment_plan   
                 
        alnafi_payments_serializer = AlNafiPaymentSerializer(queryset, many=True)
        for i in range(len(alnafi_payments_serializer.data)):
            alnafi_payments_serializer.data[i]['payment_cycle'] = payment_cycle[i]
            if active == 'true':
                alnafi_payments_serializer.data[i]['is_active'] = True
            elif active == 'false':
                alnafi_payments_serializer.data[i]['is_active'] = False
            else:
                date_string = alnafi_payments_serializer.data[i]['expiration_datetime']
                try:
                    date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S").date()
                except:
                    date_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f").date()
                if date_object < date.today():
                    alnafi_payments_serializer.data[i]['is_active'] = False
                else:
                    alnafi_payments_serializer.data[i]['is_active'] = True
                  
        if export =='true':
            file_name = f"Alanfi_Payments_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
            # Build the full path to the media directory
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            df = pd.DataFrame(alnafi_payments_serializer.data).to_csv(index=False)   
            s3 = upload_csv_to_s3(df,file_name)            
            data = {'file_link': file_path,'export':'true'}
            return Response(data)                       
        else:
            paginator = MyPagination()
            paginated_queryset = paginator.paginate_queryset(alnafi_payments_serializer.data, request)
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
        
        serializer = MainPaymentSerializer(payments['payments'],many=True)       
        if export=='true':
            df = pd.DataFrame(serializer.data)
            # Merge dataframes
            file_name = f"Payments_DATA_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            df = df.to_csv(index=False)
            s3 = upload_csv_to_s3(df,file_name)
            data = {'file_link': file_path,'export':'true'}
            return Response(data)
        else:                
            for i in range(len(serializer.data)):
                try:
                    serializer.data[i]['payment_cycle'] = payments['payment_cycle'][i]
                except Exception as e:
                    print(e)    
            paginator = MyPagination()
            paginated_queryset = paginator.paginate_queryset(serializer.data, request)
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
    
    
#main site payment data required        
class RenewalNoOfPayments(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [GroupPermission]
    required_groups = ['Sales', 'Admin']
    def get(self, request):
        source = self.request.GET.get('source', None) or None
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        
        if source:
            queryset = AlNafi_Payment.objects.filter(source__iexact=source)
            response_data = no_of_payments(start_date,end_date,queryset)
        else:
            response_data = no_of_payments(start_date,end_date,None)
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
class PaymentValidation(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [GroupPermission]
    required_groups = ['Sales', 'Admin']
    def get(self, request):
        # expiration = self.request.GET.get('expiration_date', None) or None
        q = self.request.GET.get('q', None) or None
        source = self.request.GET.get('source', None) or None
        # exact = self.request.GET.get('exact', None) or None
        export = self.request.GET.get('export', None) or None
        # create a datetime object for 24 hours ago
        time_threshold = timezone.now() - timezone.timedelta(days=90)
        time_threshold_str = time_threshold.strftime('%Y-%m-%d')
        url = request.build_absolute_uri()
        
        
        
        payments = cache.get(url)
        if payments is None:
            payments = payment_validation(time_threshold_str,q,source)
            cache.set(url, payments) 
        paginator = MyPagination()
        paginated_queryset = paginator.paginate_queryset(payments['payments'].data, request)
        return paginator.get_paginated_response(paginated_queryset)
        
        # elif source == 'easypaisa':
        #     easypaisa = cache.get(url)
        #     if easypaisa is None:
        #         easypaisa = easypaisa_payment_validation(time_threshold_str,q)
        #         cache.set(url, easypaisa) 
        #     paginator = MyPagination()
        #     paginated_queryset = paginator.paginate_queryset(easypaisa['payments'].data, request)
        #     return paginator.get_paginated_response(paginated_queryset)
        # elif source == 'stripe':
        #     stripe = cache.get(url)
        #     if stripe is None:
        #         stripe = stripe_payment_validation(time_threshold_str,q)
        #         cache.set(url, stripe) 
        #     paginator = MyPagination()
        #     paginated_queryset = paginator.paginate_queryset(stripe['payments'].data, request)
        #     return paginator.get_paginated_response(paginated_queryset)
        # else:
            # ubl = cache.get(url+'ubl')
            # if ubl is None:
            #     ubl = ubl_payment_validation(time_threshold_str,q)
            #     cache.set(url+'ubl', ubl) 
                            
            # easypaisa = cache.get(url+'easypaisa')
            # if easypaisa is None:
            #     easypaisa = easypaisa_payment_validation(time_threshold_str,q)
            #     cache.set(url+'easypaisa', easypaisa) 
            
            # stripe = cache.get(url+'stripe')
            # if stripe is None:
            #     stripe = stripe_payment_validation(time_threshold_str,q)
            #     cache.set(url+'stripe', stripe)
                        
            # combined_data = {
            #         'data1': stripe['payments'].data,
            #         'data2': ubl['payments'].data,
            #         'data3': easypaisa['payments'].data,
            #     }
            
            # serialized_data = PaymentCombinedSerializer(combined_data).data
            # for i in range(len(serialized_data['data1'])):
            #     serialized_data['data1'][i]['is_valid_payment'] = stripe['valid_payments'][i]
            
            # for i in range(len(serialized_data['data2'])):
            #     serialized_data['data2'][i]['is_valid_payment'] = ubl['valid_payments'][i]
                
            # for i in range(len(serialized_data['data3'])):
            #     serialized_data['data3'][i]['is_valid_payment'] = easypaisa['valid_payments'][i]
                                     
            # combined_queryset = list(chain(serialized_data['data1'], serialized_data['data2'],serialized_data['data3']))
            # paginator = MyPagination()
            # paginated_queryset = paginator.paginate_queryset(combined_queryset, request)
            # return paginator.get_paginated_response(paginated_queryset)
        
        
#Creating API For Stripe Payments: 
# class GetAlnafiPayments(APIView):
#     def get(self,request):
#         alnafi_payment = AlNafi_Payment.objects.all()
#         serializer = AlNafiPaymentSerializer(alnafi_payment,many=True)
#         return Response(serializer.data)
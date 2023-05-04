from rest_framework import status
from user.models import User
from .models import Stripe_Payment, Easypaisa_Payment, UBL_IPG_Payment, AlNafi_Payment
from .serializer import (StripePaymentSerializer, Easypaisa_PaymentsSerializer, Ubl_Ipg_PaymentsSerializer, 
                         AlNafiPaymentSerializer,PaymentCombinedSerializer,LocalPaymentCombinedSerializer)
from .services import (easypaisa_pay, ubl_pay, stripe_pay, json_to_csv,stripe_no_payments,ubl_no_payments,easypaisa_no_payments,
                       no_of_payments,ubl_payment_validation,easypaisa_payment_validation,stripe_payment_validation)
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

class MyPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100           



def easypaisa_payment(export,query,start_date,end_date,plan,request,url,product):
    obj = cache.get(url+'easypaisa')
    if obj is None:
        obj = easypaisa_pay(query,start_date,end_date,plan,product)
        cache.set(url+'easypaisa', obj) 
    
    serializer = Easypaisa_PaymentsSerializer(obj['data'],many=True)
    if export=='true':
        file_name = f"Easypaisa_Payments_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        # Build the full path to the media directory
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        df = pd.DataFrame(serializer.data).to_csv(index=False)
        # print(df)
        s3 = upload_csv_to_s3(df,file_name)
        data = {'file_link': file_path,'export':'true'}
        return Response(data)
    else:
        for i in range(len(serializer.data)):
            serializer.data[i]['payment_cycle'] = obj['payment_cycle'][i]
        paginator = MyPagination()
        paginated_queryset = paginator.paginate_queryset(serializer.data, request)
        return paginator.get_paginated_response(paginated_queryset)

def ubl_payment(export,query,start_date,end_date,plan,request,url,product):
    obj = cache.get(url+'ubl')
    if obj is None:
        obj = ubl_pay(query, start_date, end_date,plan,product)
        cache.set(url+'ubl', obj) 
        
    serializer = Ubl_Ipg_PaymentsSerializer(obj['data'],many=True)
    if export=='true':
        file_name = f"Ubl_Payments_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        df = pd.DataFrame(serializer.data).to_csv(index=False)
        s3 = upload_csv_to_s3(df,file_name)
        data = {'file_link': file_path,'export':'true'}
        return Response(data)
    else:
        for i in range(len(serializer.data)):
            print(obj['payment_cycle'][i])
            serializer.data[i]['payment_cycle'] = obj['payment_cycle'][i]
        paginator = MyPagination()
        paginated_queryset = paginator.paginate_queryset(serializer.data, request)
        return paginator.get_paginated_response(paginated_queryset)
            
def stripe_payment(export,query,start_date,end_date,plan,request,url,product):
    obj = cache.get(url+'stripe')
    if obj is None:
        obj = stripe_pay(query, start_date, end_date,plan,product)
        cache.set(url+'stripe', obj) 
    serializer = StripePaymentSerializer(obj['data'],many=True)
    if export=='true':
        file_name = f"Stripe_Payments_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        # Build the full path to the media directory
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        df = pd.DataFrame(serializer.data).to_csv(index=False)
        s3 = upload_csv_to_s3(df,file_name)
        data = {'file_link': file_path,'export':'true'}
        return Response(data)
    else:
        for i in range(len(serializer.data)):
            serializer.data[i]['payment_cycle'] = obj['payment_cycle'][i]
        paginator = MyPagination()
        paginated_queryset = paginator.paginate_queryset(serializer.data, request)
        return paginator.get_paginated_response(paginated_queryset)


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

class SearchAlNafiPayments(APIView):
    # permission_classes = [IsAuthenticated]
    # permission_classes = [GroupPermission]
    required_group = 'Sales'
    def get(self, request):
        expiration = self.request.GET.get('expiration_date', None) or None
        q = self.request.GET.get('q', None) or None
        source = self.request.GET.get('source', None) or None
        exact = self.request.GET.get('exact', None) or None
        export = self.request.GET.get('export', None) or None 
        plan = self.request.GET.get('plan', None) or None
        url = request.build_absolute_uri()
        # expired = self.request.GET.get('expired', None) or None
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
        
        # if expired == 'true':
        #     queryset = [obj for obj in queryset if obj.expiration_datetime.date() < date.today()]
                   
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
                print(date_string)
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
            
class SearchPayments(APIView):
    # permission_classes = [IsAuthenticated]
    # permission_classes = [GroupPermission]
    required_group = 'Sales'
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
        
        if origin =='local':
            if source=='easypaisa':
                response = easypaisa_payment(export,query,start_date,end_date,plan,request,url,product)
                return response
                
            elif source == 'ubl':
                response = ubl_payment(export,query,start_date,end_date,plan,request,url,product)
                return response
            else:
                easypaisa = cache.get(url+'easypaisa')
                if easypaisa is None:
                    easypaisa = easypaisa_pay(query, start_date, end_date,plan,product)
                    cache.set(url+'easypaisa', easypaisa)  
                        
                ubl = cache.get(url+'ubl')
                if ubl is None:
                    ubl = ubl_pay(query, start_date, end_date,plan,product)
                    cache.set(url+'ubl', ubl)         
                if export=='true':
                    easypaisa_serializer = Easypaisa_PaymentsSerializer(easypaisa,many=True)
                    ubl_serializer = Ubl_Ipg_PaymentsSerializer(ubl,many=True)
                    
                    df1 = pd.DataFrame(easypaisa_serializer.data)
                    df2 = pd.DataFrame(ubl_serializer.data)
                    
                    # Merge dataframes
                    file_name = f"Payments_DATA_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
                    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                    merged_df = pd.concat([df1, df2], axis=1)
                    df = merged_df.to_csv(index=False)
                    s3 = upload_csv_to_s3(df,file_name)
                    data = {'file_link': file_path,'export':'true'}
                    return Response(data)
                else:   
                    ubl_serializer = Ubl_Ipg_PaymentsSerializer(ubl['data'],many=True)
                    easypaisa_serializer = Easypaisa_PaymentsSerializer(easypaisa['data'],many=True)
                      
                    combined_data = {
                        'data1': ubl_serializer.data,
                        'data2': easypaisa_serializer.data,
                    }
                    serialized_data = LocalPaymentCombinedSerializer(combined_data).data
                    
                    for i in range(len(serialized_data['data1'])):
                         serialized_data['data1'][i]['payment_cycle'] = ubl['payment_cycle'][i]
                         
                    for i in range(len(serialized_data['data2'])):
                        serialized_data['data2'][i]['payment_cycle'] = easypaisa['payment_cycle'][i]
                    
                    combined_queryset = list(chain(serialized_data['data1'], serialized_data['data2']))
                    paginator = MyPagination()
                    paginated_queryset = paginator.paginate_queryset(combined_queryset, request)
                    return paginator.get_paginated_response(paginated_queryset)          
                
                        
        elif origin =='overseas':                
            response = stripe_payment(export,query,start_date,end_date,plan,request,url,product)
            return response
        else:
            if source=='easypaisa':
                response = easypaisa_payment(export,query,start_date,end_date,plan,request,url,product)
                return response
            elif source == 'ubl':
                response = ubl_payment(export,query,start_date,end_date,plan,request,url,product)
                return response
            elif source=='stripe':
                response = stripe_payment(export,query,start_date,end_date,plan,request,url,product)
                return response
            else:
                easypaisa = cache.get(url+'easypaisa')
                if easypaisa is None:
                    easypaisa = easypaisa_pay(query, start_date, end_date,plan,product)
                    cache.set(url+'easypaisa', easypaisa)      
                stripe = cache.get(url+'stripe')
                if stripe is None:
                    stripe = stripe_pay(query, start_date, end_date,plan,product)
                    cache.set(url+'stripe', stripe) 
                ubl = cache.get(url+'ubl')
                if ubl is None:
                    ubl = ubl_pay(query, start_date, end_date,plan,product)
                    cache.set(url+'ubl', ubl)         
                if export=='true':
                    easypaisa_serializer = Easypaisa_PaymentsSerializer(easypaisa,many=True)
                    stripe_serializer = StripePaymentSerializer(stripe,many=True)
                    ubl_serializer = Ubl_Ipg_PaymentsSerializer(ubl,many=True)
                    
                    df1 = pd.DataFrame(easypaisa_serializer.data)
                    df2 = pd.DataFrame(stripe_serializer.data)
                    df3 = pd.DataFrame(ubl_serializer.data)
                    
                    # Merge dataframes
                    file_name = f"Payments_DATA_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
                    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                    merged_df = pd.concat([df1, df2, df3], axis=1)
                    df = merged_df.to_csv(index=False)
                    s3 = upload_csv_to_s3(df,file_name)
                    data = {'file_link': file_path,'export':'true'}
                    return Response(data)
                else:
                    easypaisa_serializer = Easypaisa_PaymentsSerializer(easypaisa['data'],many=True)
                    stripe_serializer = StripePaymentSerializer(stripe['data'],many=True)
                    ubl_serializer = Ubl_Ipg_PaymentsSerializer(ubl['data'],many=True)
                      
                    combined_data = {
                        'data1': stripe_serializer.data,
                        'data2': ubl_serializer.data,
                        'data3': easypaisa_serializer.data,
                    }
                    serialized_data = PaymentCombinedSerializer(combined_data).data
                    for i in range(len(serialized_data['data1'])):
                         serialized_data['data1'][i]['payment_cycle'] = stripe['payment_cycle'][i]
                    
                    for i in range(len(serialized_data['data2'])):
                         serialized_data['data2'][i]['payment_cycle'] = ubl['payment_cycle'][i]
                         
                    for i in range(len(serialized_data['data3'])):
                        serialized_data['data3'][i]['payment_cycle'] = easypaisa['payment_cycle'][i]
                    
                    combined_queryset = list(chain(serialized_data['data1'], serialized_data['data2'], serialized_data['data3']))
                    paginator = MyPagination()
                    paginated_queryset = paginator.paginate_queryset(combined_queryset, request)
                    return paginator.get_paginated_response(paginated_queryset)        
 
class NoOfPayments(APIView):
    # permission_classes = [IsAuthenticated]
    # permission_classes = [GroupPermission]
    required_group = 'Sales'
    def get(self, request):
        source = self.request.GET.get('source', None) or None
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        
        if source=='stripe':
            response_data = stripe_no_payments(start_date,end_date)
        elif source =='ubl':
            response_data = ubl_no_payments(start_date,end_date)
        elif source =='easypaisa':
            response_data = easypaisa_no_payments(start_date,end_date)
        else:
            stripe_payments = stripe_no_payments(start_date,end_date)
            ubl_payments = ubl_no_payments(start_date,end_date)
            easypaisa_payments = easypaisa_no_payments(start_date,end_date)
            response_data = {"stripe_payments": stripe_payments,
                             "ubl_payments": ubl_payments,
                             "easypaisa_payments":easypaisa_payments
                             }
        return Response(response_data)
            
class RenewalNoOfPayments(APIView):
    # permission_classes = [IsAuthenticated]
    # permission_classes = [GroupPermission]
    required_group = 'Sales'
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
        
class PaymentValidation(APIView):
    # permission_classes = [IsAuthenticated]
    # permission_classes = [GroupPermission]
    required_group = 'Sales'
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
        if source == 'ubl':
            ubl = cache.get(url)
            if ubl is None:
                ubl = ubl_payment_validation(time_threshold_str,q)
                cache.set(url, ubl) 
            paginator = MyPagination()
            paginated_queryset = paginator.paginate_queryset(ubl['payments'].data, request)
            return paginator.get_paginated_response(paginated_queryset)
        
        elif source == 'easypaisa':
            easypaisa = cache.get(url)
            if easypaisa is None:
                easypaisa = easypaisa_payment_validation(time_threshold_str,q)
                cache.set(url, easypaisa) 
            paginator = MyPagination()
            print(easypaisa['payments'])
            paginated_queryset = paginator.paginate_queryset(easypaisa['payments'].data, request)
            return paginator.get_paginated_response(paginated_queryset)
        elif source == 'stripe':
            stripe = cache.get(url)
            if stripe is None:
                stripe = stripe_payment_validation(time_threshold_str,q)
                cache.set(url, stripe) 
            paginator = MyPagination()
            paginated_queryset = paginator.paginate_queryset(stripe['payments'].data, request)
            return paginator.get_paginated_response(paginated_queryset)
        else:
            ubl = cache.get(url+'ubl')
            if ubl is None:
                ubl = ubl_payment_validation(time_threshold_str,q)
                cache.set(url+'ubl', ubl) 
                            
            easypaisa = cache.get(url+'easypaisa')
            if easypaisa is None:
                easypaisa = easypaisa_payment_validation(time_threshold_str,q)
                cache.set(url+'easypaisa', easypaisa) 
            
            stripe = cache.get(url+'stripe')
            if stripe is None:
                stripe = stripe_payment_validation(time_threshold_str,q)
                cache.set(url+'stripe', stripe)
                        
            combined_data = {
                    'data1': stripe['payments'].data,
                    'data2': ubl['payments'].data,
                    'data3': easypaisa['payments'].data,
                }
            
            serialized_data = PaymentCombinedSerializer(combined_data).data
            for i in range(len(serialized_data['data1'])):
                serialized_data['data1'][i]['is_valid_payment'] = stripe['valid_payments'][i]
            
            for i in range(len(serialized_data['data2'])):
                serialized_data['data2'][i]['is_valid_payment'] = ubl['valid_payments'][i]
                
            for i in range(len(serialized_data['data3'])):
                serialized_data['data3'][i]['is_valid_payment'] = easypaisa['valid_payments'][i]
                                     
            combined_queryset = list(chain(serialized_data['data1'], serialized_data['data2'],serialized_data['data3']))
            paginator = MyPagination()
            paginated_queryset = paginator.paginate_queryset(combined_queryset, request)
            return paginator.get_paginated_response(paginated_queryset)
        
        
#Creating API For Stripe Payments: 
# class GetAlnafiPayments(APIView):
#     def get(self,request):
#         alnafi_payment = AlNafi_Payment.objects.all()
#         serializer = AlNafiPaymentSerializer(alnafi_payment,many=True)
#         return Response(serializer.data)
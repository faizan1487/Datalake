from rest_framework import status
from user.models import User
from .models import Stripe_Payment, Easypaisa_Payment, UBL_IPG_Payment, AlNafi_Payment
from .serializer import (StripePaymentSerializer, Easypaisa_PaymentsSerializer, Ubl_Ipg_PaymentsSerializer, 
                         AlNafiPaymentSerializer,PaymentCombinedSerializer)
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



def easypaisa_payment(export,query,start_date,end_date,plan,request):
    easypaisa = cache.get('easypaisa_payments')
    if easypaisa is None:
        easypaisa = easypaisa_pay(query, start_date, end_date,plan)
        cache.set('easypaisa_payments', easypaisa) 
    if export=='True':
        easypaisa_serializer = Easypaisa_PaymentsSerializer(easypaisa,many=True)
        file_name = f"Easypaisa_Payments_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        # Build the full path to the media directory
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        df = pd.DataFrame(easypaisa_serializer.data).to_csv(index=False)
        s3 = upload_csv_to_s3(df,file_name)
        data = {'file_link': file_path}
        return Response(data)
    else:
        paginator = MyPagination()
        paginated_queryset = paginator.paginate_queryset(easypaisa, request)
        easypaisa_serializer = Easypaisa_PaymentsSerializer(paginated_queryset,many=True)
        return paginator.get_paginated_response(easypaisa_serializer.data)

def ubl_payment(export,query,start_date,end_date,plan,request):
    ubl = cache.get('ubl_payments')
    if ubl is None:
        ubl = ubl_pay(query, start_date, end_date,plan)
        cache.set('ubl_payments', ubl) 
    if export=='True':
        ubl_serializer = Ubl_Ipg_PaymentsSerializer(ubl,many=True)
        file_name = f"Ubl_Payments_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        df = pd.DataFrame(ubl_serializer.data).to_csv(index=False)
        s3 = upload_csv_to_s3(df,file_name)
        data = {'file_link': file_path}
        return Response(data)
    else:
        paginator = MyPagination()
        paginated_queryset = paginator.paginate_queryset(ubl, request)
        ubl_serializer = Ubl_Ipg_PaymentsSerializer(paginated_queryset,many=True)
        return paginator.get_paginated_response(ubl_serializer.data)
            
def stripe_payment(export,query,start_date,end_date,plan,request):
    stripe = cache.get('stripe_payments')
    if stripe is None:
        stripe = stripe_pay(query, start_date, end_date,plan)
        cache.set('stripe_payments', stripe) 
    if export=='True':
        stripe_serializer = StripePaymentSerializer(stripe,many=True)
        file_name = f"Stripe_Payments_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        # Build the full path to the media directory
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        df = pd.DataFrame(stripe_serializer.data).to_csv(index=False)
        s3 = upload_csv_to_s3(df,file_name)
        data = {'file_link': file_path}
        return Response(data)
    else:
        paginator = MyPagination()
        paginated_queryset = paginator.paginate_queryset(stripe, request)
        stripe_serializer = StripePaymentSerializer(paginated_queryset,many=True)
        return paginator.get_paginated_response(stripe_serializer.data)


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
        if q:
            queryset = AlNafi_Payment.objects.filter(
                Q(customer_email__iexact=q) | Q(product_name__icontains=q)
                |Q(order_id__iexact=q))
        else:
            queryset = AlNafi_Payment.objects.all()  
        if source:
            queryset = queryset.filter(source__iexact=source)
        if plan:
            payment_plan = []
            for obj in queryset:
                product = Alnafi_Product.objects.filter(name=obj.product_name)
                # print(product)
                if plan == 'yearly':
                    for i in product:
                        if i.plan:
                            if i.plan == 'Yearly':
                                payment_plan.append(obj)
                if plan == 'half yearly':
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
                                
            queryset = payment_plan    
            
        if expiration:
            if exact=='True':
                expiration_date = date.today() + timedelta(days=int(expiration))
                query_time = queryset.filter(expiration_datetime__date=expiration_date)
                if export =='True':
                    alnafi_payments_serializer = AlNafiPaymentSerializer(query_time, many=True)
                    file_name = f"Alanfi_Payments_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
                    # Build the full path to the media directory
                    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                    pd.DataFrame(alnafi_payments_serializer.data).to_csv(file_path, index=False)
                    data = {'file_link': file_path}
                    return Response(data)
                else:
                    paginator = MyPagination()
                    paginated_queryset = paginator.paginate_queryset(query_time, request)
                    alnafi_payments_serializer = AlNafiPaymentSerializer(paginated_queryset, many=True)
                    return paginator.get_paginated_response(alnafi_payments_serializer.data)
            else:
                expiration_date = date.today() + timedelta(days=int(expiration))
                query_time = queryset.filter(Q(expiration_datetime__date__gte=date.today()) & Q(expiration_datetime__date__lte=expiration_date))
                if export =='True':
                    alnafi_payments_serializer = AlNafiPaymentSerializer(query_time, many=True)
                    file_name = f"Alanfi_Payments_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
                    # Build the full path to the media directory
                    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                    pd.DataFrame(alnafi_payments_serializer.data).to_csv(file_path, index=False)            
                    data = {'file_link': file_path}
                    return Response(data)
                else:
                    paginator = MyPagination()
                    paginated_queryset = paginator.paginate_queryset(query_time, request)
                    alnafi_payments_serializer = AlNafiPaymentSerializer(paginated_queryset, many=True)
                    return paginator.get_paginated_response(alnafi_payments_serializer.data)
        else:
            if export =='True':
                alnafi_payments_serializer = AlNafiPaymentSerializer(queryset, many=True)
                file_name = f"Alanfi_Payments_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
                # Build the full path to the media directory
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                pd.DataFrame(alnafi_payments_serializer.data).to_csv(file_path, index=False)               
                data = {'file_link': file_path}
                return Response(data)
            else:
                paginator = MyPagination()
                paginated_queryset = paginator.paginate_queryset(queryset, request)
                alnafi_payments_serializer = AlNafiPaymentSerializer(paginated_queryset, many=True)
                return paginator.get_paginated_response(alnafi_payments_serializer.data)
            
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
        
        if origin =='local':
            if source=='easypaisa':
                response = easypaisa_payment(export,query,start_date,end_date,plan,request)
                return response
                
            elif source == 'ubl':
                response = ubl_payment(export,query,start_date,end_date,plan,request)
                return response
            else:
                easypaisa = cache.get('easypaisa_payments')
                if easypaisa is None:
                    easypaisa = easypaisa_pay(query, start_date, end_date,plan)
                    cache.set('easypaisa_payments', easypaisa)      
                ubl = cache.get('ubl_payments')
                if ubl is None:
                    ubl = ubl_pay(query, start_date, end_date,plan)
                    cache.set('ubl_payments', ubl)         
                if export=='True':
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
                    data = {'file_link': file_path}
                    return Response(data)
                else:   
                    queryset = list(easypaisa) + list(ubl)
                    
                    serializer_dict = {
                        Easypaisa_Payment: Easypaisa_PaymentsSerializer,
                        UBL_IPG_Payment: Ubl_Ipg_PaymentsSerializer
                    }
                    
                    paginator = MyPagination()
                    paginated_queryset = paginator.paginate_queryset(queryset, request)
                    serializer = []
                    for obj in paginated_queryset:
                        serializer_class = serializer_dict.get(obj.__class__)
                        serializer.append(serializer_class(obj).data)
                    
                    return paginator.get_paginated_response(serializer)        
                
                        
        elif origin =='overseas':                
            response = stripe_payment(export,query,start_date,end_date,plan,request)
            return response
        else:
            if source=='easypaisa':
                response = easypaisa_payment(export,query,start_date,end_date,plan,request)
                return response
            elif source == 'ubl':
                response = ubl_payment(export,query,start_date,end_date,plan,request)
                return response
            elif source=='stripe':
                response = stripe_payment(export,query,start_date,end_date,plan,request)
                return response
            else:
                easypaisa = cache.get('easypaisa_payments')
                if easypaisa is None:
                    easypaisa = easypaisa_pay(query, start_date, end_date,plan)
                    cache.set('easypaisa_payments', easypaisa)      
                stripe = cache.get('stripe_payments')
                if stripe is None:
                    stripe = stripe_pay(query, start_date, end_date,plan)
                    cache.set('stripe_payments', stripe) 
                ubl = cache.get('ubl_payments')
                if ubl is None:
                    ubl = ubl_pay(query, start_date, end_date,plan)
                    cache.set('ubl_payments', ubl)         
                if export=='True':
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
                    data = {'file_link': file_path}
                    return Response(data)
                else:   
                    queryset = list(easypaisa) + list(stripe) + list(ubl)
                    
                    serializer_dict = {
                        Stripe_Payment: StripePaymentSerializer,
                        Easypaisa_Payment: Easypaisa_PaymentsSerializer,
                        UBL_IPG_Payment: Ubl_Ipg_PaymentsSerializer
                    }
                    
                    paginator = MyPagination()
                    paginated_queryset = paginator.paginate_queryset(queryset, request)
                    serializer = []
                    for obj in paginated_queryset:
                        serializer_class = serializer_dict.get(obj.__class__)
                        serializer.append(serializer_class(obj).data)
                    
                    return paginator.get_paginated_response(serializer)        
 
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
        
        
        
               
#Creating API For Stripe Payments: 
# class GetAlnafiPayments(APIView):
#     def get(self,request):
#         alnafi_payment = AlNafi_Payment.objects.all()
#         serializer = AlNafiPaymentSerializer(alnafi_payment,many=True)
#         return Response(serializer.data)
    
    
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
        if source == 'ubl':
            ubl = cache.get('validated_ubl_payments')
            if ubl is None:
                ubl = ubl_payment_validation(time_threshold_str,q)
                cache.set('validated_ubl_payments', ubl) 
            paginator = MyPagination()
            paginated_queryset = paginator.paginate_queryset(ubl['payments'].data, request)
            return paginator.get_paginated_response(paginated_queryset)
        
        elif source == 'easypaisa':
            easypaisa = cache.get('validated_easypaisa_payments')
            if easypaisa is None:
                easypaisa = easypaisa_payment_validation(time_threshold_str,q)
                cache.set('validated_easypaisa_payments', easypaisa) 
            paginator = MyPagination()
            paginated_queryset = paginator.paginate_queryset(easypaisa['payments'].data, request)
            return paginator.get_paginated_response(paginated_queryset)
        elif source == 'stripe':
            stripe = cache.get('validated_stripe_payments')
            if stripe is None:
                stripe = stripe_payment_validation(time_threshold_str,q)
                cache.set('validated_stripe_payments', stripe) 
            paginator = MyPagination()
            paginated_queryset = paginator.paginate_queryset(stripe['payments'].data, request)
            return paginator.get_paginated_response(paginated_queryset)
        else:
            ubl = cache.get('validated_ubl_payments')
            if ubl is None:
                ubl = ubl_payment_validation(time_threshold_str,q)
                cache.set('validated_ubl_payments', ubl) 
                            
            easypaisa = cache.get('validated_easypaisa_payments')
            if easypaisa is None:
                easypaisa = easypaisa_payment_validation(time_threshold_str,q)
                cache.set('validated_easypaisa_payments', easypaisa) 
            
            stripe = cache.get('validated_stripe_payments')
            if stripe is None:
                stripe = stripe_payment_validation(time_threshold_str,q)
                cache.set('validated_stripe_payments', stripe) 
                        
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
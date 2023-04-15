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
        if q:
            queryset = AlNafi_Payment.objects.filter(
                Q(customer_email__iexact=q) | Q(product_name__icontains=q)
                |Q(order_id__iexact=q))
        else:
            queryset = AlNafi_Payment.objects.all()            
        if source:
            queryset = queryset.filter(source__iexact=source)
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
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        export = self.request.GET.get('export', None) or None
           
        if source=='easypaisa':
            easypaisa_obj = easypaisa_pay(query, start_date, end_date)
            if export=='True':
                easypaisa_serializer = Easypaisa_PaymentsSerializer(easypaisa_obj,many=True)
                csv_link = json_to_csv(easypaisa_serializer, 'easypaisa')
                data = {'file_link': csv_link}
                return Response(data)
                return Response(csv_link)
            else:
                paginator = MyPagination()
                paginated_queryset = paginator.paginate_queryset(easypaisa_obj, request)
                easypaisa_serializer = Easypaisa_PaymentsSerializer(paginated_queryset,many=True)
                return paginator.get_paginated_response(easypaisa_serializer.data)
        elif source=='stripe':
            stripe_obj = stripe_pay(query, start_date, end_date)
            if export=='True':
                stripe_serializer = StripePaymentSerializer(stripe_obj,many=True)
                csv_link = json_to_csv(stripe_serializer, 'stripe')
                data = {'file_link': csv_link}
                return Response(data)
            else:
                paginator = MyPagination()
                paginated_queryset = paginator.paginate_queryset(stripe_obj, request)
                stripe_serializer = StripePaymentSerializer(paginated_queryset,many=True)
                return paginator.get_paginated_response(stripe_serializer.data)
        elif source == 'ubl':
            ubl_obj = ubl_pay(query, start_date, end_date)
            if export=='True':
                ubl_serializer = Ubl_Ipg_PaymentsSerializer(ubl_obj,many=True)
                csv_link = json_to_csv(ubl_serializer, 'ubl')
                data = {'file_link': csv_link}
                return Response(data)
            else:
                paginator = MyPagination()
                paginated_queryset = paginator.paginate_queryset(ubl_obj, request)
                ubl_serializer = Ubl_Ipg_PaymentsSerializer(paginated_queryset,many=True)
                return paginator.get_paginated_response(ubl_serializer.data)
        else:
            if export=='True':
                easypaisa_obj = easypaisa_pay(query, start_date, end_date)
                stripe_obj = stripe_pay(query, start_date, end_date)
                ubl_obj = ubl_pay(query, start_date, end_date)
                
                easypaisa_serializer = Easypaisa_PaymentsSerializer(easypaisa_obj,many=True)
                stripe_serializer = StripePaymentSerializer(stripe_obj,many=True)
                ubl_serializer = Ubl_Ipg_PaymentsSerializer(ubl_obj,many=True)
                
                df1 = pd.DataFrame(easypaisa_serializer.data)
                df2 = pd.DataFrame(stripe_serializer.data)
                df3 = pd.DataFrame(ubl_serializer.data)
                
                # Merge dataframes
                file_name = f"Payments_DATA_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                merged_df = pd.concat([df1, df2, df3], axis=1)
                merged_df.to_csv(file_path, index=False)
                data = {'file_link': file_path}
                return Response(data)
            else:   
                easypaisa_obj = easypaisa_pay(query, start_date, end_date)
                stripe_obj = stripe_pay(query, start_date, end_date)
                ubl_obj = ubl_pay(query, start_date, end_date) 
                
                queryset = list(easypaisa_obj) + list(stripe_obj) + list(ubl_obj)
                
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
            ubl_pay = ubl_payment_validation(time_threshold_str,q)
            paginator = MyPagination()
            paginated_queryset = paginator.paginate_queryset(ubl_pay.data, request)
            return paginator.get_paginated_response(paginated_queryset)
        
        elif source == 'easypaisa':
            easypaisa_pay = easypaisa_payment_validation(time_threshold_str,q)   
            paginator = MyPagination()
            paginated_queryset = paginator.paginate_queryset(easypaisa_pay.data, request)
            return paginator.get_paginated_response(paginated_queryset)
            # return Response(response_data)  
        elif source == 'stripe':
            stripe_pay = stripe_payment_validation(time_threshold_str,q)
            paginator = MyPagination()
            paginated_queryset = paginator.paginate_queryset(stripe_pay.data, request)
            return paginator.get_paginated_response(paginated_queryset)
            # return Response(response_data)
        else:
            ubl_pay = ubl_payment_validation(time_threshold_str,q)
            easypaisa_pay = easypaisa_payment_validation(time_threshold_str,q)
            stripe_pay = stripe_payment_validation(time_threshold_str,q)
                        
            combined_data = {
                    'data1': stripe_pay.data,
                    'data2': ubl_pay.data,
                    'data3': easypaisa_pay.data,
                }
            
            serialized_data = PaymentCombinedSerializer(combined_data).data
            combined_queryset = list(chain(serialized_data['data1'], serialized_data['data2'],serialized_data['data3']))
            paginator = MyPagination()
            paginated_queryset = paginator.paginate_queryset(combined_queryset, request)
            return paginator.get_paginated_response(paginated_queryset)
           
from rest_framework import status
from user.models import User
from .models import Stripe_Payment, Easypaisa_Payment, UBL_IPG_Payment, AlNafi_Payment, NavbarLink
from .serializer import (StripePaymentSerializer, Easypaisa_PaymentsSerializer, Ubl_Ipg_PaymentsSerializer, 
                         AlNafiPaymentSerializer)
from .services import easypaisa_pay, ubl_pay, stripe_pay, json_to_csv
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta, date
from django.db.models import Q
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.models import Group
import os
import pandas as pd
from rest_framework.permissions import BasePermission
from user.services import GroupPermission
class MyPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100           

# delete this api before production
class AlnafiPayment(APIView):
    def post(self, request):
        data = request.data
        serializer = AlNafiPaymentSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Navbar(APIView):
    def get(self,request):
        user = request.user
        sales = Group.objects.get(name='Sales')
        support = Group.objects.get(name='Support')
        support_user = User.objects.filter(groups__name=support.name, email__iexact=user.email)
        sales_user = User.objects.filter(groups__name=sales.name, email__iexact=user.email)
        if support_user:
            obj = NavbarLink.objects.filter(group='Support')
        elif sales_user:
            obj = NavbarLink.objects.filter(group='Sales')
            
        serializer = NavbarSerializer(obj, many=True)
        return Response(serializer.data)

class SearchAlNafiPayments(APIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [GroupPermission]
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
                
                if export =='true':
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
                
                if export =='true':
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
            if export =='true':
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
    permission_classes = [IsAuthenticated]
    permission_classes = [GroupPermission]
    required_group = 'Sales'
    def get(self, request):
        query = self.request.GET.get('q', None) or None
        source = self.request.GET.get('source', None) or None
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        export = self.request.GET.get('export', None) or None
           
        if source=='easypaisa':
            easypaisa_obj = easypaisa_pay(query, start_date, end_date)
            if export=='true':
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
            if export=='true':
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
            if export=='true':
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
            if export=='true':
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
        
#Creating API For Stripe Payments: 
class GetStripePayments(APIView):
    def get(self,request):
        pay = Stripe_Payment.objects.all()
        serializer = StripePaymentSerializer(pay,many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        serializer = StripePaymentSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
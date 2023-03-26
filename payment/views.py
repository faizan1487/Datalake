from django.shortcuts import render
from .models import Stripe_Payment, Easypaisa_Payment, UBL_IPG_Payment
from .serializer import StripePaymentSerializer, Easypaisa_PaymentsSerializer, Ubl_Ipg_PaymentsSerializer
from .services import easypaisa_pay, ubl_pay, stripe_pay
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
import csv

class Import_csv(APIView):
    def post(self, request):
        csv_file = self.request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        for row in reader:
            Stripe_Payment.objects.create(
                payment_id=row['payment_id'],
                name=row['name'],
                customer_email=row['email'],
                product_name = row['product'],
                amount = row['amount'],
                order_datetime = row['created'],
                status = row['status'],
                currency = row['currency'],
                source = row['source'],
                description = row['description'],
                address = row['address']
            )
            
        return Response("Data added")

class MyPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100           


class GetUserPayments(APIView):
    def get(self, request):
        query = self.request.GET.get('q')
                

class SearchPayments(APIView):
    def get(self, request):
        query = self.request.GET.get('q')
        source = self.request.GET.get('source')
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
           
        if source=='easypaisa':
            easypaisa_obj = easypaisa_pay(query, start_date, end_date, source)
            paginator = MyPagination()
            paginated_queryset = paginator.paginate_queryset(easypaisa_obj, request)
            easypaisa_serializer = Easypaisa_PaymentsSerializer(paginated_queryset,many=True)
            return paginator.get_paginated_response(easypaisa_serializer.data)
        elif source=='stripe':
            stripe_obj = stripe_pay(query, start_date, end_date, source)
            paginator = MyPagination()
            paginated_queryset = paginator.paginate_queryset(stripe_obj, request)
            stripe_serializer = StripePaymentSerializer(paginated_queryset,many=True)
            return paginator.get_paginated_response(stripe_serializer.data)
        elif source == 'ubl':
            ubl_obj = ubl_pay(query, start_date, end_date, source)
            paginator = MyPagination()
            paginated_queryset = paginator.paginate_queryset(ubl_obj, request)
            ubl_serializer = Ubl_Ipg_PaymentsSerializer(paginated_queryset,many=True)
            return paginator.get_paginated_response(ubl_serializer.data)
        else:
            easypaisa_obj = easypaisa_pay(query, start_date, end_date, source)
            stripe_obj = stripe_pay(query, start_date, end_date, source)
            ubl_obj = ubl_pay(query, start_date, end_date, source) 
            
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
    
#Creating API For ubl_ipg Payments:
class GetUBLPayments(APIView):
    def get(self,request):
        ubl_pay = UBL_IPG_Payment.objects.all()
        serializer = Ubl_Ipg_PaymentsSerializer(ubl_pay, many=True)
        return Response(serializer.data)


    
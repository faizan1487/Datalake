from cgi import print_directory
from xxlimited import new
from django.utils import timezone
from sre_constants import SUCCESS
from tracemalloc import start
from rest_framework import status

from .models import Stripe_Payment, Easypaisa_Payment, UBL_IPG_Payment, AlNafi_Payment,Main_Payment,UBL_Manual_Payment, New_Alnafi_Payments,Renewal, Unpaid_New_Alnafi_Payments
from .serializer import (Easypaisa_PaymentsSerializer, Ubl_Ipg_PaymentsSerializer, AlNafiPaymentSerializer,MainPaymentSerializer,
                         UBL_Manual_PaymentSerializer, New_Al_Nafi_Payments_Serializer,Unpaid_New_Al_Nafi_Payments_Serializer)
from .services import (renewal_no_of_payments,main_no_of_payments,no_of_payments,get_USD_rate,get_pkr_rate)
from user.models import Moc_Leads
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta, date
from django.db.models import Q
from django.db.models import Case, Value, When, BooleanField


from django.http import HttpResponse
import os
from django.core.cache import cache

import numpy as np
import json
from django.db.models.functions import Upper
from threading import Thread
from collections import defaultdict, OrderedDict
from django.db.models import Q, Value, Case, When, CharField
import pandas as pd
from django.conf import settings
from user.services import upload_csv_to_s3
import requests
from user.constants import COUNTRY_CODES
from secrets_api.algorithem import round_robin, round_robin_support
import math

import csv
from django.http import JsonResponse

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


class MyPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100           


class NewAlnafiPayment(APIView):
    def post(self, request):
        data = request.data
        # print(data)
        order_id = data.get('orderId')
        # print(order_id)

        try:
            instance = New_Alnafi_Payments.objects.filter(orderId=order_id)            
            serializer = New_Al_Nafi_Payments_Serializer(instance.first(), data=data)
        except:
            serializer = New_Al_Nafi_Payments_Serializer(data=data)

        
        if serializer.is_valid():
            serializer.save()
            # print("valid")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UnpaidNewAlnafiPayment(APIView):
    def post(self, request):
        data = request.data
        order_id = data.get('orderId')

        if data['status'] == 'paid':
            instance = Unpaid_New_Alnafi_Payments.objects.filter(orderId=order_id)
            instance.delete()
            return Response("instance deleted")
        else:
            try:
                instance = Unpaid_New_Alnafi_Payments.objects.filter(orderId=order_id)            
                serializer = Unpaid_New_Al_Nafi_Payments_Serializer(instance.first(), data=data)
            except:
                serializer = Unpaid_New_Al_Nafi_Payments_Serializer(data=data)

            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# delete this api before production
class AlnafiPayment(APIView):
    def get(self, request):
        Thread(target=self.get_thread, args=(request,)).start()
        return HttpResponse("working")

    def get_thread(self,request):
        ids = self.request.GET.get('id', None) or None
        if ids:
            id = ids.split(',')
            payments = AlNafi_Payment.objects.filter(id__in=id)
        else:
            payments = AlNafi_Payment.objects.all()

        for payment in payments:
            # print(payment)
            payment.save()
    
    def post(self, request):
        data = request.data
        payment_id = data.get('payment_id')
        # print(payment_id)

        try:
            instance = AlNafi_Payment.objects.filter(payment_id=payment_id)
            # print(instance)
            serializer = AlNafiPaymentSerializer(instance.first(), data=data)
        except:
            serializer = AlNafiPaymentSerializer(data=data)

        
        if serializer.is_valid():
            serializer.save()
            # print("valid")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UBLManualPayment(APIView):
    def get(self, request):
        Thread(target=self.get_thread, args=(request,)).start()
        return HttpResponse("working")

    def get_thread(self,request):
        ids = self.request.GET.get('id', None) or None
        if ids:
            id = ids.split(',')
            payments = UBL_Manual_Payment.objects.filter(transaction_id__in=id)
        else:
            payments = UBL_Manual_Payment.objects.all()

        for payment in payments:
            # print(payment)
            payment.save()
    
    def post(self, request):
        data = request.data
        transaction_id = data.get('transaction_id')

        try:
            instance = UBL_Manual_Payment.objects.filter(transaction_id=transaction_id)
            serializer = UBL_Manual_PaymentSerializer(instance.first(), data=data)
        except:
            serializer = UBL_Manual_PaymentSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Creating API For ubl_ipg Payments:
class GetUBLIPGPayments(APIView):
    def get(self, request):
        Thread(target=self.get_thread, args=(request,)).start()
        return HttpResponse("working")

    def get_thread(self,request):
        ids = self.request.GET.get('id', None) or None
        if ids:
            id = ids.split(',')
            payments = UBL_IPG_Payment.objects.filter(transaction_id__in=id)
        else:
            payments = UBL_IPG_Payment.objects.all()

        for payment in payments:
            # print(payment)
            payment.save()
    
    def post(self, request):
        data = request.data
        serializer = Ubl_Ipg_PaymentsSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Creating API For Easypaisa Payments
class GetEasypaisaPayments(APIView):
    def get(self, request):
        Thread(target=self.get_thread, args=(request,)).start()
        return HttpResponse("working")

    def get_thread(self,request):
        ids = self.request.GET.get('id', None) or None
        if ids:
            id = ids.split(',')
            payments = Easypaisa_Payment.objects.filter(transaction_id__in=id)
        else:
            payments = Easypaisa_Payment.objects.all()

        for payment in payments:
            # print(payment)
            payment.save()
    
    def post(self, request):
        data = request.data
        serializer = Easypaisa_PaymentsSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetStripePayments(APIView):
    def get(self, request):
        Thread(target=self.get_thread, args=(request,)).start()
        return HttpResponse("working")

    def get_thread(self,request):
        ids = self.request.GET.get('id', None) or None
        if ids:
            id = ids.split(',')
            payments = Stripe_Payment.objects.filter(payment_id__in=id)
        else:
            payments = Stripe_Payment.objects.all()

        for payment in payments:
            # print(payment)
            payment.save()



#NEW
#product issue and response time fixed
#class SearchAlnafiPayment 
class RenewalPayments(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # print("renewal payment function")
        expiration = self.request.GET.get('expiration_date', None) or None
        q = self.request.GET.get('q', None) or None
        exact = self.request.GET.get('exact', None) or None
        export = self.request.GET.get('export', None) or None
        plan = self.request.GET.get('plan', None) or None
        active = self.request.GET.get('is_active', None) or None
        product = self.request.GET.get('product', None) or None

        page = int(self.request.GET.get('page', 1))
        page_size = 10  # Number of payments per page

        # Calculate the start and end indices for slicing
        start_index = (page - 1) * page_size
        end_index = start_index + page_size

       
        payments = Main_Payment.objects.filter(source__in=['Al-Nafi','NEW ALNAFI']).exclude(
            user__email__endswith="yopmail.com"
            ).select_related(
                'product').values()
        
        

        if q:
            payments = payments.filter(Q(user__email__icontains=q) | Q(amount__iexact=q))            
            

        if product:
            products_list = product.split(',')
            if len(products_list) > 1:
                payments = payments.filter(product__product_name__in=products_list)
                # payments = payments.distinct()
            else:
                payments = payments.filter(product__product_name__in=products_list)
                # payments = payments.distinct()








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
            payments = payments.exclude(Q(payment_cycle__exact='') | Q(payment_cycle__isnull=True))
        

        # queries increasing when trying to implement multiple plan filter logic

        # if plan:
        #     # Split the source string into a list if it contains a comma
        #     plans_list = plan.split(',')

        #     # If there is more than one source, filter payments using each source
        #     if len(plans_list) > 1:
        #         payments = payments.filter(product__product_plan__in=plans_list)
        #         payments = payments.distinct()
        #     else:
        #         # If there is only one source, filter payments using that single source
        #         payments = payments.filter(product__product_plan=plan)
        #         payments = payments.distinct()
        # else:
        #     payments = payments.exclude(Q(payment_cycle__exact='') | Q(payment_cycle__isnull=True))

        total_count = payments.count()  # Calculate the total count of payments

        payments = payments[start_index:end_index]

        for i, data in enumerate(payments):
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
            removed_duplicates = self.remove_duplicate_payments(payment_list)
            file_name = f"Payments_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            df = pd.DataFrame(removed_duplicates).to_csv(index=False)
            s3 = upload_csv_to_s3(df, file_name)
            data = {'file_link': file_path, 'export': 'true'}
            return Response(data)
        else:
            payment_json = json.dumps(payment_list, default=json_serializable)  # Serialize the list to JSON with custom encoder
            payment_objects = json.loads(payment_json)
            
            removed_duplicated = self.remove_duplicate_payments(payment_objects)
            num_pages = (total_count + page_size - 1) // page_size
            return Response({
                'count': total_count,
                'num_pages': num_pages,
                'results': removed_duplicated,
            })

    def remove_duplicate_payments(self,payments):
        payment_list = []
        
        for payment in payments:
            payment_id = payment['id']
            payment_found = False

            for existing_payment in payment_list:
                # print(existing_payment)
                if existing_payment['id'] == payment_id:
                    # If payment with the same id exists in the list, append the product name
                    existing_payment['product_names'].append(payment['product_id'])
                    existing_payment['plan'].append(payment['payment_cycle'])
                    payment_found = True
                    break

            if not payment_found:
                # print(payment)
                # If payment is not found in the list, create a new entry

                payment_data = {
                    'id': payment['id'],
                    'user_id': payment['user_id'],
                    'phone': payment['phone'],
                    'source': payment['source'],
                    'amount': payment['amount'],
                    'product_names': [payment['product_id']],
                    'plan': [payment['payment_cycle']],
                    'alnafi_payment_id': payment['alnafi_payment_id'],
                    'card_mask': payment['card_mask'],
                    'order_datetime': payment['order_datetime'],
                    'expiry_datetime': payment['expiration_datetime'],
                    'order_id': payment['source_payment_id'],
                    'qarz_e_hasna': payment['qarz'],
                    'is_active': payment['is_active'],
                }
                payment_list.append(payment_data)
        
        return payment_list

#product issue and response time fixed
class ActivePayments(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        q = self.request.GET.get('q', None) or None
        export = self.request.GET.get('export', None) or None
        plan = self.request.GET.get('plan', None) or None
        product = self.request.GET.get('product', None) or None
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None

        payments = Main_Payment.objects.filter(source__in=['Al-Nafi','NEW ALNAFI']).exclude(user__email__endswith="yopmail.com").select_related('product').values()
        payments = payments.filter(expiration_datetime__date__gt=date.today())

        if payments:
            if not start_date:
                first_payment = min(payments, key=lambda obj: obj['expiration_datetime'])
                start_date = first_payment['expiration_datetime'].date() if first_payment else None

            if not end_date:
                last_payment = max(payments, key=lambda obj: obj['expiration_datetime'])
                end_date = last_payment['expiration_datetime'].date() if last_payment else None

            payments = payments.filter(Q(expiration_datetime__date__gte=start_date) & Q(expiration_datetime__date__lte=end_date))

            if q:
                payments = payments.filter(user__email__icontains=q) 
                

            if product:
                products_list = product.split(',')
                if len(products_list) > 1:
                    payments = payments.filter(product__product_name__in=products_list)
                else:
                    payments = payments.filter(product__product_name__in=products_list)
    
            payments = payments.annotate(payment_cycle=Upper('product__product_plan'))
        
            # if plan:
            #     plans_list = plan.split(',')

            #     if len(plans_list) > 1:
            #         payments = payments.filter(product__product_plan__in=plans_list)
            #         payments = payments.distinct()
            #     else:
            #         payments = payments.filter(product__product_plan=plan)
            #         payments = payments.distinct()
            # else:
            #     payments = payments.exclude(Q(payment_cycle__exact='') | Q(payment_cycle__isnull=True))

            plan_mapping = {
                'yearly': 'Yearly',
                'halfyearly': 'Half Yearly',
                'quarterly': 'Quarterly',
                'monthly': 'Monthly',
            }

            if plan:
                if plan.lower() != 'all':
                    payments = payments.filter(
                        Q(product__product_plan__iexact=plan) | Q(product__product_plan__iexact=plan_mapping.get(plan, ''))
                    )            
            else:
                payments = payments.exclude(Q(payment_cycle__exact='') | Q(payment_cycle__isnull=True))

            if export == 'true':
                for i, data in enumerate(payments):
                    date_string = payments[i]['expiration_datetime']
                    if date_string:
                        payments[i]['is_active'] = date_string.date() >= date.today()
                    else:
                        payments[i]['is_active'] = False

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

                removed_duplicates = self.remove_duplicate_payments(payment_list)
                file_name = f"Payments_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                df = pd.DataFrame(removed_duplicates).to_csv(index=False)
                s3 = upload_csv_to_s3(df, file_name)
                data = {'file_link': file_path, 'export': 'true'}
                return Response(data)

            page = int(self.request.GET.get('page', 1))
            page_size = 10  # Number of payments per page

            # Calculate the start and end indices for slicing
            start_index = (page - 1) * page_size
            end_index = start_index + page_size
            total_count = payments.count()  # Calculate the total count of payments
            payments = payments[start_index:end_index]
         
            for i, data in enumerate(payments):
                date_string = payments[i]['expiration_datetime']
                if date_string:
                    payments[i]['is_active'] = date_string.date() >= date.today()
                else:
                    payments[i]['is_active'] = False

            user_groups = request.user.groups.values_list('name', flat=True)  # Get the names of all user groups
            has_perm = False
            for i in user_groups:
                if i == 'Admin' or i == 'MOC':
                    has_perm = True
                    break
            
            if has_perm:
                pass
            else:
                if q:
                    payments = payments.filter(user__email__iexact=q)
                    for i, data in enumerate(payments):
                        date_string = payments[i]['expiration_datetime']
                        if date_string:
                            payments[i]['is_active'] = date_string.date() >= date.today()
                        else:
                            payments[i]['is_active'] = False
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
                    # print(payment_list)
                    removed_duplicate = self.remove_duplicate_payments(payment_list)
                    return Response(removed_duplicate)
                else:
                    return Response("Please enter email")
            
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
       
            def json_serializable(obj):
                    if isinstance(obj, datetime):
                        return obj.isoformat()  # Convert datetime to ISO 8601 format
                    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

            payment_json = json.dumps(payment_list, default=json_serializable)  # Serialize the list to JSON with custom encoder
            payment_objects = json.loads(payment_json)                
            removed_duplicates = self.remove_duplicate_payments(payment_objects)
            num_pages = (total_count + page_size - 1) // page_size

            user_groups = request.user.groups.values_list('name', flat=True)  # Get the names of all user groups
            has_perm = False
            for i in user_groups:
                if i == 'Admin' or i == 'MOC':
                    has_perm = True
                    break

            if has_perm:
                return Response({
                    'count': total_count,
                    'num_pages': num_pages,
                    'results': removed_duplicates,
                })
            else:
                return Response("no data")  
        else:
            return Response("No data")


    def remove_duplicate_payments(self,payments):
        payment_list = []
        
        for payment in payments:
            # print(payment)
            payment_id = payment['id']
            payment_found = False

            for existing_payment in payment_list:
                # print(existing_payment)
                if existing_payment['id'] == payment_id:
                    # If payment with the same id exists in the list, append the product name
                    existing_payment['product_names'].append(payment['product_id'])
                    existing_payment['plan'].append(payment['payment_cycle'])
                    payment_found = True
                    break

            if not payment_found:
                # print(payment)
                # If payment is not found in the list, create a new entry

                payment_data = {
                    'id': payment['id'],
                    'user_id': payment['user_id'],
                    'phone': payment['phone'],
                    'source': payment['source'],
                    'amount': payment['amount'],
                    'product_names': [payment['product_id']],
                    'plan': [payment['payment_cycle']],
                    'alnafi_payment_id': payment['alnafi_payment_id'],
                    'card_mask': payment['card_mask'],
                    'order_datetime': payment['order_datetime'],
                    'expiry_datetime': payment['expiration_datetime'],
                    'order_id': payment['source_payment_id'],
                    'qarz_e_hasna': payment['qarz'],
                    'is_active': payment['is_active'],
                }
                payment_list.append(payment_data)
        
        return payment_list


       
#Optimized
#shows no of payments on each date
class NoOfPayments(APIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [GroupPermission]
    # required_groups = ['Sales', 'Admin']
    def get(self, request):
        source = self.request.GET.get('source', None) or None
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        
        payments = main_no_of_payments(start_date,end_date,source)
        response_data = {"payments": payments}
        return Response(response_data)
    

class TotalNoOfPayments(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        source = self.request.GET.get('source', None) or None
        
        payments = no_of_payments(source)
        # response_data = {"payments": payments}
        return Response(payments)


#Optimized
#shows alnafi/mainsite no of payments on each date
class RenewalNoOfPayments(APIView):
    permission_classes = [IsAuthenticated]
    # permission_classes = [GroupPermission]
    # required_groups = ['Sales', 'Admin']
    def get(self, request):
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        payments = Main_Payment.objects.exclude(user__email__endswith="yopmail.com").filter(source='Al-Nafi')
        response_data = renewal_no_of_payments(payments)
        return Response(response_data)
        


# PRODUCTION
class SearchPayments(APIView):
    permission_classes = [IsAuthenticated]   
    # Define the sources list here
    def get(self, request):
        query = self.request.GET.get('q', None)
        origin = self.request.GET.get('origin', None)
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)
        export = self.request.GET.get('export', None)
        plan = self.request.GET.get('plan', None)
        product = self.request.GET.get('product', None)
        status = self.request.GET.get('status', None)
        page = int(self.request.GET.get('page', 1))
        source = self.request.GET.get('source', None)

        payments= search_payment(export, query, start_date, end_date, plan, source, origin, status,product,page)
        if export == 'true':
            return Response(payments)
        if payments['success']:
            total_count = payments['total_count']
            total_payments_in_usd = payments['total_payments_in_usd'] 
            total_payments_in_pkr = payments['total_payments_in_pkr']
            payments = self.process_payments(payments['payments'], export,product,plan)
            
            # Calculate the number of pages
            num_pages = (total_count + 10 - 1) // 10
            return Response({
                'count': total_count,
                'num_pages': num_pages,
                'total_payments_pkr': total_payments_in_pkr,
                'total_payments_usd': total_payments_in_usd,
                'payments': payments['payments'],
            })
        else:
            payments = []
            return Response(payments)
        
    def process_payments(self,payments,export,product,plan):
        payment_list = []
        # print(payments)
        for payment in payments:
            # print(payment)
            payment_id = payment['id']
            # print("payment_id",payment_id)

            payment_found = False

            for existing_payment in payment_list:
                if existing_payment['id'] == payment_id:
                    payment_found = True
                    break

            if not payment_found:
                # print("payment not found")
                payment_data = {
                    'id': payment['id'],
                    'user_id': payment['user'],
                    'phone': payment['user_phone'],
                    'source': payment['source'],
                    'currency': payment['currency'],
                    'amount': payment['amount'],
                    'converted_in_usd': payment['converted_in_usd'],
                    'two_percent_deduction': payment['two_percent_deduction'],
                    'after_deduction_amount': payment['after_deduction_amount'],
                    'product_names': payment['product'],
                    'plans': payment['plan'],
                    'alnafi_payment_id': payment['alnafi_payment_id'],
                    'source_payment_id': payment['source_payment_id'],
                    'card_mask': payment['card_mask'],
                    'order_datetime': payment['order_datetime'].isoformat(),
                    'internal_source': payment['internal_source']
                }

                # print(payment_data)
                payment_list.append(payment_data)



        return {
            'payments': payment_list,
            "count": len(payment_list)
        }

   
# PRODUCTION
# bug, only 3 payments showing up instead of 10 
def search_payment(export, q, start_date, end_date, plan, source, origin, status,product,page):
    payments = Main_Payment.objects.exclude(
        user__email__endswith="yopmail.com"
    ).exclude(
        source='UBL_DD', status__in=["0", False, 0]
    ).filter(
        Q(source__in=['Easypaisa', 'UBL_IPG', 'UBL_DD', 'Stripe']) | Q(source='NEW ALNAFI', internal_source__contains='dlocal')
    )

    if status:
        payments = payments.filter(status=status)
    
    if source:
        # Split the source string into a list if it contains a comma
        sources_list = source.split(',')
        if 'dlocal' in sources_list:
            if len(sources_list) > 1:
                payments = payments.filter(Q(source__in=sources_list) | Q(source='NEW ALNAFI', internal_source__contains='dlocal'))
            else:
                payments = payments.filter(Q(source=source) | Q(source='NEW ALNAFI', internal_source__contains='dlocal'))
        else:
            if len(sources_list) > 1:
                payments = payments.filter(source__in=sources_list)
            else:
                payments = payments.filter(source=source)


    if origin:
        if not payments:
            total_count = payments.count() 
            payments = {"payments": payments, "success": False,"total_count":total_count}
            return payments
        else:
            if origin == 'local':
                payments = payments.filter(source__in=['Easypaisa', 'UBL_IPG', 'UBL_DD'])
            else:
                payments = payments.filter(source='Stripe')

    if not start_date:
        if not payments:
            total_count = payments.count() 
            payments = {"payments": payments, "success": False,"total_count":total_count}
            return payments
        else:
            first_payment = payments.exclude(order_datetime=None).last()
            start_date = first_payment.order_datetime.date() if first_payment else None

    if not end_date:
        if not payments:
            total_count = payments.count() 
            payments = {"payments": payments, "success": False,"total_count":total_count}
            return payments
        else:
            last_payment = payments.exclude(order_datetime=None).first()
            end_date = last_payment.order_datetime.date() if last_payment else None

    if not payments:
        total_count = payments.count() 
        payments = {"payments": payments, "success": False,"total_count":total_count}
        return payments
    else:
        payments = payments.filter(Q(order_datetime__date__lte=end_date, order_datetime__date__gte=start_date))

    if q:
        payments = payments.filter(user__email__icontains=q)

    if product:
        products_list = product.split(',')
        # If there is more than one source, filter payments using each source
        if len(products_list) > 1:
            payments = payments.filter(product__product_name__in=products_list)
            payments = payments.distinct()
        else:
            # If there is only one source, filter payments using that single source
            payments = payments.filter(product__product_name__in=products_list)
            payments = payments.distinct()

    if plan:
        # Split the source string into a list if it contains a comma
        plans_list = plan.split(',')

        # If there is more than one source, filter payments using each source
        if len(plans_list) > 1:
            payments = payments.filter(product__product_plan__in=plans_list)
            payments = payments.distinct()
        else:
            # If there is only one source, filter payments using that single source
            payments = payments.filter(product__product_plan=plan)
            payments = payments.distinct()


    payment_cycle = payments.values_list('product__product_plan', flat=True).distinct()
    payment_cycle_descriptions = {
        'Monthly': 'Monthly',
        'Yearly': 'Yearly',
        'Half Yearly': 'Half-Yearly',
        'Quarterly': 'Quarterly'
        # Add more plan-value pairs as needed
    }

    payments = payments.annotate(
        payment_cycle=Case(
            *[When(product__product_plan=plan, then=Value(description)) for plan, description in payment_cycle_descriptions.items()],
            default=Value('Unknown Plan'),
            output_field=CharField()
        )
    )

    page_size = 10  # Number of payments per page

    # Calculate the start and end indices for slicing
    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    total_count = payments.count()  # Calculate the total count of payments


    if export == 'true':
        payments_data = payments.values('user__email', 'user__phone', 'product__product_name', 'source', 'amount','currency','order_datetime', 'id','payment_cycle','alnafi_payment_id','card_mask','source_payment_id')
        
        payments = [{'user': payment['user__email'],
                     'user_phone': payment['user__phone'], 
                     'product': payment['product__product_name'],
                     'plan': payment['payment_cycle'],
                     'source': payment['source'],
                     'amount': payment['amount'],
                     'alnafi_payment_id':payment['alnafi_payment_id'], 
                     'order_datetime': payment['order_datetime'],
                     'card_mask': payment['card_mask'], 
                     'id': payment['id'],
                     'currency': payment['currency'],
                     'source_payment_id':payment['source_payment_id']} for payment in payments_data]
        payment_list = []
        for payment in payments:
            payment_id = payment['id']
            payment_found = False
            
            for existing_payment in payment_list:
                if existing_payment['id'] == payment_id:
                    payment_found = True
                    break

            if not payment_found:
                payment_data = {
                    'id': payment['id'],
                    'user_id': payment['user'],
                    'phone': payment['user_phone'],
                    'source': payment['source'],
                    'amount': payment['amount'],
                    'currency': payment['currency'],
                    'product_names': [payment['product']],
                    'plans': [payment['plan']],
                    'alnafi_payment_id': payment['alnafi_payment_id'],
                    'source_payment_id': payment['source_payment_id'],
                    'card_mask': payment['card_mask'],
                    'order_datetime': payment['order_datetime'].isoformat(),
                }
                payment_list.append(payment_data)



        file_name = f"Payments_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        df = pd.DataFrame(payment_list).to_csv(index=False)
        s3 = upload_csv_to_s3(df, file_name)
        data = {'file_link': file_path, 'export': 'true'}
        return data


    sources = ['ubl_dd', 'al-nafi', 'easypaisa', 'ubl_ipg']
    total_payments_in_usd = 0
    for p in payments:
        amount = p.amount
        # country_name = p.user.country
        # if country_name:
        #     amount, tax = add_tax_stripe_according_to_the_country_code(amount,country_name.upper())
        if p.source.lower() not in sources:
            if p.currency.lower() == 'pkr' or p.currency.lower() == 'PKR':
                p.converted_amount = 0
                p.amount_after_deduction = amount
                p.deducted_amount = 0
            elif p.currency.lower() != 'usd':
                # print("in elif")
                currency_rate = get_USD_rate(p.currency,amount)
                converted_amount = round(int(amount) / currency_rate[p.currency],6)
                p.converted_amount = converted_amount
                p.deducted_amount = 0.02 * converted_amount
                converted_amount = converted_amount - (0.02 * converted_amount)
                p.amount_after_deduction = converted_amount
                total_payments_in_usd += converted_amount
            else:
                p.converted_amount = amount
                p.amount_after_deduction = amount
                p.deducted_amount = 0
                total_payments_in_usd += int(amount)
        else:
            p.converted_amount = 0
            p.amount_after_deduction = amount
            p.deducted_amount = 0


    total_payments_in_pkr = sum(float(p.amount) for p in payments if p.source.lower() in sources)

    payments = payments[start_index:end_index]

    if not payments:
        payments = {"payments": payments, "success": False,"total_count":total_count}
        return payments
    else:        
        payments = [
            {
                'user': payment.user.email if payment.user else None,
                'user_phone': payment.user.phone if payment.user else None,
                'product': [product.product_name for product in payment.product.all()] if payment.product.exists() else [],
                'plan': [product.product_plan for product in payment.product.all()] if payment.product.exists() else [],
                'source': payment.source,
                'currency': payment.currency,
                'amount': payment.amount,
                'converted_in_usd': payment.converted_amount,
                'two_percent_deduction': payment.deducted_amount,
                'after_deduction_amount': payment.amount_after_deduction,
                'alnafi_payment_id': payment.alnafi_payment_id,
                'order_datetime': payment.order_datetime,
                'card_mask': payment.card_mask,
                'id': payment.id,
                'source_payment_id': payment.source_payment_id,
                'internal_source': payment.internal_source
            }
            for payment in payments
        ]


        response_data = {"payments":payments,"total_count":total_count,"success":True,"total_payments_in_pkr":total_payments_in_pkr, "total_payments_in_usd":total_payments_in_usd}
        return response_data


def add_tax_stripe_according_to_the_country_code(amount,country_code):
    tax_url = f'{settings.CRM_COUNTRY_TAX_API}{country_code}'
    headers = {
    'Authorization': 'Bearer 1f9d7bce259800a704f81c37216b05555be1efa1fcec244a1f0f16622c5542e2fe713afc648301d3840a7a07e243c07928c9e9697267ca6c76a42791b628e9fbb94d0aec3da55db3d6d710a3f4108bf0a206c9407d1c51994465e3e63faaaedcb8aeb46b0d2e42dd430e658bda904b94cd31562b2592a42baebf52be94f4bb71'
    }
    r = requests.get(tax_url,headers=headers)
    try:
        response_data = r.json()['data'][0]
        if 'attributes' in response_data:
            tax = response_data['attributes']['tax']
        else:
            tax = 13

        tax_amount = amount * tax /100
        tax_rate = tax/100
        final_checkout_amount = amount + tax_amount
        return final_checkout_amount,tax_rate
    except Exception as e:
        tax = 0.13
        tax_amount = float(amount) * tax

        final_checkout_amount = float(amount) + tax_amount
        return final_checkout_amount,tax


#PRODUCTION
class PaymentValidationNew(APIView):
    permission_classes = [IsAuthenticated]
    # Your existing post method remains the same
    def post(self, request):
        comment_text = request.data.get('comment')
        print(comment_text)

        try:
            payment_id = request.data.get('payment_id')
            print(payment_id)
            payment = Main_Payment.objects.get(id=payment_id)
            print(payment)
            
            if comment_text is not None: 
                # If comment text is provided, create a comment
                payment.comment = comment_text
                print(payment.comment)
                payment.save()
            return Response({'success': True, "msg":"Comment Done"}, status=status.HTTP_201_CREATED)

        except Main_Payment.DoesNotExist:
            return Response({'msg': 'Payment does not exist'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request):
        q = self.request.GET.get('q', None) or None
        source = self.request.GET.get('source', None) or None

        page = int(self.request.GET.get('page', 1))
        page_size = 10  # Number of payments per page

        # Calculate the start and end indices for slicing
        start_index = (page - 1) * page_size
        end_index = start_index + page_size

        # Query payments with slicing to get only 10 payments for the current page
        payments = Main_Payment.objects.filter(
            source__in=['Al-Nafi', 'NEW ALNAFI']
        ).exclude(
            user__email__endswith="yopmail.com"
            ).select_related('user').prefetch_related('product')

        if source:
            payments = payments.filter(source=source)
        if q:
            payments = payments.filter(Q(user__email__icontains=q) | Q(amount__iexact=q))

        total_count = payments.count()  # Calculate the total count of payments

        payments = payments[start_index:end_index]

        payment_cycle_descriptions = {
            'Monthly': 'Monthly',
            'Yearly': 'Yearly',
            'Half Yearly': 'Half-Yearly',
            'Quarterly': 'Quarterly'
            # Add more plan-value pairs as needed
        }
        payments = payments.annotate(
            payment_cycle=Case(
                *[When(product__product_plan=plan, then=Value(description)) for plan, description in payment_cycle_descriptions.items()],
                default=Value('Unknown Plan'),
                output_field=CharField()
            )
        )

                                
        source_payments = Main_Payment.objects.filter(
            source__in=['Easypaisa', 'UBL_IPG', 'Stripe','UBL_DD']
        ).order_by('-order_datetime').select_related('user')

        valid_payments = []
        users = []
        product_names = []
        payment_list = []
        for payment in payments:
            valid_payment = {
                'valid': True,
                'reasons': [],
            }

            # print("payment source",payment.source)

            source_payment = source_payments.filter(alnafi_payment_id=payment.alnafi_payment_id).first()
            if not source_payment:
                source_payment = source_payments.filter(source_payment_id=payment.alnafi_payment_id).first()
            
            if payment.user is not None:
                if not source_payment:
                    source_payment = source_payments.filter(source='Stripe', user__email=payment.user.email).first()

            # print(source_payment)



            if source_payment:
                tolerance = timedelta(days=1)
                if payment.order_datetime and source_payment.order_datetime:
                    if (payment.order_datetime.date() - tolerance <= source_payment.order_datetime.date() <= payment.order_datetime.date() + tolerance):
                        pass
                    else:
                        valid_payment['valid'] = False
                        valid_payment['reasons'].append('Order date mismatch')
                else:
                    valid_payment['valid'] = False
                    valid_payment['reasons'].append('Order date missing')

                # Loop through related products and gather data
                # product_names = [product.product_name for product in payment.product.all()]
                for product in payment.product.all():
                    product_names.append(product.product_name)
                    product_details = self.check_product_details(product,source_payment,payment,valid_payment)

                if payment.currency == 'PKR':
                    total_product_amount_pkr = 0

                    for product in payment.product.all():  
                        total_product_amount_pkr += product.amount_pkr

                    total_product_amount_pkr = int(total_product_amount_pkr)

                    if total_product_amount_pkr == int(float(payment.amount)):
                        # print("payment matched")
                        pass
                    else:
                        # print(product)
                        # print("total_product_amount_pkr",total_product_amount_pkr)
                        # print("int(float(payment.amount))",int(float(payment.amount)))
                        # print("in else")
                        valid_payment['valid'] = False
                        valid_payment['reasons'].append('Product and Payment Amount mismatch pkr')

                else:
                    # print("in usd")
                    total_product_amount_usd = sum(product.amount_usd for product in payment.product.all())
                    total_product_amount_usd = int(total_product_amount_usd)
                    if total_product_amount_usd == int(float(payment.amount)):
                        pass
                    else:
                        valid_payment['valid'] = False
                        valid_payment['reasons'].append('Product and Payment Amount mismatch usd')
                

            else:
                # print("source payment doesnt exist")
                # print("payment.alnafi_payment_id",payment.alnafi_payment_id)
                # print("payment.source_payment_id",payment.source_payment_id)
                # print(payment.product.all())
                valid_payment['valid'] = False
                valid_payment['reasons'].append("Source payment doesn't exist against this alnafi payment")

            # print(valid_payment)
            valid_payments.append(valid_payment)
            if payment.user:
                # print("payment user exists")
                users.append(payment.user.email)
            payment_list.append(payment)

        # print(payment_list)
        # Process the data to remove duplicates
        duplicates_removed_payment_list = []
        seen_payment_ids = set()

        for i in range(len(payment_list)):
            payment_id = payment_list[i].id

            if payment_id not in seen_payment_ids:
                # If payment with the same id is not seen before, add it to the list
                product_names = [product.product_name for product in payment_list[i].product.all()]
                product_plans = [product.product_plan for product in payment_list[i].product.all()]
            
                payment_data = {
                    'id': payment_id,
                    'comment':payment_list[i].comment,
                    'phone': payment_list[i].candidate_phone,
                    'source': payment_list[i].source,
                    'amount': payment_list[i].amount,
                    'currency': payment_list[i].currency,
                    'product_names': product_names,
                    'plan': product_plans,
                    'alnafi_payment_id': payment_list[i].alnafi_payment_id,
                    'card_mask': payment_list[i].card_mask,
                    'order_datetime': payment_list[i].order_datetime.isoformat(),
                    'is_valid_payment': valid_payments[i]  # Replace with the appropriate index
                }

                if payment_list[i].user:
                    user_email = payment_list[i].user.email
                    payment_data['user_id'] = user_email

                duplicates_removed_payment_list.append(payment_data)
                seen_payment_ids.add(payment_id)

        # Calculate the number of pages
        num_pages = (total_count + page_size - 1) // page_size

        # print(duplicates_removed_payment_list)
        return Response({
            'count': total_count,
            'num_pages': num_pages,
            'results': duplicates_removed_payment_list,
        })


    def check_product_details(self, product, source_payment, payment, valid_payment):
        if product:
            if payment.expiration_datetime:
                if product.product_plan == 'Yearly':
                    tolerance = timedelta(days=15)
                    if source_payment:
                        expiry_date = payment.expiration_datetime.date()
                        expected_expiry = payment.order_datetime.date() + timedelta(days=380) - tolerance
                        if source_payment.order_datetime:
                            if expected_expiry <= expiry_date <= (source_payment.order_datetime.date() + timedelta(days=380) + tolerance):
                                pass
                            else:
                                valid_payment['valid'] = False
                                valid_payment['reasons'].append('Yearly expiration date mismatch')

                if product.product_plan == 'Half Yearly':
                    if source_payment:
                        tolerance = timedelta(days=10)
                        expiry_date = payment.expiration_datetime.date()
                        expected_expiry = payment.order_datetime.date() + timedelta(days=180) - tolerance
                        if source_payment.order_datetime:
                            if expected_expiry <= expiry_date <= (source_payment.order_datetime.date() + timedelta(days=180) + tolerance):
                                pass
                            else:
                                valid_payment['valid'] = False
                                valid_payment['reasons'].append('Half Yearly expiration date mismatch')

                if product.product_plan == 'Quarterly':
                    if source_payment:
                        tolerance = timedelta(days=7)
                        expiry_date = payment.expiration_datetime.date()
                        expected_expiry = payment.order_datetime.date() + timedelta(days=90) - tolerance

                        # print(payment.alnafi_payment_id)
                        # print(payment.source_payment_id)
                        # print("source_payment.order_datetime.date()",source_payment.order_datetime.date())
                        # print(f"{expected_expiry} <= {expiry_date} <= {source_payment.order_datetime.date() + timedelta(days=90) + tolerance}")                       
                        if source_payment.order_datetime:
                            if expected_expiry <= expiry_date <= (source_payment.order_datetime.date() + timedelta(days=90) + tolerance):
                                pass
                            else:
                                valid_payment['valid'] = False
                                valid_payment['reasons'].append('Quarterly expiration date mismatch')

                if product.product_plan == 'Monthly':
                    if source_payment:
                        tolerance = timedelta(days=7)
                        expiry_date = payment.expiration_datetime.date()
                        # print("payment.order_datetime.date()",payment.order_datetime.date())
                        expected_expiry = payment.order_datetime.date() + timedelta(days=30) - tolerance
                        # print("expiry_date",expiry_date)
                        # print("expected_expiry",expected_expiry)
                        # print("source_payment.order_datetime.date() + timedelta(days=30) + tolerance",source_payment.order_datetime.date() + timedelta(days=30) + tolerance)

                        if source_payment.order_datetime:
                            if expected_expiry <= expiry_date <= (source_payment.order_datetime.date() + timedelta(days=30) + tolerance):
                                pass
                            else:
                                # print(source_payment)
                                # print(source_payment.source_payment_id)
                                # print(source_payment.alnafi_payment_id)
                                # print("source_payment.order_datetime",source_payment.order_datetime)
                                # print(f"{expected_expiry} <= {expiry_date} <= {source_payment.order_datetime.date() + timedelta(days=30) + tolerance}")
                                valid_payment['valid'] = False
                                valid_payment['reasons'].append('Monthly expiration date mismatch')

                if product.product_plan == '4 Months':
                    if source_payment:
                        tolerance = timedelta(days=8)
                        expiry_date = payment.expiration_datetime.date()
                        expected_expiry = payment.order_datetime.date() + timedelta(days=120) - tolerance

                        if source_payment.order_datetime:
                            if expected_expiry <= expiry_date <= (source_payment.order_datetime.date() + timedelta(days=120) + tolerance):
                                pass
                            else:
                                valid_payment['valid'] = False
                                valid_payment['reasons'].append('4 month plan expiration date mismatch')

            else:
                valid_payment['valid'] = False
                valid_payment['reasons'].append('Expiration date does not exist')

            return valid_payment


class Renewal_Leads(APIView):
    def get(self,request):
        data = pd.read_csv('/home/faizan/albaseer/Al-Baseer-Backend/payment/Renewal Leads - Al Baseer to CRM - Near To Expiry.csv')
        lst = []
        for index, row in data.iterrows():
            first_name = row['name']
            user_id = row['email']
            phone = row['phone']
            date_joined = row['date_joined']
            product_name = row['product_name']
            payment_date = row['payment_date']
            expiration_date = row['expiry_date']
            status = row['status']
            
            # Remove everything after the date for date_joined
            date_joined = date_joined.split()[0]

            # Remove everything after the date for payment_date
            payment_date = payment_date.split()[0]

            # Remove everything after the date for expiration_date
            expiration_date = expiration_date.split()[0]


            # print(date_joined)
            # print(payment_date)
            # print(expiration_date)

            try:
                renewal = Renewal.objects.create(
                    first_name=first_name,
                    user_id=user_id,
                    phone=phone,
                    date_joined=date_joined,
                    payment_date=payment_date,
                    expiration_date=expiration_date,
                    product_name=product_name,
                    status=status
                )
            except Exception as e:
                print(e)
                lst.append(row['email'])
            
        data_Frame = pd.DataFrame(lst)
        data_Frame.to_csv("error.csv")
        return Response("DONE")


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


class ProductAnalytics(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        q = self.request.GET.get('q', None) or None
        source = self.request.GET.get('source', None) or None
        origin = self.request.GET.get('origin', None) or None
        start_date = self.request.GET.get('start_date', None) or None
        end_date = self.request.GET.get('end_date', None) or None
        export = self.request.GET.get('export', None) or None
        plan = self.request.GET.get('plan', None) or None   
        product = self.request.GET.get('product', None) or None  
        page = int(self.request.GET.get('page', 1))
        
        phone = self.request.GET.get('phone', None) or None  
        status = self.request.GET.get('status', None) or None
        url = request.build_absolute_uri()
        sort_by_str = request.GET.get('sort_by')

        if sort_by_str is not None:
            sort_by = sort_by_str.split(',')
        else:
            # Handle the case when 'sort_by' is not provided in the query
            sort_by = ['payment_total']  # You can set your default value here


        order = self.request.GET.get('order')
        payments= search_payment_for_product_analytics(export, q ,start_date, end_date, plan, source, origin, status,product,page)

        # print(len(payments['payments']))
        # print(payments['payments'])

        # return Response("kjdgrk")
        if payments['success']:        
            # count the product with most payments
            product_info = defaultdict(lambda: {'count': 0, 'payment_total': 0.0, 'plan': '','source':''})
            # usd_rate = get_USD_rate()
            for i in payments['payments']:
                payment_amount = i['amount']
                if i['product']:
                    product_name = i['product']
                else:
                    product_name = None
                
                if product_name and payment_amount:
                    product_info[product_name]['count'] += 1
                    product_info[product_name]['plan'] = i['plan']
                    product_info[product_name]['source'] = i['source']
                    product_info[product_name]['order_datetime'] = i['order_datetime']
                    sources = ['ubl_dd','al-nafi','easypaisa','ubl_ipg']
                    if i['source'].lower() in sources:
                        product_info[product_name]['payment_total'] += float(payment_amount)
                    else:
                        product_info[product_name]['payment_total']  += int(float(payment_amount))
                 
            # Generate dynamic sorting key based on criteria
            def dynamic_sort(data, criteria, order):
                # Generate dynamic sorting key based on criteria
                def string_to_bool(s):
                    if s is not None:
                        return s.lower() == 'true'
                    else:
                        return True
                    
                def key_func(product):
                    if not criteria:
                        return data[product]['payment_total']
                    return tuple(data[product][key] for key in criteria)

                sorted_products = sorted(data.keys(), key=key_func, reverse=string_to_bool(order))
                
                return OrderedDict((product, data[product]) for product in sorted_products)
            
            # Example usage
            sorted_by_count_and_payment = dynamic_sort(product_info, sort_by, order)    

            if product_info:
                product_with_max_revenue = max(product_info, key=lambda k: product_info[k]['payment_total'])
                max_revenue = product_info[product_with_max_revenue]['payment_total']
                product_with_min_revenue = min(product_info, key=lambda k: product_info[k]['payment_total'])
                min_revenue = product_info[product_with_min_revenue]['payment_total']
            else:
                product_with_max_revenue = 0
                product_with_min_revenue = 0
                max_revenue = 0
                min_revenue = 0


            # Find the product with the most payments

            if product_info:
                max_product = max(product_info, key=lambda k: product_info[k]['count'])
                max_product_details = product_info[max_product]
                product_most_payments = max_product
                max_payments_count = max_product_details['count']
                
                # # Find the product with the least payments
                min_product = min(product_info, key=lambda k: product_info[k]['count'])
                min_product_details = product_info[min_product]
                product_least_payments = min_product
                min_payments_count = min_product_details['count']
            else:
                min_payments_count = 0
                max_payments_count = 0
                product_most_payments = 0
                product_least_payments = 0


           
            if export=='true':
                df = pd.DataFrame(payments)
                # Merge dataframes
                file_name = f"Payments_DATA_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                df = df.to_csv(index=False)
                s3 = upload_csv_to_s3(df,file_name)
                data = {'file_link': file_path,'export':'true'}
                return Response(data)
            else:            
                # payment_json = json.dumps(payments, default=json_serializable)  # Serialize the list to JSON with custom encoder
                # payment_objects = json.loads(payment_json)
                
                total_payments_in_pkr = 0
                total_payments_in_usd = 0
                for i in payments['payments']:
                    sources = ['ubl_dd','al-nafi','easypaisa','ubl_ipg']
                    if i['source'].lower() in sources:
                        total_payments_in_pkr += int(float(i['amount']))
                        # total_payments_in_usd += int(float(i['amount'])) // usd_rate['PKR']

                    else:
                        # total_payments_in_pkr += int(float(i['amount'])) * usd_rate['PKR']
                        total_payments_in_usd += int(float(i['amount']))
                
                list_of_products = [{"product_name": key, "details": value} for key, value in sorted_by_count_and_payment.items()]

                paginator = MyPagination()
                paginated_queryset = paginator.paginate_queryset(list_of_products, request)
                
                data = [{'product_with_max_revenue':product_with_max_revenue}, 
                        {'max_revenue':int(max_revenue)}, {'product_with_min_revenue':product_with_min_revenue}, 
                        {'min_revenue': int(min_revenue)}, {'most_payments_product':product_most_payments}, 
                        {'most_payments_count':max_payments_count}, {'least_payments_product':product_least_payments}, 
                        {'least_payments_count':min_payments_count},{'total_payments_pkr': total_payments_in_pkr}, 
                        {'total_payments_usd': total_payments_in_usd}]
                payments = {'product_analytics': data,'product_info':list_of_products}
                
                
                # return paginator.get_paginated_response(paginated_queryset)
                # print(payments)
                return Response(payments)
        else:
            response_data = {"Error": "Incorrect product name or payments for this product does not exist"}
            return Response(response_data)


def search_payment_for_product_analytics(export, q, start_date, end_date, plan, source, origin, status,product,page):
    payments = Main_Payment.objects.exclude(
        user__email__endswith="yopmail.com"
    ).exclude(
        source='UBL_DD', status__in=["0", False, 0]
    ).filter(
        source__in=['Easypaisa', 'UBL_IPG', 'UBL_DD', 'Stripe']
    )
   
    if not start_date:
        first_payment = payments.exclude(order_datetime=None).last()
        start_date = first_payment.order_datetime.date() if first_payment else None

    if not end_date:
        last_payment = payments.exclude(order_datetime=None).first()
        end_date = last_payment.order_datetime.date() if last_payment else None

    payments = payments.filter(Q(order_datetime__date__lte=end_date, order_datetime__date__gte=start_date))


    if plan:
        payments = payments.filter(product__product_plan=plan)
        payments = payments.distinct()


    payment_cycle = payments.values_list('product__product_plan', flat=True).distinct()
    payment_cycle_descriptions = {
        'Monthly': 'Monthly',
        'Yearly': 'Yearly',
        'Half Yearly': 'Half-Yearly',
        'Quarterly': 'Quarterly'
        # Add more plan-value pairs as needed
    }

    payments = payments.annotate(
        payment_cycle=Case(
            *[When(product__product_plan=plan, then=Value(description)) for plan, description in payment_cycle_descriptions.items()],
            default=Value('Unknown Plan'),
            output_field=CharField()
        )
    )


    if export == 'true':
        payments_data = payments.values('user__email', 'user__phone', 'product__product_name', 'source', 'amount',
                                         'order_datetime', 'id','payment_cycle','alnafi_payment_id','card_mask','source_payment_id')
        payments = [{'user': payment['user__email'],'user_phone': payment['user__phone'], 'product': payment['product__product_name'],
                     'plan': payment['payment_cycle'],'source': payment['source'],'amount': payment['amount'],
                     'alnafi_payment_id':payment['alnafi_payment_id'], 'order_datetime': payment['order_datetime'],'card_mask': payment['card_mask'], 
                     'id': payment['id'],'source_payment_id':payment['source_payment_id']} for payment in payments_data]
        payment_list = []
        for payment in payments:
            payment_id = payment['id']
            payment_found = False

            for existing_payment in payment_list:
                if existing_payment['id'] == payment_id:
                    payment_found = True
                    break

            if not payment_found:
                payment_data = {
                    'id': payment['id'],
                    'user_id': payment['user'],
                    'phone': payment['user_phone'],
                    'source': payment['source'],
                    'amount': payment['amount'],
                    'product_names': [payment['product']],
                    'plans': [payment['plan']],
                    'alnafi_payment_id': payment['alnafi_payment_id'],
                    'source_payment_id': payment['source_payment_id'],
                    'card_mask': payment['card_mask'],
                    'order_datetime': payment['order_datetime'].isoformat(),
                }
                payment_list.append(payment_data)



        file_name = f"Payments_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        df = pd.DataFrame(payment_list).to_csv(index=False)
        s3 = upload_csv_to_s3(df, file_name)
        data = {'file_link': file_path, 'export': 'true'}
        return data



    if not payments:
        payments = {"payments": payments, "success": False}
        return payments
    else:        
        payments_data = payments.values('user__email', 'user__phone', 'product__product_name', 'source', 'amount',
                                         'order_datetime', 'id', 'payment_cycle', 'alnafi_payment_id', 'card_mask',
                                         'source_payment_id', 'currency')

        payments = [{'user': payment['user__email'], 'user_phone': payment['user__phone'],
                     'product': payment['product__product_name'], 'plan': payment['payment_cycle'],
                     'source': payment['source'], 'amount': payment['amount'],
                     'alnafi_payment_id': payment['alnafi_payment_id'],
                     'order_datetime': payment['order_datetime'], 'card_mask': payment['card_mask'],
                     'id': payment['id'], 'source_payment_id': payment['source_payment_id'],
                     'currency': payment['currency']} for payment in payments_data]

        response_data = {"payments":payments,"success":True}
        return response_data


#Renewal payments
class ExpiryPayments(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        user_email = self.request.GET.get('q')
        product = self.request.GET.get('product')
        renewal_status = self.request.GET.get('Renewal', None)
        export = self.request.GET.get('export', None) or None

        today = date.today()
        start_date = today.replace(day=1)

        if not start_date_str or not end_date_str:
                end_date = (today.replace(day=1, month=1, year=today.year + 1) if today.month == 12
                            else today.replace(day=1, month=today.month + 1)) - timedelta(days=1)
        else:
            start_date = timezone.make_aware(datetime.strptime(start_date_str, '%Y-%m-%d')).date()
            end_date = timezone.make_aware(datetime.strptime(end_date_str, '%Y-%m-%d')).date()


        cache_key = f"expiry_payments_{start_date}_{end_date}_{user_email}_{product}_{renewal_status}_{export}"
        cached_data = cache.get(cache_key)


        if cached_data:
            response = json.loads(cached_data)
            response_data = response['response_data']
            renewal_amount = response['renewal_amount']
            renewed_amount = response['renewed_amount']
            total_renewal_amount = response['total_renewal_amount']
        else:
            filtered_payments = Main_Payment.objects.filter(
                source__in=['Al-Nafi','NEW ALNAFI'],
                expiration_datetime__range=(start_date, end_date),
                ).exclude(
                user__email__endswith="yopmail.com"
                ).select_related('product').values()
            
            filtered_payments = filtered_payments.annotate(product_plan=Upper('product__product_plan'))

            if user_email:
                filtered_payments = filtered_payments.filter(user__email=user_email)
            if product:
                filtered_payments = filtered_payments.filter(product__product_name__icontains=product)

            # if product:
            #     products_list = product.split(',')
            #     # print(products_list)
            #     # If there is more than one source, filter payments using each source
            #     if len(products_list) > 1:
            #         print(products_list)
            #         filtered_payments = filtered_payments.filter(product__product_name__in=products_list)
            #         print(filtered_payments)

            #         # payments = payments.distinct()
            #     else:
            #         filtered_payments = filtered_payments.filter(product__product_name__in=products_list)
                    # payments = payments.filter(product__product_name__in=products_list)
                    # payments = payments.distinct()


            # Query payments falling within the specified date range for the renewal check
            renewal_payments = Main_Payment.objects.filter(
                order_datetime__range=(start_date, today)
            )
            response_data = []

            users = list(filtered_payments.values('user__email','user__phone'))
            payment_list = list(filtered_payments.values("id","candidate_name","user_id","amount","currency","product_plan","product__product_name","source","order_datetime","expiration_datetime","source_payment_id","alnafi_payment_id","card_mask","country"))
    
            j=0

            renewal_amount = 0
            renewed_amount = 0
            total_renewal_amount = 0



            for i in range(len(payment_list)):

                # while payment_list[i]['id'] != products[j]['id']:
                #     j += 1

                renewal_payment = False
                renewal_payment = renewal_payments.filter(
                    user__email__iexact=users[i]['user__email'],
                    product__product_name=payment_list[i]['product__product_name'],
                    order_datetime__gt=payment_list[i]['order_datetime']
                ).exists()

                if renewal_status == 'false':
                    if not renewal_payment:
                        single_renewal_amount = self.calculate_renewal_amount(payment_list[i])
                        renewal_amount += single_renewal_amount
                elif renewal_status == 'true':
                    if renewal_payment:
                        single_renewed_amount = self.calculate_renewed_amount(payment_list[i])   
                        renewed_amount += single_renewed_amount 
                else:
                    if renewal_payment:
                        single_renewed_amount = self.calculate_renewed_amount(payment_list[i])
                        renewed_amount += single_renewed_amount 
                    else:
                        single_renewal_amount = self.calculate_renewal_amount(payment_list[i])
                        renewal_amount += single_renewal_amount


                payment_list[i]['user_id'] = users[i]['user__email']
                payment_list[i]['Renewal'] = renewal_payment
                payment_list[i]['phone'] = users[i]['user__phone']

                j += 1

               
                if (renewal_status == 'true' and renewal_payment) or (renewal_status == 'false' and not renewal_payment) or renewal_status == 'None':
                    response_data.append(payment_list[i])


            total_renewal_amount = renewed_amount + renewal_amount
            if export == 'true':
                file_name = f"Renewed_Payments_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                df = pd.DataFrame(response_data).to_csv(index=False)
                s3 = upload_csv_to_s3(df, file_name)
                data = {'file_link': file_path, 'export': 'true'}
                return Response(data)
            

            response = {"response_data": response_data,
                        "renewal_amount":renewal_amount,
                        "renewed_amount":renewed_amount,
                        "total_renewal_amount":total_renewal_amount}
            cache.set(cache_key, json.dumps(response, default=str), 60 * 60 * 24)


        if export == 'true':
            file_name = f"Renewed_Payments_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            df = pd.DataFrame(response_data).to_csv(index=False)
            s3 = upload_csv_to_s3(df, file_name)
            data = {'file_link': file_path, 'export': 'true'}
            return Response(data)

        paginator = Paginator(response_data, 10)  # Set the number of items per page (adjust as needed)
        page_number = request.GET.get('page', 1)

        try:
            response_data_paginated = paginator.page(page_number)
        except PageNotAnInteger:
            response_data_paginated = paginator.page(1)
        except EmptyPage:
            response_data_paginated = paginator.page(paginator.num_pages)

        

        return Response({
            'count': len(response_data),
            'num_pages': paginator.num_pages,
            'current_page': response_data_paginated.number,
            'has_next': response_data_paginated.has_next(),
            'has_previous': response_data_paginated.has_previous(),
            'total_renewal_amount': total_renewal_amount,
            'renewal_amount': renewal_amount,
            'renewed_amount': renewed_amount,
            'payments': response_data_paginated.object_list,
        })
    

    def calculate_renewed_amount(self, payment):
        renewed_amount = 0
        amount = payment['amount']
        if payment['currency'].lower() != 'pkr':
            currency_rate = get_pkr_rate(payment['currency'],amount)
            converted_amount = round(float(amount) / currency_rate[payment['currency']],6)
            renewed_amount += converted_amount
        else:
            renewed_amount += float(amount)
        
        return renewed_amount
    
    def calculate_renewal_amount(self, payment):
        amount = payment['amount']
        renewal_amount = 0
        if payment['currency'].lower() != 'pkr':
            currency_rate = get_pkr_rate(payment['currency'],amount)
            converted_amount = round(float(amount) / currency_rate[payment['currency']],6)
            renewal_amount += converted_amount
        else:
            renewal_amount += float(amount)

        return renewal_amount



#Fresh users month wise
class NewPayments(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        user_email = self.request.GET.get('q')
        product = self.request.GET.get('product')
        new_registrations = self.request.GET.get('new_registrations', None)
        export = self.request.GET.get('export', None) or None

        today = date.today()
        start_date = today.replace(day=1)

        if not start_date_str or not end_date_str:
                end_date = (today.replace(day=1, month=1, year=today.year + 1) if today.month == 12
                            else today.replace(day=1, month=today.month + 1)) - timedelta(days=1)
        else:
            start_date = timezone.make_aware(datetime.strptime(start_date_str, '%Y-%m-%d')).date()
            end_date = timezone.make_aware(datetime.strptime(end_date_str, '%Y-%m-%d')).date()


        cache_key = f"new_payments_{start_date}_{end_date}_{user_email}_{product}_{export}_{new_registrations}"
        cached_data = cache.get(cache_key)


        if cached_data:
            response = json.loads(cached_data)
            response_data = response['response_data']
            new_registrations_amount = response['new_registrations_amount']
        else:
            filtered_payments = Main_Payment.objects.filter(
                source__in=['Al-Nafi','NEW ALNAFI','New_Al-Nafi'],
                order_datetime__range=(start_date, end_date),
                ).exclude(
                user__email__endswith="yopmail.com"
                ).select_related('product').values()
            
            
            all_payments = Main_Payment.objects.filter(source__in=['Al-Nafi','NEW ALNAFI','New_Al-Nafi']).select_related('product').values()
            
            filtered_payments = filtered_payments.annotate(product_plan=Upper('product__product_plan'))

            if user_email:
                filtered_payments = filtered_payments.filter(user__email__icontains=user_email)
            if product:
                filtered_payments = filtered_payments.filter(product__product_name__icontains=product)

            # Query payments falling within the specified date range for the renewal check
            response_data = []

            users = list(filtered_payments.values('user__email','user__phone'))
            payment_list = list(filtered_payments.values("id","candidate_name","user_id","amount","currency","product_plan","product__product_name","source","order_datetime","expiration_datetime","source_payment_id","alnafi_payment_id","card_mask","country"))
    
            j=0
           
            new_registrations_amount = 0

            for i in range(len(payment_list)):

                new_payment = all_payments.filter(
                    user__email__iexact=users[i]['user__email'],
                    product__product_name=payment_list[i]['product__product_name'],
                )

                if not len(new_payment) > 1:
                    amount = payment_list[i]['amount']
                    if payment_list[i]['currency'].lower() != 'pkr':
                        currency_rate = get_pkr_rate(payment_list[i]['currency'],amount)
                        converted_amount = round(float(amount) / currency_rate[payment_list[i]['currency']],6)
                        new_registrations_amount += converted_amount
                    else:
                        new_registrations_amount += float(amount)

                payment_list[i]['user_id'] = users[i]['user__email']
                payment_list[i]['phone'] = users[i]['user__phone']

                j += 1
                if new_registrations == 'true':
                    if not len(new_payment) > 1:
                        payment_list[i]['new_registration'] = True
                        response_data.append(payment_list[i])
                else:
                    payment_list[i]['new_registration'] = False
                    response_data.append(payment_list[i])


            if export == 'true':
                file_name = f"Renewed_Payments_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
                file_path = os.path.join(settings.MEDIA_ROOT, file_name)
                df = pd.DataFrame(response_data).to_csv(index=False)
                s3 = upload_csv_to_s3(df, file_name)
                data = {'file_link': file_path, 'export': 'true'}
                return Response(data)
            

            response = {"response_data": response_data,
                        "new_registrations_amount":new_registrations_amount}
            
            cache.set(cache_key, json.dumps(response, default=str), 60 * 60 * 24)


        if export == 'true':
            file_name = f"Renewed_Payments_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            df = pd.DataFrame(response_data).to_csv(index=False)
            s3 = upload_csv_to_s3(df, file_name)
            data = {'file_link': file_path, 'export': 'true'}
            return Response(data)

        paginator = Paginator(response_data, 10)  # Set the number of items per page (adjust as needed)
        page_number = request.GET.get('page', 1)

        try:
            response_data_paginated = paginator.page(page_number)
        except PageNotAnInteger:
            response_data_paginated = paginator.page(1)
        except EmptyPage:
            response_data_paginated = paginator.page(paginator.num_pages)

        

        return Response({
            'count': len(response_data),
            'num_pages': paginator.num_pages,
            'current_page': response_data_paginated.number,
            'has_next': response_data_paginated.has_next(),
            'has_previous': response_data_paginated.has_previous(),
            'new_registrations_amount': new_registrations_amount,
            'payments': response_data_paginated.object_list,
        })



class UploadLeads(APIView):
    def get(self, request):
        url = 'https://crm.alnafi.com/api/resource/Lead'

        data = pd.read_csv('/home/faizan/albaseer/Al-Baseer-Backend/payment/Untitled spreadsheet - Haider Bhai main File (copy).csv')
        for index, row in data.iterrows():
            api_key, api_secret = round_robin()
            headers = {
            'Authorization': f'token {api_key}:{api_secret}',
            "Content-Type": "application/json",
            "Accept": "application/json",
            }
            # print(api_key)
            # print(api_secret)
            date_joined = row.get('Date Joined')
            print(type(row.get('Date Joined')))
            print(row.get('Date Joined'))
            if type(date_joined) != float:
                date_joined = datetime.strptime(date_joined, '%Y-%m-%d %H:%M:%S').date()

            assigned_date = row.get('Assigned Date')
            if type(assigned_date) != float:
                assigned_date = datetime.strptime(assigned_date, '%Y-%m-%d %H:%M:%S').date()

            # Check if the data already exists
            # filter_url = f'https://crm.alnafi.com/api/resource/Suppport?filters=[["customer_email", "=", "{row.get("customer_email")}"],["product_name", "=", "{row.get("product_name")}"]]&limit_start=0&limit_page_length=10000000'
            # check_response = requests.get(filter_url, headers=headers)

            # if check_response.status_code == 200 and len(check_response.json().get('data')) > 0:
            #     print(f"Data for {row.get('customer_email')} already exists!")
            # else:
            # If data doesn't exist, make the POST request
            data_to_post = {
                    'status': row.get('Status'),
                    'email_id': row.get('Email'),
                    'first_name': None if pd.isna(row.get('First Name')) else row.get('First Name'),
                    'last_name': None if pd.isna(row.get('Last Name')) else row.get('Last Name'),
                    'date_joined': None if pd.isna(date_joined) else str(date_joined),
                    'date': None if pd.isna(assigned_date) else str(assigned_date),        
                    'submit_your_question': None if pd.isna(row.get('Submit Your Question If Any')) else row.get('Submit Your Question If Any'),
                    'lead_name': None if pd.isna(row.get('Full Name')) else row.get('Full Name'),
                    'source': row.get('Source') or '',
                    'form': None if pd.isna(row.get('Form')) else row.get('Form'),
                    'how_did_you_hear_about_us': None if pd.isna(row.get('How Did You Hear About Us')) else row.get('How Did You Hear About Us'),

                
                    'product_names_list': None if pd.isna(row.get('Product Names List')) else row.get('Product Names List'), 
                    'advert_detail': row.get('Advert Detail') or '', 
                    'product_name': row.get('Product Name') or '',
                    'cv_link': row.get('CV Link') or '',
                    'demo_product': row.get('Demo Product') or '',
                    'enrollment': row.get('Enrollment') or '',
                    'mobile_no': str(row.get('Mobile No')) or '',
                    'country': row.get('Country') or '',
                    'phone': str(row.get('Phone')) or '',
                    'Image': row.get('Image') or '',
                    'title': row.get('Title') or '',
            }

            print(data_to_post)

            response = requests.post(url, json=data_to_post, headers=headers)
            print(response.status_code)
            if response.status_code == 200:
                print(f"Data for {row.get('Email')} sent successfully!")
            else:
                print(f"Failed to send data for {row.get('Email')}. Status code: {response.status_code}")

        return JsonResponse({'message': 'Data processing completed'})



class LeadDataAPIView(APIView):
    def get(self, request):
        print("api running")
        url = 'https://crm.alnafi.com/api/resource/Suppport'

        # data = pd.read_csv('/home/faizan/albaseer/Al-Baseer-Backend/payment/Checkout-2023-11-23.xlsx')

        file_path = '/home/faizan/albaseer/Al-Baseer-Backend/payment/Checkout-2023-11-23.xlsx'
        data = pd.read_excel(file_path)

        for index, row in data.iterrows():
            api_key, api_secret = round_robin_support()
            headers = {
                'Authorization': f'token {api_key}:{api_secret}',
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
            payment_date = datetime.strptime(row['payment_date'], '%Y-%m-%d %H:%M:%S').date()
            # expiration_date = datetime.strptime(row['expiration_date'], '%Y-%m-%d %H:%M:%S').date()
            expiration_date = row['expiration_date']

            if isinstance(expiration_date, str):
                expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d %H:%M:%S').date()
            else:
                expiration_date = ''

            email = row["email"]
            product = row["product_name"]

            user_api_key = '4e7074f890507cb'
            user_secret_key = 'c954faf5ff73d31'

            admin_headers = {
                'Authorization': f'token {user_api_key}:{user_secret_key}',
                "Content-Type": "application/json",
                "Accept": "application/json",
            }

            # Check if the data already exists
            filter_url = f'https://crm.alnafi.com/api/resource/Suppport?filters=[["customer_email", "=", "{email}"],["product_name", "=", "{product}"]]'
            check_response = requests.get(filter_url, headers=admin_headers)
            # print(check_response.text)
            if check_response.status_code == 200 and len(check_response.json().get('data')) > 0:
                email = row["email"]
                print(f"Data for {email} already exists!")
                continue
            else:
                email = row["email"]
                url = f'https://crm.alnafi.com/api/resource/Suppport?fields=["lead_creator"]&filters=[["customer_email", "=", "{email}"]]'

                user_api_key = '4e7074f890507cb'
                user_secret_key = 'c954faf5ff73d31'

                admin_headers = {
                    'Authorization': f'token {user_api_key}:{user_secret_key}',
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                }

                data = requests.get(url, headers=admin_headers)
                if data.status_code == 200 and len(data.json().get('data')) > 0:

                    data = data.json()
                    email = data['data'][0]["lead_creator"]

                    agents = {"zeeshan.mehr@alnafi.edu.pk": ["a17f7cc184a55ec","3e26bf2dde0db20"],
                              "mutahir.hassan@alnafi.edu.pk": ["ee3c9803e0a7aa0","ad8a5dc4bc4f13f"],
                              "mehtab.sharif@alnafi.edu.pk": ["6b0bb41dba21795","f56c627e47bdff6"],
                              "salman.amjad@alnafi.edu.pk": ["c09e9698c024bd5","02c5e4ff622bb22"],
                              "ahsan.ali@alnafi.edu.pk": ["b5658b2d5a087d0","a9faaabc26bddc5"],
                              "mujtaba.jawed@alnafi.edu.pk": ["940ef42feabf766","7a642a5b930eb44"]
                              }
                    
                    if email in agents:
                        keys_of_zeeshan_mehr = agents[email]
                        # print(keys_of_zeeshan_mehr[0])
                        # print(keys_of_zeeshan_mehr[1])
                    else:
                        print("Email not found in the agents dictionary.")

                    # print("assigning lead to existing agent")
                    # print("agent",email)
                    phone = row['phone']
                    data_to_post = {
                        'price_pkr': row['amount_pkr'],
                        'price_usd': row['amount_usd'],
                        'amount': row['amount'],
                        # 'first_name': row['depositor_name'] or '',
                        'first_name': str(row['depositor_name']) if pd.notna(row['depositor_name']) else '',
                        'payment': str(payment_date) or '',
                        'expiration_date': str(expiration_date) or '',
                        'product_name': row['product_name'] or '',
                        'customer_email': row['email'] or '',
                        'contact_no': str(phone),
                        'expiration_status': 'Active',
                        'payment_source': 'UBL',
                        'lead_creator': email
                    }


                    # Check if price_pkr is nan and convert to None
                    if math.isnan(data_to_post['price_pkr']):
                        data_to_post['price_pkr'] = None

                    # Check if price_usd is nan and convert to None
                    if math.isnan(data_to_post['price_usd']):
                        data_to_post['price_usd'] = None


                    # Check if price_usd is nan and convert to None
                    # if math.isnan(data_to_post['first_name']):
                    #     data_to_post['first_name'] = None


                    print(data_to_post)

                    headers = {
                        'Authorization': f'token {keys_of_zeeshan_mehr[0]}:{keys_of_zeeshan_mehr[1]}',
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                    }

                    response = requests.post(url, json=data_to_post, headers=headers)
                    if response.status_code == 200:
                        print(f"Data for {row['email']} sent successfully!")
                    else:
                        print(response.text)
                        print(f"Failed to send data for {row['email']}. Status code: {response.status_code}")
                else:
                    print("assigning lead to new agent")
                    # If data doesn't exist, make the POST request
                    phone = row['phone']
                    data_to_post = {
                        'price_pkr': row['amount_pkr'],
                        'price_usd': row['amount_usd'],
                        'amount': row['amount'],
                        # 'first_name': row['depositor_name'] or '',
                        'first_name': str(row['depositor_name']) if pd.notna(row['depositor_name']) else '',
                        'payment': str(payment_date) or '',
                        'expiration_date': str(expiration_date) or '',
                        'product_name': row['product_name'] or '',
                        # 'customer_email': row['email'] or '',
                        'customer_email': str(row['email']) if pd.notna(row['email']) else '',
                        # 'contact_no': str(phone),
                        'contact_no': str(row['phone']) if pd.notna(row['phone']) else '',
                        'expiration_status': 'Active',
                        'payment_source': 'UBL',
                        # 'lead_creator': email
                    }

                    # Check if price_pkr is nan and convert to None
                    if math.isnan(data_to_post['price_pkr']):
                        data_to_post['price_pkr'] = None

                    # Check if price_usd is nan and convert to None
                    if math.isnan(data_to_post['price_usd']):
                        data_to_post['price_usd'] = None


                    # print(data_to_post)


                    # Check if price_usd is nan and convert to None
                    # if math.isnan(data_to_post['first_name']):
                    #     data_to_post['first_name'] = None


                    response = requests.post(url, json=data_to_post, headers=headers)
                    # print(response.status_code)
                    
                    if response.status_code == 200:
                        print(f"Data for {row['email']} sent successfully!")
                    else:
                        print(response.text)
                        print(f"Failed to send data for {row['email']}. Status code: {response.status_code}")

        return JsonResponse({'message': 'Data processing completed'})
# from operator import itemgetter
class CommisionData(APIView):
    def get(self, request, *args, **kwargs):
        q = self.request.GET.get('q', None)
        created_date_filter = self.request.GET.get('created_date', None)
        # print(created_date_filter)
        start_date_filter = self.request.GET.get('start_date', None)
        end_date_filter = self.request.GET.get('end_date', None)
        page_size = 10  # Set your desired page size
        paginator = PageNumberPagination()
        paginator.page_size = page_size
        page_number = request.GET.get('page', 1)

        # print(start_date_filter)
        # print(end_date_filter)
        # export = self.request.GET.get('export', None)
        # print("payment_date", payment_date_filter)

        url = f'https://crm.alnafi.com/api/resource/Commission?fields=["title","lead_owner","phone","payment_date","total_product_payment", "owner_pkr","product","order_id","payment_id","order_id", "created_at"]&limit_start=0&limit_page_length=10000000'
        api_key = "4e7074f890507cb"
        api_secret = "c954faf5ff73d31"
        headers = {
            'Authorization': f'token {api_key}:{api_secret}',
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        response = requests.get(url, headers=headers)
        data = response.json()

        filtered_items = data["data"]

        if q:
            # Filter data based on the provided email address (case-insensitive and partial match)
            filtered_items = [item for item in filtered_items if q.lower() in item.get("lead_owner", "").lower()]

        if created_date_filter:
            # Filter data based on the provided payment date
            filtered_items = [item for item in filtered_items if item.get("created_at") == created_date_filter]
        if start_date_filter and end_date_filter:
            start_date = datetime.strptime(start_date_filter, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_filter, '%Y-%m-%d')
            filtered_items = [item for item in filtered_items if
                            item.get("created_at") and start_date <= datetime.strptime(item.get("created_at"), '%Y-%m-%d') <= end_date]
        elif start_date_filter:
            start_date = datetime.strptime(start_date_filter, '%Y-%m-%d')
            filtered_items = [item for item in filtered_items if
                            item.get("created_at") and start_date <= datetime.strptime(item.get("created_at"), '%Y-%m-%d')]
        elif end_date_filter:
            end_date = datetime.strptime(end_date_filter, '%Y-%m-%d')
            filtered_items = [item for item in filtered_items if
                            item.get("created_at") and datetime.strptime(item.get("created_at"), '%Y-%m-%d') <= end_date]
        reversed_items = filtered_items[::-1]
        paginated_data = paginator.paginate_queryset(reversed_items, request)
        total_length = len(reversed_items)
        total_product_payments = round(sum(float(item.get('total_product_payment', 0)) for item in reversed_items),2)
        total_commission = round(sum(float(item.get('owner_pkr', 0)) for item in reversed_items),2)
        total_pages = math.ceil(total_length / page_size)


        # Add Total Product Payments and Total Commission to the response data
        response_data = {
            "Total Data": total_length,
            "Page-Count": total_pages,
            "Total Commission": total_commission,
            "Total Product Payments": total_product_payments,
            "Current-page": int(page_number),
            "data": paginated_data,
        }
        return Response(response_data)
        # if export == 'true':
        #     file_name = f"Commission{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
        #     file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        #     df = pd.DataFrame(response_data).to_csv(index=False)
        #     s3 = upload_csv_to_s3(df, file_name)
        #     data = {'file_link': file_path, 'export': 'true'}
        #     return Response(data)

        # return Response(response_data)


class Roidata(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        status_filter = request.GET.get('status')
        email_filter = request.GET.get('q')
        start_date_filter = request.GET.get('start_date')
        end_date_filter = request.GET.get('end_date')
        export = request.GET.get('export')
        # print("export", export)
        # print(status_filter, email_filter, start_date_filter, end_date_filter)
        
        moc_data = Moc_Leads.objects.values('first_name', 'email', 'phone', 'form', 'country', 'login_source', 'created_at__date', 'advert')         
        if email_filter:
            moc_data = moc_data.filter(email=email_filter)

        if start_date_filter:
            start_date = datetime.strptime(start_date_filter, "%Y-%m-%d").date()
            moc_data = moc_data.filter(created_at__date__gte=start_date)

        if end_date_filter:
            end_date = datetime.strptime(end_date_filter, "%Y-%m-%d").date() + timedelta(days=1)
            moc_data = moc_data.filter(created_at__date__lt=end_date)

        moc_data = list(moc_data)

        moc_emails = [entry['email'] for entry in moc_data if entry['email']]

        if start_date_filter:
            start_date_payment = datetime.strptime(start_date_filter, "%Y-%m-%d").date()
            existing_payments = Main_Payment.objects.filter(user__email__in=moc_emails, order_datetime__date__gte=start_date_payment)
        else:
            existing_payments = Main_Payment.objects.filter(user__email__in=moc_emails)

        if end_date_filter:
            today = datetime.now().date()
            existing_payments = existing_payments.filter(order_datetime__date__lt=today)

        payments_info = existing_payments.values('user__email', 'amount', 'source_payment_id', 'order_datetime__date', 'currency', 'source')
        payments_info = {payment['user__email']: payment for payment in payments_info}

        status_filter = status_filter.lower() if status_filter else None

        if status_filter == 'converted':
            total_sum_of_amounts = sum(float(payment_info['amount']) for payment_info in payments_info.values() if payment_info['amount'])
        elif status_filter == 'not converted':
            total_sum_of_amounts = 0
        else:
            total_sum_of_amounts = sum(float(payment_info['amount']) for payment_info in payments_info.values() if payment_info['amount'])

        for entry in moc_data:
            email = entry['email']
            if email in payments_info:
                payment_info = payments_info[email]
                entry['amount'] = payment_info['amount']
                entry['source_payment_id'] = payment_info['source_payment_id']
                entry['currency'] = payment_info['currency']
                entry['source'] = payment_info['source']
                entry['order_datetime'] = payment_info['order_datetime__date']
            else:
                entry['amount'] = None
                entry['source_payment_id'] = None
                entry['currency'] = None
                entry['source'] = None
                entry['order_datetime__date'] = None

            entry['status'] = 'Converted' if email in payments_info else 'Not Converted'
            if entry['currency'] not in ['PKR', 'None', None, 'null']:
                currency_rate = get_pkr_rate(entry['currency'], entry['amount'])
                converted_amount = round(float(entry['amount']) / currency_rate[entry['currency']], 2)
                entry['amount'] = converted_amount
                entry['currency'] = 'PKR'
        if status_filter:
            moc_data = [entry for entry in moc_data if entry['status'].lower() == status_filter]

        paginator = Paginator(moc_data, 10)
        page_number = request.GET.get('page')

        try:
            paginated_data = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_data = paginator.page(1)
        except EmptyPage:
            paginated_data = paginator.page(paginator.num_pages)
        if export == 'true':
            file_name = f"Roi_data{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            df = pd.DataFrame(moc_data).to_csv(index=False)
            s3 = upload_csv_to_s3(df, file_name)
            data = {'file_link': file_path, 'export': 'true'}
            return Response(data)

        response_data = {
            'total_sum_of_amounts': total_sum_of_amounts,
            'total_pages': paginator.num_pages,
            'current_page': paginated_data.number,
            'length_data': paginator.count,
            'page_count': paginator.num_pages,
            'data': list(paginated_data),
        }
        return JsonResponse(response_data, safe=False)
        
        
        

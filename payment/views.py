from locale import currency
from math import prod
from sre_constants import SUCCESS
from tracemalloc import start
from rest_framework import status

import payment
from .models import Stripe_Payment, Easypaisa_Payment, UBL_IPG_Payment, AlNafi_Payment,Main_Payment,UBL_Manual_Payment, New_Alnafi_Payments,Renewal
from products.models import Main_Product
from .serializer import (Easypaisa_PaymentsSerializer, Ubl_Ipg_PaymentsSerializer, AlNafiPaymentSerializer,MainPaymentSerializer,
                         UBL_Manual_PaymentSerializer, New_Al_Nafi_Payments_Serializer)
from .services import (json_to_csv, renewal_no_of_payments,main_no_of_payments,no_of_payments,get_USD_rate)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta, date
from django.db.models import Q
from django.http import HttpResponse
from django.conf import settings
import os
import pandas as pd
from django.core.cache import cache
from user.services import upload_csv_to_s3
import numpy as np
import json
from django.db.models.functions import Upper
from threading import Thread
from collections import defaultdict, OrderedDict
from django.db.models import Q, F, Value, Case, When, CharField
import csv
import requests
from secrets_api.algorithem import round_robin_support
from django.db.models import F
from django.core.cache import cache


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
            # print(instance)
            
            serializer = New_Al_Nafi_Payments_Serializer(instance.first(), data=data)
        except:
            serializer = New_Al_Nafi_Payments_Serializer(data=data)

        
        if serializer.is_valid():
            serializer.save()
            # print("valid")
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
        source = self.request.GET.get('source', None) or None
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
            payments = payments.exclude(Q(payment_cycle__exact='') | Q(payment_cycle__isnull=True))

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
                # payments = payments.filter(Q(user__email__icontains=q) | Q(amount__iexact=q))            
                
            if product:
                payments = payments.filter(product__product_name__icontains=product)
    
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

                
            if request.user.is_admin:
                # print("admin user")
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

            # print(removed_duplicates)
            if request.user.is_admin:
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
        page = self.request.GET.get('page', 1) or None  
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
        payments= search_payment(export, q ,start_date, end_date, plan, source, origin, status,product,page)
        if payments['success']:
            def json_serializable(obj):
                    if isinstance(obj, datetime):
                        return obj.isoformat()  # Convert datetime to ISO 8601 format
                    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")
        
            # count the product with most payments
            product_info = defaultdict(lambda: {'count': 0, 'payment_total': 0.0, 'plan': '','source':''})
            # usd_rate = get_USD_rate()
            for i in payments['payments']:
                # try:
                    # print(i['payment_cycle'])
                    # payments[i]['user_id'] = users[i]['user__email']
                    # payment[i]['product_id'] = users[i]['product__product_name']
                payment_amount = i['amount']
                if i['product']:
                    product_name = i['product'][0]
                
                # print("payments[i]['product']",payments[i]['product'])
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
                            #  * usd_rate['PKR']
                # except Exception as e:
                #     # pass
                #     print(e)
            # print(product_info)
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
            # print(sorted_by_count_and_payment)        
            # sorted_products = sorted(product_info.keys(), key=lambda k: (product_info[k]['count'], product_info[k]['payment_total']), reverse=True)
            # sorted_dict = OrderedDict((product, product_info[product]) for product in sorted_products)
            
            product_with_max_revenue = max(product_info, key=lambda k: product_info[k]['payment_total'])
            max_revenue = product_info[product_with_max_revenue]['payment_total']
            product_with_min_revenue = min(product_info, key=lambda k: product_info[k]['payment_total'])
            min_revenue = product_info[product_with_min_revenue]['payment_total']

            # print("product_with_max_revenue",product_with_max_revenue)
            # print("max revenue", max_revenue)
            # print("product_with_min_revenue",product_with_min_revenue)
            # print("min revenue", min_revenue)
            # print(product_info) 
            # Find the product with the most payments
            max_product = max(product_info, key=lambda k: product_info[k]['count'])
            max_product_details = product_info[max_product]
            product_most_payments = max_product
            max_payments_count = max_product_details['count']
            # print("max_product_details",max_product_details)
            # print("max_payments_count",max_payments_count)

            # # Find the product with the least payments
            min_product = min(product_info, key=lambda k: product_info[k]['count'])
            min_product_details = product_info[min_product]
            product_least_payments = min_product
            min_payments_count = min_product_details['count']

            # print("min_product_details",min_product_details,min_payments_count)
           

           
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
                payment_json = json.dumps(payments, default=json_serializable)  # Serialize the list to JSON with custom encoder
                payment_objects = json.loads(payment_json)
                
                total_payments_in_pkr = 0
                total_payments_in_usd = 0
                for i in payment_objects['payments']:
                    sources = ['ubl_dd','al-nafi','easypaisa','ubl_ipg']
                    if i['source'].lower() in sources:
                        total_payments_in_pkr += int(float(i['amount']))
                        # total_payments_in_usd += int(float(i['amount'])) // usd_rate['PKR']

                    else:
                        # total_payments_in_pkr += int(float(i['amount'])) * usd_rate['PKR']
                        total_payments_in_usd += int(float(i['amount']))
                
                list_of_products = [{"product_name": key, "details": value} for key, value in sorted_by_count_and_payment.items()]

                paginator = MyPagination()
                # paginated_queryset = paginator.paginate_queryset(payment_objects, request)
                
                data = [{'product_with_max_revenue':product_with_max_revenue}, 
                        {'max_revenue':max_revenue}, {'product_with_min_revenue':product_with_min_revenue}, 
                        {'min_revenue': min_revenue}, {'most_payments_product':product_most_payments}, 
                        {'most_payments_count':max_payments_count}, {'least_payments_product':product_least_payments}, 
                        {'least_payments_count':min_payments_count},{'total_payments_pkr': total_payments_in_pkr}, 
                        {'total_payments_usd': total_payments_in_usd}]
                payments = {'product_analytics': data,'product_info':list_of_products}
                
                
                # return paginator.get_paginated_response(paginated_queryset)
                return Response(payments)
        else:
            response_data = {"Error": "Incorrect product name or payments for this product does not exist"}
            return Response(response_data)

       
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
        source = self.request.GET.get('source', None)
        origin = self.request.GET.get('origin', None)
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)
        export = self.request.GET.get('export', None)
        plan = self.request.GET.get('plan', None)
        product = self.request.GET.get('product', None)
        status = self.request.GET.get('status', None)
        page = int(self.request.GET.get('page', 1))

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
                    'amount': payment['amount'],
                    'product_names': payment['product'],
                    'plans': payment['plan'],
                    'alnafi_payment_id': payment['alnafi_payment_id'],
                    'source_payment_id': payment['source_payment_id'],
                    'card_mask': payment['card_mask'],
                    'order_datetime': payment['order_datetime'].isoformat(),
                    'currency': payment['currency'],
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
        source__in=['Easypaisa', 'UBL_IPG', 'UBL_DD', 'Stripe']
    )


    if status:
        payments = payments.filter(status=status)

    if source:
        payments = payments.filter(source=source)

    if origin:
        if origin == 'local':
            payments = payments.filter(source__in=['Easypaisa', 'UBL_IPG', 'UBL_DD'])
        else:
            payments = payments.filter(source='Stripe')

    if not start_date:
        first_payment = payments.exclude(order_datetime=None).last()
        start_date = first_payment.order_datetime.date() if first_payment else None

    if not end_date:
        last_payment = payments.exclude(order_datetime=None).first()
        end_date = last_payment.order_datetime.date() if last_payment else None

    payments = payments.filter(Q(order_datetime__date__lte=end_date, order_datetime__date__gte=start_date))

    if q:
        payments = payments.filter(user__email__icontains=q)



    if product:
        keywords = product.split()
        query = Q()
        for keyword in keywords:
            query &= Q(product__product_name__icontains=keyword)
        payments = payments.filter(query)
        payments = payments.distinct()


 
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

    page_size = 10  # Number of payments per page

    # Calculate the start and end indices for slicing
    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    total_count = payments.count()  # Calculate the total count of payments


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


    sources = ['ubl_dd', 'al-nafi', 'easypaisa', 'ubl_ipg']

    total_payments_in_usd = 0
    for p in payments:
        if p.source.lower() not in sources:
            if p.currency.lower() == 'pkr':
                pass
            elif p.currency.lower() != 'usd':
                currency_rate = get_USD_rate(p.currency,p.amount)
                converted_amount = float(p.amount) / currency_rate[p.currency]
                total_payments_in_usd += converted_amount
            else:
                total_payments_in_usd += float(p.amount)

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
                'amount': payment.amount,
                'alnafi_payment_id': payment.alnafi_payment_id,
                'order_datetime': payment.order_datetime,
                'card_mask': payment.card_mask,
                'id': payment.id,
                'source_payment_id': payment.source_payment_id,
                'currency': payment.currency
            }
            for payment in payments
        ]

        response_data = {"payments":payments,"total_count":total_count,"success":True,"total_payments_in_pkr":total_payments_in_pkr, "total_payments_in_usd":total_payments_in_usd}
        return response_data










#PRODUCTION
class PaymentValidationNew(APIView):
    permission_classes = [IsAuthenticated]
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
            source__in=['Easypaisa', 'UBL_IPG', 'Stripe']
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
            source_payment = source_payments.filter(alnafi_payment_id=payment.alnafi_payment_id).first()

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
                    total_product_amount_pkr = sum(product.amount_pkr for product in payment.product.all())
                    total_product_amount_pkr = int(total_product_amount_pkr)
                    if total_product_amount_pkr == int(float(payment.amount)):
                        pass
                    else:
                        valid_payment['valid'] = False
                        valid_payment['reasons'].append('Product and Payment Amount mismatch pkr')

                if payment.currency == 'USD':
                    total_product_amount_usd = sum(product.amount_usd for product in payment.product.all())
                    total_product_amount_usd = int(total_product_amount_usd)
                    if total_product_amount_usd == int(float(payment.amount)):
                        pass
                    else:
                        valid_payment['valid'] = False
                        valid_payment['reasons'].append('Product and Payment Amount mismatch usd')
                
                if payment.currency == 'sar':
                    total_product_amount_sar = sum(product.amount_usd for product in payment.product.all())
                    total_product_amount_usd = int(total_product_amount_usd)
                    if total_product_amount_usd == int(float(payment.amount)):
                        pass
                    else:
                        valid_payment['valid'] = False
                        valid_payment['reasons'].append('Product and Payment Amount mismatch usd')

            else:
                valid_payment['valid'] = False
                valid_payment['reasons'].append("Source payment doesn't exist against this alnafi payment")

            valid_payments.append(valid_payment)
            if payment.user:
                users.append(payment.user.email)
            payment_list.append(payment)

        # Process the data to remove duplicates
        duplicates_removed_payment_list = []
        seen_payment_ids = set()

        for payment in payment_list:
            payment_id = payment.id

            if payment_id not in seen_payment_ids:
                # If payment with the same id is not seen before, add it to the list
                if payment.user:
                    user_email = payment.user.email
                product_names = [product.product_name for product in payment.product.all()]
                product_plans = [product.product_plan for product in payment.product.all()]
                payment_data = {
                    'id': payment_id,
                    'user_id': user_email,
                    'phone': payment.candidate_phone,
                    'source': payment.source,
                    'amount': payment.amount,
                    'currency': payment.currency,
                    'product_names': product_names,
                    'plan': product_plans,
                    'alnafi_payment_id': payment.alnafi_payment_id,
                    'card_mask': payment.card_mask,
                    'order_datetime': payment.order_datetime.isoformat(),
                    'is_valid_payment': valid_payments[0]  # Replace with the appropriate index
                }

                duplicates_removed_payment_list.append(payment_data)
                seen_payment_ids.add(payment_id)

        # Calculate the number of pages
        num_pages = (total_count + page_size - 1) // page_size

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
                        if source_payment.order_datetime:
                            if expected_expiry <= expiry_date <= (source_payment.order_datetime.date() + timedelta(days=90) + tolerance):
                                pass
                            else:
                                valid_payment['valid'] = False
                                valid_payment['reasons'].append('Quarterly expiration date mismatch')

                if product.product_plan == 'Monthly':
                    if source_payment:
                        tolerance = timedelta(days=5)
                        expiry_date = payment.expiration_datetime.date()
                        expected_expiry = payment.order_datetime.date() + timedelta(days=30) - tolerance

                        if source_payment.order_datetime:
                            if expected_expiry <= expiry_date <= (source_payment.order_datetime.date() + timedelta(days=30) + tolerance):
                                pass
                            else:
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





#OLD
#response time 6 seconds in prod
#bug in plan payment filter, when implement plan filter payment gets duplicated
#issue in product filter when trying to optimize api further than 6 seconds and ,export not fixed
# class SearchPayments(APIView):
#     # permission_classes = [IsAuthenticated]   
#     # Define the sources list here
#     def get(self, request):
#         query = self.request.GET.get('q', None)
#         source = self.request.GET.get('source', None)
#         origin = self.request.GET.get('origin', None)
#         start_date = self.request.GET.get('start_date', None)
#         end_date = self.request.GET.get('end_date', None)
#         export = self.request.GET.get('export', None)
#         plan = self.request.GET.get('plan', None)
#         product = self.request.GET.get('product', None)
#         status = self.request.GET.get('status', None)
#         page = int(self.request.GET.get('page', 1))
#         phone = self.request.GET.get('phone', None)

#         payments, success= search_payment(export, query, start_date, end_date, plan, source, origin, status,product,page,request,phone)
#         if success:
#             payments = self.process_payments(payments, export,product)            
#             if export == 'true':
#                 return Response(payments)
#             paginated_queryset = self.paginate_response(request,payments)
#             response = {"total_payments_pkr": payments['total_payments_pkr'],"total_payments_usd":payments['total_payments_usd'],'count': payments['count'],"payments":paginated_queryset}
#             return Response(response)
#         else:
#             payments = []
#             return Response(payments)

#     def process_payments(self, payments, export,product):
#         payment_list = []
#         for payment in payments:
#             payment_id = payment['id']

#             payment_found = False

#             for existing_payment in payment_list:
#                 if existing_payment['id'] == payment_id:
#                     existing_payment['product_names'].append(payment['product'])
#                     existing_payment['plans'].append(payment['plan'])
#                     payment_found = True
#                     break

#             if not payment_found:
#                 payment_data = {
#                     'id': payment['id'],
#                     'user_id': payment['user'],
#                     'phone': payment['user_phone'],
#                     'source': payment['source'],
#                     'amount': payment['amount'],
#                     'product_names': [payment['product']],
#                     'plans': [payment['plan']],
#                     'alnafi_payment_id': payment['alnafi_payment_id'],
#                     'source_payment_id': payment['source_payment_id'],
#                     'card_mask': payment['card_mask'],
#                     'order_datetime': payment['order_datetime'].isoformat(),
#                     'currency': payment['currency'],
#                 }

#                 payment_list.append(payment_data)


#         sources = ['ubl_dd', 'al-nafi', 'easypaisa', 'ubl_ipg']
#         total_payments_in_pkr = sum(float(p['amount']) for p in payment_list if p['source'].lower() in sources)
#         # total_payments_in_usd = sum(float(p['amount']) for p in payment_list if p['source'].lower() not in sources)

#         total_payments_in_usd = 0
#         for p in payment_list:
#             if p['source'].lower() not in sources:
#                 if p['currency'].lower() == 'pkr':
#                     pass
#                 elif p['currency'].lower() != 'usd':
#                     currency_rate = get_USD_rate(p['currency'],p['amount'])
#                     converted_amount = float(p['amount']) / currency_rate[p['currency']]
#                     total_payments_in_usd += converted_amount
#                 else:
#                     total_payments_in_usd += float(p['amount'])


#         if export == 'true':
#             file_name = f"Payments_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
#             file_path = os.path.join(settings.MEDIA_ROOT, file_name)
#             df = pd.DataFrame(payment_list).to_csv(index=False)
#             s3 = upload_csv_to_s3(df, file_name)
#             data = {'file_link': file_path, 'export': 'true'}
#             return data


#         return {
#             'total_payments_pkr': total_payments_in_pkr,
#             'total_payments_usd': total_payments_in_usd,
#             'payments': payment_list,
#             "count": len(payment_list)
#         }

#     def paginate_response(self, request, payments):
#         paginator = MyPagination()
#         paginated_queryset = paginator.paginate_queryset(payments['payments'], request)
#         return paginated_queryset
    
#     def are_product_names_equal(self,product_name1, product_name2):
#         cleaned_name1 = self.clean_product_name(product_name1)
#         cleaned_name2 = self.clean_product_name(product_name2)
        
#         return cleaned_name1 == cleaned_name2
    
#     def clean_product_name(self,product_name):
#     # List of terms to remove
#         remove_terms = ["Half Yearly", "Yearly", "Quarterly", "Monthly", "4 Months"]
#         remove_words = ["in"]

#         # Remove terms from the end of the product name
#         if type(product_name) == list:
#             for term in remove_terms:
#                 if product_name[0].endswith(term):
#                     product_name = product_name[0][:-len(term)].strip()

#             # Remove specific words from the product name
#             for word in remove_words:
#                 product_name = product_name[0].replace(word, "").strip()
#         else:

#             for term in remove_terms:
#                 if product_name.endswith(term):
#                     product_name = product_name[:-len(term)].strip()

#             # Remove specific words from the product name
#             for word in remove_words:
#                 product_name = product_name.replace(word, "").strip()


#         return product_name.lower().replace(" ", "")




#OLD
# def search_payment(export, q, start_date, end_date, plan, source, origin, status, product, page, request, phone):
#     payments = Main_Payment.objects.exclude(
#         user__email__endswith="yopmail.com"
#     ).exclude(
#         source='UBL_DD', status__in=["0", False, 0]
#     ).filter(
#         source__in=['Easypaisa', 'UBL_IPG', 'UBL_DD', 'Stripe']
#     )

#     if status:
#         payments = payments.filter(status=status)

#     if source:
#         payments = payments.filter(source=source)

#     if origin:
#         source_filter = ['Easypaisa', 'UBL_IPG', 'UBL_DD'] if origin == 'local' else ['Stripe']
#         payments = payments.filter(source__in=source_filter)

#     if not start_date:
#         start_date = payments.exclude(order_datetime=None).last().order_datetime.date()

#     if not end_date:
#         end_date = payments.exclude(order_datetime=None).first().order_datetime.date()

#     payments = payments.filter(order_datetime__range=(start_date, end_date))

#     print(payments)

#     if q:
#         payments = payments.filter(user__email__icontains=q)


#     print(payments)

#     if phone:
#         phone = phone.strip()
#         if phone.startswith("92"):
#             phone = "+" + phone
#         payments = payments.filter(user__phone__icontains=phone)

#     if product:
#         keywords = product.split()
#         query = Q()
#         for keyword in keywords:
#             query &= Q(product__product_name__icontains=keyword)
#         payments = payments.filter(query)

#     if plan:
#         payments = payments.filter(product__product_plan=plan)

#     payment_cycle_descriptions = {
#         'Monthly': 'Monthly',
#         'Yearly': 'Yearly',
#         'Half Yearly': 'Half-Yearly',
#         'Quarterly': 'Quarterly'
#         # Add more plan-value pairs as needed
#     }

#     payments = payments.annotate(
#         payment_cycle=Case(
#             *[When(product__product_plan=plan, then=Value(description)) for plan, description in payment_cycle_descriptions.items()],
#             default=Value('Unknown Plan'),
#             output_field=CharField()
#         )
#     )

#     if not payments:
#         return payments, False
#     else:
#         payments_data = payments.values('user__email', 'user__phone', 'product__product_name', 'source', 'amount',
#                                          'order_datetime', 'id', 'payment_cycle', 'alnafi_payment_id', 'card_mask',
#                                          'source_payment_id', 'currency')

#         payments = [{'user': payment['user__email'], 'user_phone': payment['user__phone'],
#                      'product': payment['product__product_name'], 'plan': payment['payment_cycle'],
#                      'source': payment['source'], 'amount': payment['amount'],
#                      'alnafi_payment_id': payment['alnafi_payment_id'],
#                      'order_datetime': payment['order_datetime'], 'card_mask': payment['card_mask'],
#                      'id': payment['id'], 'source_payment_id': payment['source_payment_id'],
#                      'currency': payment['currency']} for payment in payments_data]

#         return payments, True



# class PaymentDelete(APIView):
#     def get(self, request):
#         objs = UBL_Manual_Payment.objects.all()
#         objs.delete()
#         return Response('deleted')








# def clean_product_name(product_name):
#         # print("in clean product name func")
#         # List of terms to remove
#         remove_terms = ["Half Yearly", "Yearly", "Quarterly", "Monthly", "4 Months","Annual"]
#         remove_words = ["in"]

#         # Remove terms from the end of the product name
#         # print("product_name",type(product_name))
#         if type(product_name) == list:
#             # print("product_name[0]",product_name[0])
#             for term in remove_terms:
#                 if product_name[0].endswith(term):
#                     # print("ends with term")
#                     product_name = product_name[0][:-len(term)].strip()
#                     # print("product_name",product_name)
#             # Split the string into words, filter out unwanted words, and join them back
#             product_name_parts = product_name.split()
#             product_name_parts = [word for word in product_name_parts if word not in remove_words]
#             product_name = ' '.join(product_name_parts)

#             # print("product_name",product_name)
#             # print("word removed")
#         else:
#             # print("in else")
#             # print("product_name",product_name)
#             for term in remove_terms:
#                 if product_name.endswith(term):
#                     # print("ends with term")
#                     product_name = product_name[:-len(term)].strip()
#                     # print("product_name",product_name)

#             # Remove specific words from the product name
#             for word in remove_words:
#                 product_name = product_name.replace(word, "").strip()

#         # print("product_name",product_name)
#         # print("exiting clean product name func")
#         return product_name.lower().replace(" ", "")
#         # return product_name


# def are_product_names_equal(self,product, payment_product):
#         product = self.clean_product_name(product)
#         payment_product = self.clean_product_name(payment_product)
        
#         # print("cleaned_name1",product)
#         # print("cleaned_name2",payment_product)
#         return product == payment_product
from django.shortcuts import render
from .models import Stripe_Payment, Easypaisa_Payment, UBL_IPG_Payment,AlNafi_Payment, Main_Payment
from .serializer import StripePaymentSerializer, Ubl_Ipg_PaymentsSerializer, Easypaisa_PaymentsSerializer,MainPaymentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from datetime import date, datetime, time, timedelta
import pandas as pd
from django.conf import settings
import os
import shutil
from products.models import Alnafi_Product, Main_Product
from django.db.models import F, Max, Q
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Case, CharField, Value, When
import calendar
from calendar import monthrange
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.core.cache import cache
import requests
import json
from collections import defaultdict


def json_to_csv(serialized_data,name):
    file_name = f"{name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
    # Build the full path to the media directory
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    pd.DataFrame(serialized_data.data).to_csv(file_path, index=False)
    return file_path


def main_no_of_payments(start_date,end_date,source):
    payments = Main_Payment.objects.exclude(product__product_name="test").exclude(amount=1).filter(source__in=['Easypaisa','UBL_IPG','Stripe','UBL_DD'])
    
    if source:
        payments = payments.filter(source=source)
    
    try:
        if not start_date:
            if payments:
                first_payment = payments.exclude(order_datetime=None).last()
                date_time_obj = first_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
                new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")                                                                                    
                start_date = new_date_obj + timedelta(days=20)       
        if not end_date:
            if payments:
                last_payment = payments.exclude(order_datetime=None).first()
                date_time_obj = last_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
                new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")
                end_date = new_date_obj - timedelta(days=20)
                
        delta = end_date - start_date
        dates = []
        for i in range(delta.days + 1):
            date = start_date + timedelta(days=i)
            dates.append(date)
            
        payments = payments.filter(order_datetime__date__in=dates)
        payment_dict = {}
        for payment in payments:
            if payment.order_datetime.date() in payment_dict:
                payment_dict[payment.order_datetime.date()].append(payment)
            else:
                payment_dict[payment.order_datetime.date()] = [payment]

        response_data = []
        for date in dates:
            if date.date() in payment_dict:
                payments_for_date = payment_dict[date.date()]
                serialized_payments = MainPaymentSerializer(payments_for_date, many=True).data
            else:
                serialized_payments = []

            response_data.append({
                'date': date.date(),
                'payments': len(serialized_payments)
            })
    except TypeError:
        error_message = "Source is incorrect"
        response_data = {'error': error_message}
    except Exception as e:
        error_message = str(e)
        response_data = {'error': error_message}

    return response_data


def no_of_payments(source):
    filtered_payments = Main_Payment.objects.exclude(product__product_name="test") \
    .exclude(amount=1) \
    .filter(source__in=['Easypaisa', 'UBL_IPG', 'Stripe', 'UBL_Manual', 'UBL_DD'])

    # Initialize a defaultdict to store payments by source
    payments_by_source = defaultdict(list)

    # Organize payments into lists based on source
    for payment in filtered_payments:
        payments_by_source[payment.source].append({
            "id": payment.id,
            "amount": payment.amount,
            "status": payment.status,
            # Include other payment attributes you want in the response
        })

    # Exclude payments with status 0 for the 'ubl_dd' source
    ubl_dd_payments = payments_by_source["UBL_DD"]
    ubl_dd_payments = [payment for payment in ubl_dd_payments if payment["status"] != 0]
    payments_by_source["UBL_DD"] = ubl_dd_payments

    # Create a dictionary with count of payments for each source
    payments_count_by_source = {}
    for source, payments in payments_by_source.items():
        payments_count_by_source[source] = len(payments)

    # Print or return the dictionary with count of payments for each source
    # print(payments_count_by_source)
    return payments_count_by_source



def renewal_no_of_payments(payments):
    current_month = datetime.now().month
    current_year = datetime.now().year

    _, num_days = monthrange(current_year, current_month)

    dates_of_month = [datetime(current_year, current_month, day) for day in range(1, num_days + 1)]

    payments_by_date = payments.filter(
        expiration_datetime__year=current_year,
        expiration_datetime__month=current_month,
        expiration_datetime__day__in=range(1, num_days + 1)
    ).annotate(date=TruncDate('expiration_datetime')).values('date').annotate(payments_count=Count('id'))

    response_data = []
    total_payments = 0

    for date in dates_of_month:
        payment_data = next((p for p in payments_by_date if p['date'] == date.date()), None)
        count = payment_data['payments_count'] if payment_data else 0
        total_payments += count
        response_data.append({
            'date': date,
            'payments': count
        })

    response_data.insert(0, {'total_payments': total_payments})
    return response_data




def search_payment(export, q, start_date, end_date, plan, request, url, product, source, origin,status):
    payments = Main_Payment.objects.exclude(product__product_name__in=["test", "Test Course", "Test"]).exclude(amount__in=[1, 2, 0, 0.01, 1.0, 2.0, 3.0, 4.0, 5.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 10, 1])
    statuses = ["0",False,0]
    payments = payments.exclude(source='UBL_DD', status__in=statuses)

    if status:
        payments = payments.filter(status=status)
    
    if source:
        payments = payments.filter(source=source)
   
    if origin:
        if origin == 'local':
            payments = payments.filter(source__in=['Easypaisa', 'UBL_IPG','UBL_DD','Al-Nafi','NEW ALNAFI'])
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
    
    if plan:
        if plan == 'yearly':
            payments = payments.filter(product__product_plan='Yearly')
        elif plan == 'halfyearly':
            payments = payments.filter(product__product_plan='Half Yearly')
        elif plan == 'quarterly':
            payments = payments.filter(product__product_plan='Quarterly')
        elif plan == 'monthly':
            payments = payments.filter(product__product_plan='Monthly')
    
            
    payment_cycle = payments.values_list('product__product_plan', flat=True).distinct()
    payment_cycle_descriptions = {
        'Monthly': 'Monthly',
        'Yearly': 'Yearly',
        'Half Yearly': 'Half-Yearly',
        'Quarterly': 'Quarterly'
    # Add more plan-value pairs as needed
    }   

    # Annotate the payment queryset with the payment cycle field
    payments = payments.annotate(
        payment_cycle =Case(
            *[When(product__product_plan=plan, then=Value(description)) for plan, description in payment_cycle_descriptions.items()],
            default=Value('Unknown Plan'),
            output_field=CharField()
        )
    )
    if not payments:  # Check if payments queryset is empty
        response_data = {"payments": payments, "success": "false"}
    else:
        response_data = {"payments": payments, "success": "true"}
    return response_data


def get_USD_rate():
    # usd_details = cache.get("usd_details")
    # if usd_details:
        # print(usd_details)
        # print("usd_details", usd_details["PKR"])
        # return json.loads(usd_details)
    usd_details = {}
    url = f"https://v6.exchangerate-api.com/v6/{settings.EXCHANGE_RATE_API_KEY}/latest/USD"
    response = requests.get(url).json()
    # print(response)
    usd_details["PKR"] = response["conversion_rates"]["PKR"]
    usd_details["USD"] = response["conversion_rates"]["USD"]

    # cache.set("usd_details", json.dumps(usd_details), 60*120)
    # print("usd_details",usd_details)
    return usd_details
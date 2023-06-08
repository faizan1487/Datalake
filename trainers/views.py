from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache

# Create your views here.
from payment.models import Main_Payment
from payment.serializer import MainPaymentSerializer
from products.models import Alnafi_Product, Main_Product
from trainers.models import Trainer
from user.models import AlNafi_User, Main_User
from user.serializers import MainUserSerializer
from django.db.models import Count, OuterRef, Subquery
from collections import defaultdict
import json
from django.db.models import F, Max, Q
from datetime import date, datetime, time, timedelta
from django.db.models import Prefetch

class MyPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100     



# class TrainersData(APIView):
#     # permission_classes = [IsAuthenticated]
#     # permission_classes = [GroupPermission]
#     # required_groups = ['Sales', 'Admin']
#     def get(self, request):
#         q = self.request.GET.get('q', None) or None
#         product = self.request.GET.get('product', None)
#         export = self.request.GET.get('export', None) or None
#         # create a datetime object for 24 hours ago
#         url = request.build_absolute_uri()  
        
      
#         # payments = Main_Payment.objects.filter(product__product_name__icontains='Python Automation - Tools and handson')
#         # print(payments)
#         # payments = payments.exclude(amount__in=[0,0.1,1,2,0.01,1.0,2.0,3.0,4.0,5.0,5.0,6.0,7.0,8.0,9.0,10.0,10])
#         # distinct_users = payments.order_by('user').values('user').distinct()
#         trainers = Trainer.objects.all()
#         if q:
#             trainers = trainers.filter(trainer_name__icontains=q)

#         if product:
#             keywords = product.split()
#             query = Q()
#             for keyword in keywords:
#                 query &= Q(products__product_name__icontains=keyword)
#                 trainers = trainers.filter(query)

#         trainers = trainers.annotate(total_users=Count('products__product_payments__user', distinct=True)).values('trainer_name', 'products__product_name', 'products__product_payments__user__email','products__product_payments__user__username')
#         # Create a dictionary to store the grouped data
#         grouped_data = defaultdict(lambda: defaultdict(list))

#         # Iterate over the queryset and group the data
#         for trainer in trainers:
#             trainer_name = trainer['trainer_name']
#             product_name = trainer['products__product_name']
#             user_email = trainer['products__product_payments__user__username' if 'products__product_payments__user__email' == None else 'products__product_payments__user__email']
#             grouped_data[trainer_name][product_name].append(user_email)

#         # print(grouped_data)

#         # Convert the grouped data to a list of dictionaries
#         result = []
#         for trainer_name, products in grouped_data.items():
#             # print("trainer_namee",trainer_name)
#             # print("products",products)
#             for product_name, users in products.items():
#                 result.append({
#                     'trainer_name': trainer_name,
#                     'product_name': product_name,
#                     # 'users': users,
#                     'user_count': len(users)-1 if users[0] == None else len(users)
#                 })
#                 # print("users",len(users))

#         # print(result[-1])
#         # payments = payments.filter(user__id__in=Subquery(distinct_users)).values('product__id', 'product__product_name').annotate(total_payments=Count('id'))
#         paginator = MyPagination()
#         paginated_queryset = paginator.paginate_queryset(result, request)
#         return paginator.get_paginated_response(paginated_queryset)    



# class TrainersData(APIView):
#     def get(self, request):
#         q = self.request.GET.get('q', None) or None
#         product = self.request.GET.get('product', None)
#         export = self.request.GET.get('export', None) or None
#         url = request.build_absolute_uri()  
        
#         trainers = Trainer.objects.all().prefetch_related('products__product_payments__user')
#         if q:
#             trainers = trainers.filter(trainer_name__icontains=q)

#         if product:
#             keywords = product.split()
#             query = Q()
#             for keyword in keywords:
#                 query &= Q(products__product_name__icontains=keyword)
#             trainers = trainers.filter(query)

#         trainers_data = []

#         for trainer in trainers:
#             trainer_data = {
#                 'trainer_name': trainer.trainer_name,
#                 'products': {}
#             }

#             for product in trainer.products.all():
#                 user_count = len(set(payment.user_id for payment in product.product_payments.all()))
#                 trainer_data['products'][product.product_name] = user_count

#             trainers_data.append(trainer_data)

#         return Response(trainers_data)


class TrainersData(APIView):
    def get(self, request):
        q = self.request.GET.get('q', None) or None
        product = self.request.GET.get('product', None)
        export = self.request.GET.get('export', None) or None
        url = request.build_absolute_uri()  
        
        trainers = Trainer.objects.all().prefetch_related('products__product_payments__user')
        if q:
            trainers = trainers.filter(trainer_name__icontains=q)

        if product:
            keywords = product.split()
            query = Q()
            for keyword in keywords:
                query &= Q(products__product_name__icontains=keyword)
            trainers = trainers.filter(query)

        trainers_data = []

        for trainer in trainers:
            trainer_data = {
                'trainer_name': trainer.trainer_name,
                'trainer_data': []
            }

            for product in trainer.products.all():
                user_count = len(set(payment.user_id for payment in product.product_payments.all()))
                trainer_data['trainer_data'].append({'product_name':product.product_name,'users': user_count})

            trainers_data.append(trainer_data)

        return Response(trainers_data)











class AnalyticsTrainers(APIView):
    def get(self, request):
        q = self.request.GET.get('q', None) or None
        trainers = Trainer.objects.all()
        if q:
            trainers = trainers.filter(trainer_name__icontains=q)

        trainers_data = []

        for trainer in trainers:
            trainer_data = {
                'trainer_name': trainer.trainer_name,
                'user_counts': []
            }

            user_count = 0

            products = trainer.products.all().prefetch_related('product_payments')
            payments = Main_Payment.objects.filter(product__in=products).order_by('order_datetime')

            for payment in payments:
                user_count += 1
                trainer_data['user_counts'].append({
                    'order_datetime': payment.order_datetime,
                    'user_count': user_count
                })
            trainers_data.append(trainer_data)
        

        # print(trainers_data)
        return Response(trainers_data)




# payments = Main_Payment.objects.exclude(product__product_name="test").exclude(amount=1).filter(source__in=['Easypaisa','UBL_IPG','Stripe'])
    
#     if source:
#         payments = payments.filter(source=source)
        
#     if not start_date:
#         if payments:
#             first_payment = payments.exclude(order_datetime=None).last()
#             date_time_obj = first_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
#             new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")                                                                                    
#             start_date = new_date_obj + timedelta(days=20)       
#     if not end_date:
#         if payments:
#             last_payment = payments.exclude(order_datetime=None).first()
#             date_time_obj = last_payment.order_datetime.strftime("%Y-%m-%d %H:%M:%S.%f%z")
#             new_date_obj = datetime.strptime(date_time_obj, "%Y-%m-%d %H:%M:%S.%f")
#             end_date = new_date_obj - timedelta(days=20)
               
#     delta = end_date - start_date
#     dates = []
#     for i in range(delta.days + 1):
#         date = start_date + timedelta(days=i)
#         dates.append(date)
        
#     payments = payments.filter(order_datetime__date__in=dates)
#     payment_dict = {}
#     for payment in payments:
#         if payment.order_datetime.date() in payment_dict:
#             payment_dict[payment.order_datetime.date()].append(payment)
#         else:
#             payment_dict[payment.order_datetime.date()] = [payment]

#     response_data = []
#     for date in dates:
#         if date.date() in payment_dict:
#             payments_for_date = payment_dict[date.date()]
#             serialized_payments = MainPaymentSerializer(payments_for_date, many=True).data
#         else:
#             serialized_payments = []

#         response_data.append({
#             'date': date.date(),
#             'payments': len(serialized_payments)
#         })
    
#     print(payments.count())
#     return response_data